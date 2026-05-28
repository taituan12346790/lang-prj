from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from app.services.learning_service import LearningService

logger = logging.getLogger(__name__)

router = APIRouter()
service = LearningService()

class ChatRequest(BaseModel):
    user_input: str
    user_id: str = "default_user"
    session_id: Optional[str] = None
    
    # === Thêm các trường hỗ trợ multi-language ===
    target_lang: Optional[str] = None      # Ví dụ: "Tiếng Đức", "Tiếng Nhật", "Tiếng Anh"
    explain_in: Optional[str] = "Tiếng Việt"
    difficulty: Optional[str] = None
    temperature: Optional[float] = 0.7


class ChatResponse(BaseModel):
    response: str
    processing_time: Optional[float] = None
    target_lang: Optional[str] = None
    success: bool = True


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint chính để chat với AI Language Tutor
    Hỗ trợ thay đổi ngôn ngữ mục tiêu theo từng request
    """
    try:
        # Gọi service (LearningService sẽ nhận thêm override)
        result = await service.process(
            user_input=request.user_input,
            user_id=request.user_id,
            target_lang=request.target_lang,
            explain_in=request.explain_in,
            difficulty=request.difficulty,
            temperature=request.temperature
        )

        if isinstance(result, dict):
            return ChatResponse(
                response=result.get("response", str(result)),
                processing_time=result.get("processing_time"),
                target_lang=result.get("target_lang"),
                success=result.get("success", True)
            )
        else:
            return ChatResponse(response=str(result))

    except Exception as e:
        logger.exception(f"Error in /chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )