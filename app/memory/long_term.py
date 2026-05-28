# app/memory/long_term_memory.py
from typing import Dict, Any
from datetime import datetime, timezone
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user_profile import UserProfile


class LongTermMemory:
    """Long-term Memory sử dụng PostgreSQL"""

    async def load(self, user_id: str, db: AsyncSession) -> UserProfile:
        """Load UserProfile từ database, tạo mới nếu chưa có"""
        fallback_profile = UserProfile(user_id=user_id)  # Khởi tạo fallback trước

        try:
            result = await db.execute(
                select(UserProfile).where(UserProfile.user_id == user_id)
            )
            profile = result.scalar_one_or_none()

            if not profile:
                profile = UserProfile(user_id=user_id)
                db.add(profile)
                await db.commit()
                await db.refresh(profile)

            return profile

        except Exception as e:
            logger.exception(f"Error loading long-term memory for {user_id}: {e}")
            return fallback_profile

    async def save(self, profile: UserProfile, db: AsyncSession) -> UserProfile:
        """Save/Update profile"""
        try:
            profile = await db.merge(profile)   # merge trả về instance mới
            await db.commit()
            await db.refresh(profile)
            return profile
        except Exception as e:
            logger.exception(f"Error saving long-term memory for {profile.user_id}: {e}")
            await db.rollback()
            raise

    async def update_from_analysis(
        self,
        user_id: str,
        analysis: Dict[str, Any],
        db: AsyncSession
    ) -> UserProfile:
        """Cập nhật profile từ reflection/analysis"""
        profile = await self.load(user_id, db)

        try:
            # Weak & Strong skills
            for skill in analysis.get("weak_skills", []):
                profile.weak_skills[skill] = profile.weak_skills.get(skill, 0) + 1

            for skill in analysis.get("strong_skills", []):
                profile.strong_skills[skill] = profile.strong_skills.get(skill, 0) + 1

            # Lists (MutableList sẽ tự detect thay đổi)
            for item in analysis.get("interests", []):
                if item not in profile.interests:
                    profile.interests.append(item)

            for item in analysis.get("goals", []):
                if item not in profile.goals:
                    profile.goals.append(item)

            for item in analysis.get("preferred_topics", []):
                if item not in profile.preferred_topics:
                    profile.preferred_topics.append(item)

            if analysis.get("learning_style"):
                profile.learning_style = analysis["learning_style"]

            if analysis.get("detected_level"):
                profile.current_level = analysis["detected_level"]

            profile.total_sessions = (profile.total_sessions or 0) + 1
            profile.last_active = datetime.now(timezone.utc)

            profile = await self.save(profile, db)
            return profile

        except Exception as e:
            logger.exception(f"Error updating long-term from analysis for {user_id}: {e}")
            return profile