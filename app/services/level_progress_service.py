# app/services/level_progress_service.py
"""
B5: Unified Level-Up Eligibility Service
Single source of truth for level-up rules
"""

from typing import Dict, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from loguru import logger

from app.models.user_profile import UserProfile
from app.models.user_topic_progress import UserTopicProgress
from app.models.topic import Topic


class LevelProgressService:
    """Unified service for checking level-up eligibility"""
    
    # Level progression map
    LEVEL_PROGRESSION = {
        "A1": "A2",
        "A2": "B1",
        "B1": "B2",
        "B2": "C1",
        "C1": "C2",
    }
    
    # Requirements for level-up
    MIN_TOPICS_COMPLETED_PERCENT = 75  # 75% of topics in current level
    MIN_QUIZ_AVG_SCORE = 70  # 70% average quiz score
    
    async def check_eligibility(
        self, 
        user_id: UUID, 
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Check if user is eligible for level-up test
        
        Returns:
            {
                "eligible": bool,
                "current_level": str,
                "next_level": str | None,
                "requirements": {
                    "topics_completed": str,  # "3/4"
                    "topics_completed_percent": float,  # 75.0
                    "quiz_avg_score": float,  # 85.5
                    "meets_topic_requirement": bool,
                    "meets_quiz_requirement": bool
                },
                "message": str
            }
        """
        try:
            # Get user profile
            result = await db.execute(
                select(UserProfile).where(UserProfile.user_id == user_id)
            )
            profile = result.scalar_one_or_none()
            
            if not profile:
                return {
                    "eligible": False,
                    "current_level": None,
                    "next_level": None,
                    "requirements": {},
                    "message": "Không tìm thấy profile"
                }
            
            current_level = profile.current_level
            next_level = self.LEVEL_PROGRESSION.get(current_level)
            
            if not next_level:
                return {
                    "eligible": False,
                    "current_level": current_level,
                    "next_level": None,
                    "requirements": {},
                    "message": f"Bạn đã đạt level cao nhất ({current_level})"
                }
            
            # Count topics in current level
            total_topics_result = await db.execute(
                select(func.count(Topic.id)).where(Topic.level == current_level)
            )
            total_topics = total_topics_result.scalar() or 0
            
            if total_topics == 0:
                return {
                    "eligible": False,
                    "current_level": current_level,
                    "next_level": next_level,
                    "requirements": {},
                    "message": "Không có chủ đề nào cho level này"
                }
            
            # Count completed topics for this level
            completed_topics_result = await db.execute(
                select(func.count(UserTopicProgress.topic_id))
                .join(Topic, UserTopicProgress.topic_id == Topic.id)
                .where(
                    UserTopicProgress.user_id == user_id,
                    UserTopicProgress.status == "completed",
                    Topic.level == current_level
                )
            )
            completed_topics = completed_topics_result.scalar() or 0
            
            # Calculate average quiz score for current level
            quiz_avg_result = await db.execute(
                select(func.avg(UserTopicProgress.quiz_score))
                .join(Topic, UserTopicProgress.topic_id == Topic.id)
                .where(
                    UserTopicProgress.user_id == user_id,
                    UserTopicProgress.quiz_score.isnot(None),
                    Topic.level == current_level
                )
            )
            quiz_avg_score = quiz_avg_result.scalar() or 0.0
            
            # Calculate completion percentage
            topics_completed_percent = (completed_topics / total_topics * 100) if total_topics > 0 else 0
            
            # Check requirements
            meets_topic_requirement = topics_completed_percent >= self.MIN_TOPICS_COMPLETED_PERCENT
            meets_quiz_requirement = quiz_avg_score >= self.MIN_QUIZ_AVG_SCORE
            
            eligible = meets_topic_requirement and meets_quiz_requirement
            
            # Build message
            if eligible:
                message = f"🎉 Bạn đủ điều kiện thi lên {next_level}!"
            else:
                missing = []
                if not meets_topic_requirement:
                    missing.append(f"hoàn thành thêm {int(self.MIN_TOPICS_COMPLETED_PERCENT - topics_completed_percent)}% chủ đề")
                if not meets_quiz_requirement:
                    missing.append(f"tăng điểm quiz lên {self.MIN_QUIZ_AVG_SCORE}%")
                message = f"💪 Cần {' và '.join(missing)} để đủ điều kiện thi lên level"
            
            return {
                "eligible": eligible,
                "current_level": current_level,
                "next_level": next_level,
                "requirements": {
                    "topics_completed": f"{completed_topics}/{total_topics}",
                    "topics_completed_percent": round(topics_completed_percent, 1),
                    "quiz_avg_score": round(quiz_avg_score, 1),
                    "meets_topic_requirement": meets_topic_requirement,
                    "meets_quiz_requirement": meets_quiz_requirement,
                },
                "message": message
            }
            
        except Exception as e:
            logger.exception(f"Error checking level-up eligibility for user {user_id}: {e}")
            return {
                "eligible": False,
                "current_level": None,
                "next_level": None,
                "requirements": {},
                "message": "Lỗi khi kiểm tra điều kiện"
            }
