# app/routers/analytics.py
"""
Analytics API endpoints:
  GET /api/analytics/dashboard - Thống kê tổng quan
  GET /api/analytics/skills - Phân tích theo skill
  GET /api/analytics/reviews - Topics cần ôn tập
  GET /api/analytics/timeline - Timeline học tập
  POST /api/analytics/ai-help - Yêu cầu AI giải thích lỗi
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.quiz_analytics_service import QuizAnalyticsService
from app.services.ai_context_service import AIContextService
from pydantic import BaseModel


router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


class DashboardAnalytics(BaseModel):
    """Response model for dashboard analytics"""
    study_streak: int
    last_study_date: str | None
    total_exercises: int
    correct_rate: float
    weak_skills: Dict[str, float]
    skill_breakdown: Dict[str, Any]
    level_eligible: bool = False  # Phase 4
    eligibility_details: Dict[str, Any] = {}  # Phase 4


class AIHelpRequest(BaseModel):
    """Request để AI giải thích lỗi quiz"""
    topic_id: str | None = None
    lesson_id: str | None = None
    quiz_results: List[Dict[str, Any]] | None = None
    question: str | None = None


class AIHelpResponse(BaseModel):
    """Response từ AI"""
    explanation: str
    suggestions: List[str]
    practice_prompts: List[Dict[str, Any]]


@router.get("/dashboard")
async def get_analytics_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DashboardAnalytics:
    """Lấy analytics tổng quan cho dashboard"""
    skill_breakdown = await QuizAnalyticsService.get_skill_breakdown(db, str(current_user.id))
    
    # Calculate total and correct
    total_exercises = sum(s["total"] for s in skill_breakdown.values())
    total_correct = sum(s["correct"] for s in skill_breakdown.values())
    correct_rate = total_correct / total_exercises if total_exercises > 0 else 0
    
    # Find weak skills
    weak_skills = {
        skill: data["accuracy"]
        for skill, data in skill_breakdown.items()
        if data["accuracy"] < 0.6
    }
    
    # Phase 4: Add level-up eligibility check
    level_eligible = False
    eligibility_details = {}
    try:
        from app.services.level_progress_service import LevelProgressService
        eligibility_service = LevelProgressService()
        eligibility_result = await eligibility_service.check_eligibility(current_user.id, db)
        level_eligible = eligibility_result.get("eligible", False)
        eligibility_details = eligibility_result
    except Exception as e:
        from loguru import logger
        logger.warning(f"Could not check level eligibility: {e}")
    
    return DashboardAnalytics(
        study_streak=current_user.study_streak or 0,
        last_study_date=current_user.last_study_date.isoformat() if current_user.last_study_date else None,
        total_exercises=total_exercises,
        correct_rate=round(correct_rate, 2),
        weak_skills=weak_skills,
        skill_breakdown=skill_breakdown,
        level_eligible=level_eligible,  # Phase 4
        eligibility_details=eligibility_details  # Phase 4
    )


@router.get("/skills")
async def get_skill_analysis(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Phân tích chi tiết theo từng skill"""
    return await QuizAnalyticsService.get_skill_breakdown(db, str(current_user.id))


@router.get("/reviews")
async def get_due_reviews(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[Dict]:
    """Lấy danh sách topics cần ôn tập hôm nay"""
    return await QuizAnalyticsService.get_due_reviews(db, str(current_user.id))


@router.get("/timeline")
async def get_learning_timeline(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[Dict]:
    """Lấy timeline học tập trong N ngày gần đây"""
    return await QuizAnalyticsService.get_learning_timeline(db, str(current_user.id), days)


@router.post("/ai-help")
async def get_ai_help(
    request: AIHelpRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AIHelpResponse:
    """
    Yêu cầu AI giải thích lỗi hoặc cung cấp bài tập
    
    Có thể gửi:
    - quiz_results: Để AI giải thích câu sai
    - topic_id + lesson_id: Để AI biết context
    - question: Câu hỏi trực tiếp
    """
    # Build learning context
    learning_context = AIContextService.build_learning_context(
        db,
        str(current_user.id),
        request.topic_id,
        request.lesson_id
    )
    
    # If quiz results provided, build review context
    review_context = ""
    if request.quiz_results:
        review_context = AIContextService.build_quiz_review_context(request.quiz_results)
    
    # Generate prompt for AI (this will be used by chat endpoint)
    base_prompt = "You are an experienced language tutor helping a student understand their mistakes."
    
    full_prompt = AIContextService.generate_system_prompt_with_context(
        base_prompt,
        learning_context + "\n" + review_context
    )
    
    # Here you would call your AI service (Gemini/Claude)
    # For now, return the prompt structure
    explanation = f"Context prepared for AI:\n{full_prompt}"
    
    # Get weak skills from context if available
    weak_skills = {}
    if request.quiz_results:
        for r in request.quiz_results:
            if not r.get("is_correct") and "skill_tag" in r:
                skill = r["skill_tag"]
                weak_skills[skill] = weak_skills.get(skill, 0) + 1
    
    suggestions = AIContextService.suggest_exercises_for_weak_skills(
        {k: v/10 for k, v in weak_skills.items()},  # Convert count to fake accuracy
        target_count=3
    )
    
    return AIHelpResponse(
        explanation=explanation,
        suggestions=[
            "Review the grammar rules mentioned above",
            "Practice with similar exercises",
            "Ask specific questions about confusing parts"
        ],
        practice_prompts=suggestions
    )


@router.get("/chat-activities")
async def get_chat_activities(
    days: int = 30,
    activity_type: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Lấy danh sách hoạt động học từ AI Tutor chat
    
    Query params:
    - days: Số ngày gần đây (default 30)
    - activity_type: Lọc theo loại (lesson, practice, quiz, vocabulary)
    """
    from app.services.chat_learning_service import ChatLearningService
    
    # Get activities
    activities = await ChatLearningService.get_user_chat_activities(
        db=db,
        user_id=current_user.id,
        days=days,
        activity_type=activity_type,
    )
    
    # Get summary
    summary = await ChatLearningService.get_activity_summary(
        db=db,
        user_id=current_user.id,
        days=days,
    )
    
    # Format activities for response
    formatted_activities = [
        {
            "id": str(activity.id),
            "type": activity.activity_type,
            "title": activity.title,
            "custom_topic": activity.custom_topic,
            "score": activity.score,
            "skill_tags": activity.skill_tags,
            "created_at": activity.created_at.isoformat(),
            "session_id": activity.chat_session_id,
        }
        for activity in activities
    ]
    
    return {
        "total": len(activities),
        "summary": summary,
        "activities": formatted_activities,
    }

