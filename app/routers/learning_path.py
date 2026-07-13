# app/routers/learning_path.py
"""
API endpoints cho Learning Path:
  GET  /api/learning/dashboard
  GET  /api/learning/topics/{level}
  GET  /api/learning/topic/{topic_id}
  GET  /api/learning/lesson/{lesson_id}
  POST /api/learning/topic/{topic_id}/lesson/{lesson_order}/complete
  GET  /api/learning/eligibility
  POST /api/learning/analyze-error
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.topic_service import TopicService
from app.services.error_service import ErrorService
from app.services.level_progress_service import LevelProgressService
from app.schemas.learning import (
    DashboardResponse,
    TopicResponse,
    TopicDetailResponse,
    LessonResponse,
    UpdateLessonProgressResponse,
    AnalyzeErrorRequest,
    ActivateLearningContextRequest,
    LearningContextResponse,
)
from app.schemas.learning_action import ExecuteActionRequest

router = APIRouter(prefix="/api/learning", tags=["Learning Path"])
_svc = TopicService()


@router.get("/test-ping")
async def test_ping():
    """Simple test endpoint - no dependencies, no schema"""
    return {"status": "ok", "message": "Learning Path router is alive!", "timestamp": "2026-06-03"}


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Bảng điều khiển học tập: tiến độ, chủ đề tiếp theo, điều kiện level-up."""
    return await _svc.get_dashboard(current_user.id, db)


