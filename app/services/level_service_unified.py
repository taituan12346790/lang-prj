# app/services/level_service_unified.py
"""
Unified Level Eligibility Service
Single source of truth for all level-up eligibility checks
Rule: 75% topics completed AND avg quiz score ≥70
"""

from typing import Dict, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.models.user import User
from app.models.user_topic_progress import UserTopicProgress
from app.models.exercise_result import ExerciseResult
from app.schemas.test import Level


class LevelServiceUnified:
    """Unified eligibility service for all level-up checks"""

    @staticmethod
    async def get_eligibility(
        user_id: UUID,
        current_level: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Check if user is eligible for level-up test
        Single rule: 75% topics completed AND avg quiz ≥70
        
        Returns:
            {
                "can_level_up": bool,
                "message": str,
                "completion_percentage": float,
                "average_quiz_score": float,
                "completed_topics": int,
                "total_topics": int,
                "next_level": str
            }
        """
        try:
            # Get all topics for current level
            progress_result = await db.execute(
                select(UserTopicProgress).where(
                    UserTopicProgress.user_id == user_id,
                )
            )
            all_topics = progress_result.scalars().all()

            # Filter by current level
            current_topics = [
                t for t in all_topics
                if t.topic and t.topic.level == current_level
            ]

            if not current_topics:
                logger.warning(
                    f"No topics found for user {user_id} at level {current_level}"
                )
                return {
                    "can_level_up": False,
                    "message": "No topics found for this level",
                    "completion_percentage": 0,
                    "average_quiz_score": None,
                    "completed_topics": 0,
                    "total_topics": 0,
                    "next_level": None,
                }

            total_topics = len(current_topics)
            completed_topics = sum(
                1 for t in current_topics
                if t.lesson_completed >= 5 and t.quiz_score and t.quiz_score >= 70
            )
            completion_pct = (completed_topics / total_topics * 100) if total_topics > 0 else 0

            # Calculate average quiz score for completed topics
            quiz_scores = [
                t.quiz_score
                for t in current_topics
                if t.quiz_score is not None
            ]
            avg_score = round(sum(quiz_scores) / len(quiz_scores), 1) if quiz_scores else None

            # Unified eligibility rule: 75% topics completed AND avg score ≥70
            can_level_up = (
                completion_pct >= 75
                and avg_score is not None
                and avg_score >= 70
                and current_level != "C2"
            )

            # Determine next level
            level_map = {
                "A1": "A2",
                "A2": "B1",
                "B1": "B2",
                "B2": "C1",
                "C1": "C2",
                "C2": None,
            }
            next_level = level_map.get(current_level)

            # Build message
            if can_level_up:
                message = "🎉 Bạn đủ điều kiện làm bài kiểm tra nâng cấp!"
            else:
                needed_topics = max(0, round(total_topics * 0.75) - completed_topics)
                if needed_topics > 0:
                    message = f"Hoàn thành {needed_topics} chủ đề nữa để mở khóa Level-Up Test."
                elif avg_score is None or avg_score < 70:
                    message = f"Điểm trung bình cần ≥70. Hiện tại: {avg_score or 'N/A'}"
                else:
                    message = "Tiếp tục học để nâng cấp."

            return {
                "can_level_up": can_level_up,
                "message": message,
                "completion_percentage": round(completion_pct, 1),
                "average_quiz_score": avg_score,
                "completed_topics": completed_topics,
                "total_topics": total_topics,
                "next_level": next_level,
                "current_level": current_level,
            }

        except Exception as e:
            logger.exception(f"Error checking eligibility: {e}")
            raise

    @staticmethod
    async def handle_test_completion(
        user_id: UUID,
        current_level: str,
        test_score: float,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Handle level-up test completion
        If passed (≥75%), promote user to next level
        
        Args:
            user_id: User ID
            current_level: Current level (e.g., "A1")
            test_score: Test score (0-100)
            db: Database session
            
        Returns:
            {
                "passed": bool,
                "promoted": bool,
                "new_level": str or None,
                "message": str
            }
        """
        try:
            # Check if test passed (≥75%)
            passed = test_score >= 75

            if not passed:
                return {
                    "passed": False,
                    "promoted": False,
                    "new_level": None,
                    "message": f"Score {test_score}% không đủ. Cần ≥75% để nâng cấp.",
                }

            # Get user and promote
            user_result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = user_result.scalar_one_or_none()

            if not user:
                logger.error(f"User {user_id} not found")
                return {
                    "passed": True,
                    "promoted": False,
                    "new_level": None,
                    "message": "User not found",
                }

            # Determine next level
            level_map = {
                "A1": "A2",
                "A2": "B1",
                "B1": "B2",
                "B2": "C1",
                "C1": "C2",
                "C2": None,
            }
            new_level = level_map.get(current_level)

            if new_level is None:
                return {
                    "passed": True,
                    "promoted": False,
                    "new_level": None,
                    "message": f"Bạn đã ở level cao nhất (C2)!",
                }

            # Promote user
            user.current_level = new_level
            await db.commit()

            logger.info(f"User {user_id} promoted from {current_level} to {new_level}")

            return {
                "passed": True,
                "promoted": True,
                "new_level": new_level,
                "message": f"🎉 Chúc mừng! Bạn đã được nâng lên level {new_level}!",
            }

        except Exception as e:
            logger.exception(f"Error handling test completion: {e}")
            raise
