"""Test script to verify learning context is loaded properly"""
import asyncio
import sys
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.services.topic_service import TopicService
from app.services.learning_service import LearningService
from loguru import logger

async def test_context():
    """Test learning context loading"""
    async for db in get_db():
        try:
            # Get first user
            result = await db.execute(select(User).limit(1))
            user = result.scalar_one_or_none()
            
            if not user:
                logger.error("No users found in database")
                return
            
            logger.info(f"Testing with user: {user.email}")
            
            # Get user profile
            profile_result = await db.execute(
                select(UserProfile).where(UserProfile.user_id == user.id)
            )
            profile = profile_result.scalar_one_or_none()
            
            if not profile:
                logger.error(f"No profile found for user {user.id}")
                return
            
            logger.info(f"Profile: level={profile.current_level}, active_topic_id={profile.active_topic_id}, active_lesson={profile.active_lesson_order}")
            
            # Test topic service get_learning_context
            topic_service = TopicService()
            context = await topic_service.get_learning_context(user.id, db)
            
            if context:
                logger.info("✅ TopicService.get_learning_context returned:")
                logger.info(f"   Topic: {context.topic_name_vi}")
                logger.info(f"   Lesson: {context.lesson_title}")
                logger.info(f"   Grammar: {context.grammar_focus}")
            else:
                logger.warning("⚠️ TopicService.get_learning_context returned None")
            
            # Test learning service _build_learning_context_dict
            learning_service = LearningService()
            context_dict = await learning_service._build_learning_context_dict(db, str(user.id))
            
            if context_dict:
                logger.info("✅ LearningService._build_learning_context_dict returned:")
                logger.info(f"   Topic: {context_dict.get('topic_name_vi')}")
                logger.info(f"   Lesson: {context_dict.get('lesson_title')}")
                logger.info(f"   Grammar: {context_dict.get('grammar_focus')}")
            else:
                logger.warning("⚠️ LearningService._build_learning_context_dict returned None")
            
        except Exception as e:
            logger.exception(f"Error testing context: {e}")
        finally:
            break

if __name__ == "__main__":
    asyncio.run(test_context())
