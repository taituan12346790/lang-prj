# app/routers/quiz.py
"""
Quiz API endpoints:
  GET  /api/quiz/topic/{topic_id}/questions
  POST /api/quiz/topic/{topic_id}/submit
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.topic_service import TopicService
from app.services.quiz_enhanced import QuizEnhancedService
from app.schemas.learning import (
    QuizQuestionsResponse,
    QuizSubmitRequest,
    QuizSubmitResponse,
)

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])
_svc = TopicService()
_enhanced_svc = QuizEnhancedService()


@router.get("/topic/{topic_id}/questions", response_model=QuizQuestionsResponse)
async def get_quiz_questions(
    topic_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy câu hỏi quiz của một chủ đề (không có đáp án đúng)."""
    result = await _svc.get_quiz_questions(topic_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Quiz not found for this topic")
    return result


@router.post("/topic/{topic_id}/submit")
async def submit_quiz(
    topic_id: UUID,
    request: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Nộp bài quiz, nhận điểm, phản hồi chi tiết, và weak_skills cho AI review."""
    try:
        # Use enhanced service to get quiz results + weak_skills + AI context
        result = await _enhanced_svc.submit_quiz_with_chat_context(
            topic_id=topic_id,
            user_id=current_user.id,
            request=request,
            db=db,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Log the actual error
        import traceback
        print(f"❌ Quiz submission error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Quiz submission failed: {str(e)}")
