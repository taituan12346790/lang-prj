from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.test import PlacementTestRequest, PlacementTestResponse, LevelUpTestRequest, LevelUpTestResult
from app.models.user import User
from app.services.test_service import TestService
from loguru import logger

router = APIRouter(prefix="/api/test", tags=["Test & Level"])
test_service = TestService()


@router.post("/placement", response_model=PlacementTestResponse)
async def placement_test(
    request: PlacementTestRequest, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    """
    Placement Test - Assess user's current English level
    
    - Takes answers to placement questions
    - Returns estimated CEFR level (A1-C2)
    - Identifies strengths and weaknesses
    - Provides learning recommendations
    """
    try:
        logger.info(f"[PlacementTest] User {current_user.id} started")
        
        result = await test_service.take_placement_test(
            user_id=str(current_user.id),
            request=request,
            db=db
        )
        
        logger.success(f"[PlacementTest] User {current_user.id} scored {result.score}%")
        return result
        
    except Exception as e:
        logger.exception(f"Placement test error for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process placement test. Please try again."
        )


@router.post("/level-up", response_model=LevelUpTestResult)
async def level_up_test(
    request: LevelUpTestRequest, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    """
    Level-Up Test - Assess if user is ready for next CEFR level
    
    - Takes level-specific questions
    - Checks against current level
    - Determines pass/fail status
    - Suggests new level if passed
    - Identifies areas needing improvement
    """
    try:
        logger.info(
            f"[LevelUpTest] User {current_user.id} attempting "
            f"level-up from {request.current_level}"
        )
        
        result = await test_service.take_level_up_test(
            user_id=str(current_user.id),
            request=request,
            db=db
        )
        
        status = "passed ✅" if result.passed else "failed ❌"
        logger.info(
            f"[LevelUpTest] User {current_user.id} {status} | Score: {result.score}%"
        )
        return result
        
    except Exception as e:
        logger.exception(f"Level-up test error for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process level-up test. Please try again."
        )