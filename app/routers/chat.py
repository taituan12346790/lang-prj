from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.services.service_container import get_learning_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.models.user import User

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Lazy-load learning service on first use
        learning_service = get_learning_service()
        result = await learning_service.process(
            user_input=request.user_input,
            user_id=str(current_user.id),
            db=db,
            target_lang=request.target_lang,
            explain_in=request.explain_in
        )
        return ChatResponse(
            response=result.get("response", ""),
            metadata=result.get("metadata", {}),
            success=result.get("success", False),
            error=result.get("error")
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi khi xử lý chat. Vui lòng thử lại sau."
        )