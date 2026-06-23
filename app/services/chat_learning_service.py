# app/services/chat_learning_service.py
"""
Chat Learning Service - Record learning activities from AI Tutor chat
Ghi nhận lesson, practice, quiz từ chat vào DB
"""
from typing import Dict, Any, Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from datetime import datetime, timezone

from app.models.chat_learning_activity import ChatLearningActivity
from app.models.error_log import UserErrorLog
from app.models.exercise_result import ExerciseResult


class ChatLearningService:
    """Service để ghi nhận hoạt động học từ AI Tutor chat"""

    @staticmethod
    async def record_activity(
        db: AsyncSession,
        user_id: UUID,
        session_id: str,
        activity: Optional[Dict[str, Any]],
        curriculum_topic_id: Optional[UUID] = None,
        lesson_order: Optional[int] = None,
    ) -> bool:
        """
        Ghi nhận một hoạt động học từ chat
        
        Args:
            db: Database session
            user_id: User ID
            session_id: Chat session ID
            activity: Activity data từ reflector
                {
                    "type": "lesson|practice|quiz|none",
                    "title": "Past Simple",
                    "custom_topic": "du lịch",
                    "items": [...],  # For practice/quiz
                    "summary": "...",  # For lesson
                    "key_points": [...],  # For lesson
                }
            curriculum_topic_id: Topic ID nếu đang học từ curriculum
            lesson_order: Lesson order nếu đang học từ curriculum
            
        Returns:
            bool: True nếu ghi thành công
        """
        try:
            # Skip if no activity or type is "none"
            if not activity or activity.get("type") == "none":
                logger.debug(f"No activity to record for session {session_id}")
                return False
            
            activity_type = activity.get("type")
            title = activity.get("title", "Untitled")
            custom_topic = activity.get("custom_topic")
            
            # Build content based on activity type
            content = {}
            score = None
            skill_tags = activity.get("skill_tags", [])
            
            if activity_type == "practice":
                # Practice: có câu hỏi + đáp án
                items = activity.get("items", [])
                if items:
                    # Lưu item đầu tiên (hoặc có thể lưu nhiều)
                    content = items[0] if len(items) == 1 else {"items": items}
                    
                    # Calculate score
                    correct_count = sum(1 for item in items if item.get("is_correct", False))
                    score = (correct_count / len(items)) * 100 if items else 0
                    
                    # Log errors for incorrect answers
                    await ChatLearningService._log_practice_errors(
                        db, user_id, items, curriculum_topic_id
                    )
                    
                    # Optional: sync to exercise_results for analytics
                    await ChatLearningService._sync_to_exercise_results(
                        db, user_id, session_id, items, skill_tags
                    )
            
            elif activity_type == "lesson":
                # Lesson: giải thích + key points
                content = {
                    "summary": activity.get("summary", ""),
                    "key_points": activity.get("key_points", []),
                    "examples": activity.get("examples", []),
                }
            
            elif activity_type == "quiz":
                # Quiz: nhiều câu hỏi
                questions = activity.get("items", [])
                correct_count = sum(1 for q in questions if q.get("is_correct", False))
                total = len(questions)
                score = (correct_count / total) * 100 if total > 0 else 0
                
                content = {
                    "questions": questions,
                    "total": total,
                    "correct_count": correct_count,
                }
                
                # Log errors
                await ChatLearningService._log_practice_errors(
                    db, user_id, questions, curriculum_topic_id
                )
            
            elif activity_type == "vocabulary":
                # Vocabulary: danh sách từ vựng được học
                content = {
                    "words": activity.get("words", []),
                    "count": len(activity.get("words", [])),
                }
            
            else:
                logger.warning(f"Unknown activity type: {activity_type}")
                return False
            
            # Create activity record
            new_activity = ChatLearningActivity(
                user_id=user_id,
                chat_session_id=session_id,
                activity_type=activity_type,
                title=title,
                custom_topic=custom_topic,
                curriculum_topic_id=curriculum_topic_id,
                curriculum_lesson_order=lesson_order,
                content=content,
                score=score,
                skill_tags=skill_tags,
                source="ai_tutor_chat",
                created_at=datetime.now(timezone.utc),
            )
            
            db.add(new_activity)
            await db.commit()
            
            logger.info(
                f"✅ Recorded {activity_type} activity '{title}' for user {user_id} "
                f"(session: {session_id[:8]}..., score: {score})"
            )
            return True
            
        except Exception as e:
            logger.exception(f"Failed to record chat activity: {e}")
            await db.rollback()
            return False

    @staticmethod
    async def _log_practice_errors(
        db: AsyncSession,
        user_id: UUID,
        items: List[Dict[str, Any]],
        topic_id: Optional[UUID],
    ):
        """Ghi các câu trả lời sai vào error_logs"""
        try:
            for item in items:
                # Only log when is_correct is explicitly False (not None/null)
                if item.get("is_correct") is False:
                    # Determine error type based on skill_tag
                    skill = item.get("skill_tag", "unknown")
                    
                    # Classify as GRAMMAR_ERROR or VOCABULARY_ERROR
                    vocabulary_skills = ["vocabulary", "vocab", "word", "phrase"]
                    if any(v in skill.lower() for v in vocabulary_skills):
                        error_type = "VOCABULARY_ERROR"
                    else:
                        error_type = "GRAMMAR_ERROR"  # Default to grammar
                    
                    error_log = UserErrorLog(
                        user_id=user_id,
                        error_type=error_type,
                        skill_tag=skill,
                        severity="MEDIUM",
                        user_input=item.get("user_answer", ""),
                        user_answer=item.get("user_answer", ""),
                        correct_form=item.get("correct_answer", ""),
                        question=item.get("question", ""),
                        topic_id=topic_id,
                        explanation=item.get("ai_feedback", ""),
                        created_at=datetime.now(timezone.utc),
                    )
                    db.add(error_log)
            
            await db.commit()
            logger.debug(f"Logged {len([i for i in items if i.get('is_correct') is False])} practice errors")
            
        except Exception as e:
            logger.warning(f"Failed to log practice errors: {e}")
            await db.rollback()

    @staticmethod
    async def _sync_to_exercise_results(
        db: AsyncSession,
        user_id: UUID,
        session_id: str,
        items: List[Dict[str, Any]],
        skill_tags: List[str],
    ):
        """Optional: đồng bộ practice sang exercise_results để analytics dùng chung"""
        try:
            from uuid import uuid4
            
            for item in items:
                # Only sync when is_correct is not None (exercise has been graded)
                if item.get("is_correct") is not None:
                    # Get skill from item or use first skill_tag
                    skill = item.get("skill_tag") or (skill_tags[0] if skill_tags else "unknown")
                    
                    exercise_result = ExerciseResult(
                        id=uuid4(),
                        user_id=user_id,
                        session_id=None,  # We don't have learning_session_id from chat
                        exercise_id=None,  # AI-generated, no fixed ID
                        exercise_type="chat_practice",
                        user_answer=item.get("user_answer", ""),
                        expected_answer=item.get("correct_answer", ""),
                        is_correct=item.get("is_correct", False),
                        skill_tag=skill,
                        difficulty="medium",
                        created_at=datetime.now(timezone.utc),
                    )
                    db.add(exercise_result)
            
            await db.commit()
            logger.debug(f"Synced {len([i for i in items if i.get('is_correct') is not None])} items to exercise_results")
            
        except Exception as e:
            logger.warning(f"Failed to sync to exercise_results: {e}")
            await db.rollback()

    @staticmethod
    async def get_user_chat_activities(
        db: AsyncSession,
        user_id: UUID,
        days: int = 30,
        activity_type: Optional[str] = None,
    ) -> List[ChatLearningActivity]:
        """Lấy danh sách hoạt động học từ chat của user"""
        from sqlalchemy import select, and_
        from datetime import timedelta
        
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            query = select(ChatLearningActivity).where(
                and_(
                    ChatLearningActivity.user_id == user_id,
                    ChatLearningActivity.created_at >= cutoff_date,
                )
            )
            
            if activity_type:
                query = query.where(ChatLearningActivity.activity_type == activity_type)
            
            query = query.order_by(ChatLearningActivity.created_at.desc())
            
            result = await db.execute(query)
            activities = result.scalars().all()
            
            return list(activities)
            
        except Exception as e:
            logger.exception(f"Failed to get chat activities: {e}")
            return []

    @staticmethod
    async def get_activity_summary(
        db: AsyncSession,
        user_id: UUID,
        days: int = 30,
    ) -> Dict[str, Any]:
        """Lấy tóm tắt hoạt động học từ chat"""
        from sqlalchemy import select, func, and_
        from datetime import timedelta
        
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            # Count by activity type
            result = await db.execute(
                select(
                    ChatLearningActivity.activity_type,
                    func.count(ChatLearningActivity.id).label("count"),
                    func.avg(ChatLearningActivity.score).label("avg_score"),
                )
                .where(
                    and_(
                        ChatLearningActivity.user_id == user_id,
                        ChatLearningActivity.created_at >= cutoff_date,
                    )
                )
                .group_by(ChatLearningActivity.activity_type)
            )
            
            summary = {}
            for row in result:
                summary[row.activity_type] = {
                    "count": row.count,
                    "avg_score": round(row.avg_score, 1) if row.avg_score else None,
                }
            
            return summary
            
        except Exception as e:
            logger.exception(f"Failed to get activity summary: {e}")
            return {}
