from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import json
import asyncio

from app.core.database import get_db
from app.core.deps import get_current_user
from app.services.service_container import get_learning_service
from app.services.conversation_service import ConversationService
from app.services.ai_exercise_service import AIExerciseService
from app.schemas.chat import ChatRequest, ChatResponse
from app.models.user import User
from app.utils.exercise_parser import parse_exercises_from_response
from loguru import logger

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"🔵 CHAT REQUEST START: user={current_user.id}, input={request.user_input[:50]}...")
    
    try:
        # Lazy-load learning service on first use
        logger.info("🔵 Loading learning service...")
        learning_service = get_learning_service()
        
        logger.info(f"🔵 Processing chat with learning service...")
        result = await learning_service.process(
            user_input=request.user_input,
            user_id=str(current_user.id),
            db=db,
            session_id=request.session_id,
            quiz_wrong_answers=request.quiz_wrong_answers,
            quiz_topic_id=request.quiz_topic_id,
            target_lang=request.target_lang,
            explain_in=request.explain_in
        )
        
        logger.info(f"🔵 Learning service returned: success={result.get('success')}")
        
        response_text = result.get("response", "")
        
        # Check if response contains exercises and save to DB
        exercises = parse_exercises_from_response(response_text)
        if exercises and len(exercises) >= 3:
            # Save exercises in background
            background_tasks.add_task(
                save_exercises_to_db,
                user_id=current_user.id,
                session_id=request.session_id,
                exercises=exercises,
                user_input=request.user_input,
                db=db
            )
            
            logger.info(f"Detected {len(exercises)} exercises in AI response, saving to DB")
        
        logger.info(f"🟢 CHAT REQUEST SUCCESS: response_length={len(response_text)}")
        
        return ChatResponse(
            response=response_text,
            metadata=result.get("metadata", {}),
            success=result.get("success", False),
            error=result.get("error")
        )
    except Exception as e:
        logger.error(f"🔴 CHAT ERROR: {str(e)}")
        logger.error(f"🔴 Error type: {type(e).__name__}")
        logger.exception(e)  # Log full traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi xử lý chat: {str(e)}"
        )


@router.post("/stream")
async def chat_with_ai_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Streaming endpoint for better UX - response appears word by word"""
    
    async def generate_stream():
        try:
            logger.info(f"🌊 STREAM REQUEST START: user={current_user.id}, input={request.user_input[:50]}...")
            
            # Import here to avoid circular dependency
            from app.llm.prompts import build_prompt
            
            # Simple fast-path: Skip full LangGraph for streaming
            # Just get essentials and stream LLM response
            
            # Load minimal context
            from app.services.quiz_analytics_service import QuizAnalyticsService
            try:
                skill_breakdown = await QuizAnalyticsService.get_skill_breakdown(db, str(current_user.id))
                analytics_context = {"skill_breakdown": skill_breakdown}
            except:
                analytics_context = {}
            
            # Build prompt
            system_prompt = build_prompt(
                user_input=request.user_input,
                strategy={"mode": "tutor", "explain_in": request.explain_in or "Tiếng Việt"},
                plan={"intent": "chat", "tools_to_use": []},
                rag_context="",
                analytics_context=analytics_context,
                quiz_context=None,
                short_mem=None,
                tool_results=None
            )
            
            # Stream LLM response
            from app.llm.llm_client import get_llm_client
            llm_client = get_llm_client()
            
            full_response = ""
            async for chunk in llm_client.stream_async(
                user_input=request.user_input,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1500
            ):
                full_response += chunk
                # Send as Server-Sent Events format
                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'chunk': '', 'done': True, 'full_response': full_response})}\n\n"
            
            logger.info(f"🌊 STREAM COMPLETE: response_length={len(full_response)}")
            
        except Exception as e:
            logger.error(f"🔴 STREAM ERROR: {str(e)}")
            error_data = json.dumps({'error': str(e), 'done': True})
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


async def save_exercises_to_db(
    user_id: UUID,
    session_id: str,
    exercises: list,
    user_input: str,
    db: AsyncSession
):
    """Background task to save exercises"""
    try:
        # Parse error context from user input
        error_type = "GRAMMAR_ERROR"  # Default
        skill_tag = "general"
        frequency = 1
        
        # Try to extract from user input (if it's from AI Tutor mode)
        if "TUTOR MODE" in user_input or "ERROR" in user_input:
            # This is from AI Tutor error remediation
            # Try to extract error_type
            if "TENSE" in user_input.upper():
                error_type = "TENSE_MISMATCH"
                skill_tag = "present_continuous"
            elif "SUBJECT_VERB" in user_input.upper():
                error_type = "SUBJECT_VERB_AGREEMENT"
            
            # Try to extract frequency
            import re
            freq_match = re.search(r'Times Wrong:\s*(\d+)', user_input)
            if freq_match:
                frequency = int(freq_match.group(1))
        
        service = AIExerciseService()
        await service.create_exercise(
            user_id=user_id,
            session_id=UUID(session_id) if session_id else None,
            error_type=error_type,
            skill_tag=skill_tag,
            frequency=frequency,
            exercises=exercises,
            db=db
        )
        
        logger.success(f"Saved {len(exercises)} exercises to DB for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to save exercises: {e}")


from pydantic import BaseModel

class SaveMessageRequest(BaseModel):
    """Request model for saving chat message"""
    session_id: str
    role: str  # "user" or "assistant"
    message: str
    model_used: str = "gpt-4"
    tokens: int = 0
    topic_id: str | None = None
    learning_mode: str = "normal"


@router.post("/save-message")
async def save_chat_message(
    request: SaveMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save a chat message to database"""
    try:
        conv = await ConversationService.save_message(
            user_id=current_user.id,
            session_id=request.session_id,
            role=request.role,
            message=request.message,
            model_used=request.model_used,
            tokens=request.tokens,
            topic_id=request.topic_id,
            learning_mode=request.learning_mode,
            db=db
        )
        return {
            "success": True,
            "message_id": str(conv.id),
            "created_at": conv.created_at.isoformat() if conv.created_at else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lưu message: {str(e)}"
        )


@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get chat history for a session"""
    try:
        history = await ConversationService.get_messages_by_session(
            user_id=current_user.id,
            session_id=session_id,
            db=db,
            limit=limit
        )
        return {
            "success": True,
            "session_id": session_id,
            "messages": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy history: {str(e)}"
        )


@router.get("/sessions")
async def get_all_sessions(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all chat sessions for current user"""
    try:
        sessions = await ConversationService.get_sessions_by_user(
            user_id=current_user.id,
            db=db,
            limit=limit
        )
        return {
            "success": True,
            "sessions": sessions,
            "count": len(sessions)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy sessions: {str(e)}"
        )