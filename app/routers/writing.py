# app/routers/writing.py
"""API endpoints for writing submissions"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.writing_service import WritingService
from app.schemas.writing import (
    SubmitWritingRequest,
    WritingFeedbackResponse,
    WritingHistoryItem,
    WritingStatsResponse
)
from loguru import logger

router = APIRouter(prefix="/api/writing", tags=["Writing"])
_svc = WritingService()


@router.post("/submit", response_model=WritingFeedbackResponse)
async def submit_writing(
    request: SubmitWritingRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit writing for AI review
    Returns structured feedback with scoring rubric
    """
    try:
        # Fetch lesson and topic information for context-aware grading
        from app.models.lesson import Lesson
        from app.models.topic import Topic
        from sqlalchemy import select
        
        lesson_result = await db.execute(
            select(Lesson).where(Lesson.id == request.lesson_id)
        )
        lesson = lesson_result.scalar_one_or_none()
        
        topic = None
        if lesson:
            topic_result = await db.execute(
                select(Topic).where(Topic.id == lesson.topic_id)
            )
            topic = topic_result.scalar_one_or_none()
        
        # Save submission to database
        writing = await _svc.submit_writing(
            user_id=current_user.id,
            lesson_id=request.lesson_id,
            topic_id=request.topic_id,
            prompt=request.prompt,
            user_text=request.user_text,
            word_count=request.word_count,
            db=db
        )
        
        # Get AI feedback using WritingAgent
        from app.tools.tool_registry import tool_registry
        
        # Build context for agent
        cefr_level = topic.level if topic else "B1"
        
        try:
            # Call WritingAgent through tool_registry
            result = await tool_registry.execute(
                "writing_evaluator",
                {
                    "user_text": request.user_text,
                    "prompt": request.prompt,
                    "cefr_level": cefr_level
                }
            )
            
            # Unwrap if needed
            if result.get("success") and "data" in result:
                feedback_result = result["data"]
            else:
                feedback_result = result
            
            if not feedback_result.get("success"):
                raise ValueError(feedback_result.get("error", "Writing evaluation failed"))
            
            # Save feedback to database
            await _svc.save_feedback(
                writing_id=writing.id,
                feedback=feedback_result.get("feedback", "No feedback provided"),
                score_grammar=feedback_result.get("score_grammar", 20.0),
                score_vocabulary=feedback_result.get("score_vocabulary", 20.0),
                score_content=feedback_result.get("score_content", 20.0),
                score_structure=feedback_result.get("score_structure", 20.0),
                detailed_feedback=feedback_result.get("detailed_feedback"),
                db=db
            )
            
            # Refresh to get updated data
            await db.refresh(writing)
            
            return WritingFeedbackResponse(
                writing_id=writing.id,
                attempt_number=writing.attempt_number,
                feedback=writing.feedback,
                score_grammar=writing.score_grammar,
                score_vocabulary=writing.score_vocabulary,
                score_content=writing.score_content,
                score_structure=writing.score_structure,
                score_total=writing.score_total,
                detailed_feedback=writing.detailed_feedback,
                submitted_at=writing.submitted_at,
                reviewed_at=writing.reviewed_at
            )
            
        except Exception as e:
            logger.error(f"WritingAgent evaluation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Writing evaluation failed: {str(e)}")
        
    except Exception as e:
        logger.exception(f"Error submitting writing: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing writing: {str(e)}")


@router.get("/history", response_model=list[WritingHistoryItem])
async def get_writing_history(
    lesson_id: UUID = None,
    topic_id: UUID = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's writing history"""
    writings = await _svc.get_user_writings(
        user_id=current_user.id,
        db=db,
        lesson_id=lesson_id,
        topic_id=topic_id,
        limit=limit
    )
    return writings


@router.get("/stats", response_model=WritingStatsResponse)
async def get_writing_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's writing statistics"""
    stats = await _svc.get_writing_stats(current_user.id, db)
    return WritingStatsResponse(**stats)