@router.get("/topics/{level}", response_model=list[TopicResponse])
async def list_topics(
    level: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Danh sách chủ đề của một level (kèm tiến độ của user)."""
    level = level.upper()
    if level not in {"A1", "A2", "B1", "B2", "C1", "C2"}:
        raise HTTPException(status_code=400, detail=f"Invalid level: {level}")
    return await _svc.get_topics_by_level(level, current_user.id, db)


@router.get("/topic/{topic_id}", response_model=TopicDetailResponse)
async def get_topic_detail(
    topic_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Chi tiết chủ đề + danh sách bài học (không có nội dung đầy đủ)."""
    detail = await _svc.get_topic_detail(topic_id, current_user.id, db)
    if not detail:
        raise HTTPException(status_code=404, detail="Topic not found")
    return detail


@router.get("/lesson/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Nội dung đầy đủ của một bài học."""
    lesson = await _svc.get_lesson(lesson_id, db)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post(
    "/topic/{topic_id}/lesson/{lesson_order}/complete",
    response_model=UpdateLessonProgressResponse,
)
async def complete_lesson(
    topic_id: UUID,
    lesson_order: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Đánh dấu một bài học đã hoàn thành, cập nhật tiến độ."""
    if lesson_order not in range(1, 6):
        raise HTTPException(status_code=400, detail="lesson_order must be 1-5")
    return await _svc.complete_lesson(topic_id, lesson_order, current_user.id, db)


@router.get("/eligibility")
async def check_level_up_eligibility(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Kiểm tra xem user đủ điều kiện làm Level-Up Test chưa (Unified Check)."""
    try:
        from app.services.level_service_unified import LevelServiceUnified
        
        unified_svc = LevelServiceUnified()
        result = await unified_svc.get_eligibility(
            current_user.id,
            current_user.current_level,
            db
        )
        return result
    except Exception as e:
        logger.exception(f"Error checking eligibility: {e}")
        raise HTTPException(status_code=500, detail="Error checking eligibility")


@router.post("/analyze-error")
async def analyze_error(
    request: AnalyzeErrorRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Phân tích lỗi của user khi làm practice/quiz sai
    Trả về error analysis + suggestion + frequency
    """
    try:
        # 1. Analyze error using ErrorAnalyzerAgent
        from app.tools.tool_registry import tool_registry
        
        result = await tool_registry.execute(
            "error_analyzer",
            {
                "question": request.question,
                "user_answer": request.user_answer,
                "correct_answer": request.correct_answer,
                "skill_tag": request.skill_tag
            }
        )
        
        # Unwrap if needed
        if result.get("success") and "data" in result:
            error_data = result["data"]
        else:
            error_data = result
        
        # 2. Get error frequency (before logging this error)
        frequency_data = await ErrorService.get_error_frequency(
            user_id=str(current_user.id),
            error_type=error_data["error_type"],
            db=db
        )
        
        # Current frequency (will be this number + 1 after logging)
        current_freq = frequency_data["frequency"]
        
        # 3. Log error to database FIRST
        await ErrorService.log_error(
            user_id=str(current_user.id),
            error_data=error_data,
            question=request.question,
            user_answer=request.user_answer,
            correct_answer=request.correct_answer,
            db=db,
            lesson_id=str(request.lesson_id) if request.lesson_id else None,
            topic_id=str(request.topic_id) if request.topic_id else None
        )
        
        # Now frequency is current_freq + 1
        freq = current_freq + 1
        
        # 4. Generate personalized suggestion based on NEW frequency
        suggestion = await ErrorService.generate_suggestion(
            user_id=str(current_user.id),
            error_data=error_data,
            frequency=freq,
            db=db
        )
        
        error_data["suggestion"] = suggestion
        
        # 5. Determine recommendation type
        if freq == 1:
            recommendation_type = "FIRST_TIME"
        elif freq <= 3:
            recommendation_type = "EXPLAIN_WITH_EXAMPLES"
        elif freq <= 5:
            recommendation_type = "INTENSIVE_PRACTICE"
        else:
            recommendation_type = "BACK_TO_BASICS"
        
        return {
            "error": error_data,
            "frequency": freq,
            "suggestion": suggestion,
            "recommendation_type": recommendation_type,
            "next_action": {
                "type": "PRACTICE" if freq > 2 else "REVIEW",
                "count": min(5, freq + 2)  # Số bài tập gợi ý
            }
        }
        
    except Exception as e:
        from loguru import logger
        logger.error(f"Error analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Error analysis failed: {str(e)}")


# ── Learning Context Activation (Sprint 1) ──────────────────────────

@router.post("/activate-context")
async def activate_learning_context(
    request: ActivateLearningContextRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Set active topic/lesson/mode on user profile.
    This context will be passed to AI Tutor for every chat.
    """
    await _svc.set_active_context(
        user_id=current_user.id,
        topic_id=request.topic_id,
        lesson_order=request.lesson_order,
        learning_mode=request.learning_mode,
        db=db,
    )
    return {"status": "ok", "message": "Learning context activated"}


@router.get("/context", response_model=LearningContextResponse)
async def get_learning_context(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current learning context for the user.
    Returns active topic, lesson, mode, level, etc.
    """
    context = await _svc.get_learning_context(current_user.id, db)
    if not context:
        raise HTTPException(status_code=404, detail="User context not found")
    return context


@router.get("/level-up-eligibility")
async def get_level_up_eligibility(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    B5: Check if user is eligible for level-up test
    Returns eligibility status and requirements
    """
    service = LevelProgressService()
    result = await service.check_eligibility(current_user.id, db)
    return result


# ── Phase 3: Execute Agent-suggested Actions ────────────────────

@router.post("/execute-action")
async def execute_action(
    request: ExecuteActionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Phase 3: Execute an action suggested by Learning Orchestrator
    Routes action_type to appropriate service
    Returns redirect_page for Streamlit to handle
    """
    from app.schemas.learning_action import ExecuteActionResponse, SuggestedActionType
    from loguru import logger
    
    try:
        action_type = request.action_type
        params = request.params
        
        # Route to appropriate handler
        if action_type == SuggestedActionType.COMPLETE_LESSON:
            # Mark lesson as complete
            topic_id = params.get("topic_id")
            lesson_order = params.get("lesson_order")
            
            if not topic_id or not lesson_order:
                return ExecuteActionResponse(
                    success=False,
                    message="Missing topic_id or lesson_order"
                )
            
            # Handle both string and UUID types
            topic_uuid = UUID(topic_id) if isinstance(topic_id, str) else topic_id
            
            result = await _svc.complete_lesson(
                topic_uuid,
                int(lesson_order),
                current_user.id,
                db
            )
            
            # Calculate next lesson order
            next_lesson = int(lesson_order) + 1 if int(lesson_order) < 5 else None
            
            return ExecuteActionResponse(
                success=True,
                message=f"✅ Đã hoàn thành bài {lesson_order}!",
                redirect_page="lesson" if next_lesson else None,
                data={
                    "topic_id": str(topic_id),
                    "next_lesson_order": next_lesson,
                    "lesson_completed": result.lesson_completed,
                    "status": result.status.value
                }
            )
        
        elif action_type == SuggestedActionType.START_QUIZ:
            # Redirect to quiz page
            topic_id = params.get("topic_id")
            
            if not topic_id:
                return ExecuteActionResponse(
                    success=False,
                    message="Missing topic_id"
                )
            
            return ExecuteActionResponse(
                success=True,
                message="🎯 Chuyển đến quiz...",
                redirect_page="quiz",
                data={"topic_id": topic_id}
            )
        
        elif action_type == SuggestedActionType.GO_TO_LESSON:
            # Activate new lesson
            topic_id = params.get("topic_id")
            lesson_order = params.get("lesson_order")
            
            if not topic_id or not lesson_order:
                return ExecuteActionResponse(
                    success=False,
                    message="Missing topic_id or lesson_order"
                )
            
            # Handle both string and UUID types
            topic_uuid = UUID(topic_id) if isinstance(topic_id, str) else topic_id
            
            await _svc.set_active_context(
                user_id=current_user.id,
                topic_id=str(topic_uuid),  # set_active_context expects string
                lesson_order=int(lesson_order),
                learning_mode="lesson",
                db=db
            )
            
            return ExecuteActionResponse(
                success=True,
                message=f"📖 Đã chuyển đến bài {lesson_order}",
                redirect_page="lesson",
                data={
                    "topic_id": topic_id,
                    "lesson_order": lesson_order
                }
            )
        
        elif action_type == SuggestedActionType.OFFER_PRACTICE:
            # Stay on chat, Agent will generate practice
            return ExecuteActionResponse(
                success=True,
                message="✏️ AI sẽ tạo bài tập cho bạn...",
                redirect_page=None,  # Stay on chat
                data={"count": params.get("count", 5)}
            )
        
        elif action_type == SuggestedActionType.START_LEVEL_UP_TEST:
            # Redirect to level-up test
            return ExecuteActionResponse(
                success=True,
                message="🚀 Chuyển đến bài thi level-up...",
                redirect_page="level_up",
                data={"current_level": params.get("current_level")}
            )
        
        elif action_type == SuggestedActionType.QUIZ_REVIEW:
            # Stay on chat, already in review mode
            return ExecuteActionResponse(
                success=True,
                message="📝 Tiếp tục ôn lại lỗi...",
                redirect_page=None,
                data=params
            )
        
        elif action_type == SuggestedActionType.REVIEW_WEAK_SKILL:
            # Stay on chat, Agent will guide review
            return ExecuteActionResponse(
                success=True,
                message="🔄 Bắt đầu ôn luyện...",
                redirect_page=None,
                data=params
            )
        
        elif action_type == SuggestedActionType.CONTINUE_LESSON:
            # Stay on chat
            return ExecuteActionResponse(
                success=True,
                message="📖 Tiếp tục học...",
                redirect_page=None,
                data=params
            )
        
        elif action_type == SuggestedActionType.FREE_CHAT:
            # Stay on chat
            return ExecuteActionResponse(
                success=True,
                message="💬 Hỏi gì cũng được!",
                redirect_page=None,
                data=params
            )
        
        else:
            return ExecuteActionResponse(
                success=False,
                message=f"Unknown action type: {action_type}"
            )
    
    except Exception as e:
        logger.exception(f"Error executing action {request.action_type}: {e}")
        return ExecuteActionResponse(
            success=False,
            message=f"Lỗi: {str(e)}"
        )
