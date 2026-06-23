from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.profile import UserProfileResponse, UserProfileUpdate
from app.models.user import User
from app.models.user_profile import UserProfile


def _build_profile_response(profile: UserProfile, user: User) -> UserProfileResponse:
    return UserProfileResponse(
        user_id=profile.user_id,
        email=user.email,
        full_name=user.full_name,
        native_language=profile.native_language,
        target_language=profile.target_language,
        current_level=profile.current_level,
        placement_score=profile.placement_score or 0.0,
        learning_style=profile.learning_style,
        interests=profile.interests or [],
        goals=profile.goals or [],
        preferred_topics=profile.preferred_topics or [],
        total_sessions=profile.total_sessions or 0,
        streak_days=profile.streak_days or 0,
        last_active=profile.last_active
    )


router = APIRouter(prefix="/api/profile", tags=["Profile"])

@router.get("/", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    return _build_profile_response(profile, current_user)

@router.put("/", response_model=UserProfileResponse)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    update_dict = profile_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if value is not None:
            setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return _build_profile_response(profile, current_user)


@router.post("/onboarding")
async def complete_onboarding(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Complete onboarding for OAuth users who skipped initial setup"""
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update profile with onboarding data
    update_dict = profile_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if value is not None:
            setattr(profile, key, value)
    
    # Mark onboarding as completed
    profile.onboarding_completed = True
    
    await db.commit()
    await db.refresh(profile)
    
    return {
        "success": True,
        "message": "Onboarding completed successfully",
        "profile": _build_profile_response(profile, current_user)
    }