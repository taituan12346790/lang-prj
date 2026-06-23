from uuid import UUID
from app.services.level_service import LevelService
from app.services.level_service_unified import LevelServiceUnified
from app.schemas.test import (
    PlacementTestRequest,
    PlacementTestResponse,
    LevelUpTestRequest,
    LevelUpTestResult
)
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger


class TestService:
    def __init__(self):
        self.level_service = LevelService()
        self.level_service_unified = LevelServiceUnified()

    async def take_placement_test(
        self,
        user_id: str,
        request: PlacementTestRequest,
        db: AsyncSession
    ) -> PlacementTestResponse:
        return await self.level_service.placement_test(
            user_id=user_id,
            answers=request.answers,
            db=db
        )

    async def take_level_up_test(
        self,
        user_id: str,
        request: LevelUpTestRequest,
        db: AsyncSession
    ) -> LevelUpTestResult:
        # Get test result
        result = await self.level_service.level_up_test(
            user_id=user_id,
            test_type=request.test_type,
            current_level=request.current_level,
            num_questions=request.num_questions,
            answers=request.answers,
            db=db
        )
        
        # If passed, use unified service to promote user
        if result.passed:
            try:
                promotion_result = await self.level_service_unified.handle_test_completion(
                    user_id=UUID(user_id),
                    current_level=request.current_level.value,
                    test_score=result.score,
                    db=db
                )
                
                # Update result with promotion details
                if promotion_result.get("promoted"):
                    logger.info(
                        f"User {user_id} promoted to {promotion_result.get('new_level')}"
                    )
                    result.new_level = promotion_result.get("new_level")
                    result.message = promotion_result.get("message")
            except Exception as e:
                logger.exception(f"Error promoting user {user_id}: {e}")
                # Continue with normal result if promotion fails
        
        return result
