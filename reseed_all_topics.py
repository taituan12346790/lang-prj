#!/usr/bin/env python
"""
Script để XÓA topics cũ và SEED LẠI tất cả 190 topics (A1-C2)
Chạy: python reseed_all_topics.py
"""
import asyncio
from sqlalchemy import select, func, delete
from loguru import logger

from app.core.database import AsyncSessionLocal, async_engine, Base
from app.models.topic import Topic
from app.models.lesson import Lesson
from app.models.user_topic_progress import UserTopicProgress
from app.data.topics_data import get_all_topics


async def clear_old_data():
    """Xóa tất cả topics và lessons cũ"""
    async with AsyncSessionLocal() as db:
        logger.warning("⚠️  Clearing old topics and lessons...")
        
        # Xóa user progress trước (foreign key)
        await db.execute(delete(UserTopicProgress))
        
        # Xóa lessons
        result = await db.execute(select(func.count()).select_from(Lesson))
        lesson_count = result.scalar() or 0
        await db.execute(delete(Lesson))
        
        # Xóa topics
        result = await db.execute(select(func.count()).select_from(Topic))
        topic_count = result.scalar() or 0
        await db.execute(delete(Topic))
        
        await db.commit()
        logger.info(f"   Deleted {topic_count} topics and {lesson_count} lessons")


async def seed_all_topics():
    """Seed TẤT CẢ 190 topics (A1-C2) vào database"""
    async with AsyncSessionLocal() as db:
        logger.info("🌱 Seeding ALL 190 topics (A1-C2) into database...")
        topics_data = get_all_topics()
        
        logger.info(f"   Total topics to seed: {len(topics_data)}")
        
        total_lessons = 0
        level_counts = {}
        
        for i, t_data in enumerate(topics_data, 1):
            lessons_data = t_data.pop("lessons", [])
            level = t_data.get("level", "??")
            
            # Tạo topic
            topic = Topic(**t_data)
            db.add(topic)
            await db.flush()  # Lấy topic.id
            
            # Đếm topics theo level
            level_counts[level] = level_counts.get(level, 0) + 1
            
            # Tạo lessons cho topic này
            for l_data in lessons_data:
                lesson = Lesson(topic_id=topic.id, **l_data)
                db.add(lesson)
                total_lessons += 1
            
            # Log progress mỗi 20 topics
            if i % 20 == 0:
                logger.info(f"   Progress: {i}/{len(topics_data)} topics...")
        
        await db.commit()
        
        logger.success(f"✅ Successfully seeded {len(topics_data)} topics with {total_lessons} lessons")
        logger.info("📊 Topics by level:")
        for level in sorted(level_counts.keys()):
            logger.info(f"   {level}: {level_counts[level]} topics")
        
        # Verify
        result = await db.execute(select(func.count()).select_from(Topic))
        final_count = result.scalar()
        
        result = await db.execute(select(func.count()).select_from(Lesson))
        final_lessons = result.scalar()
        
        logger.info(f"📊 Final count: {final_count} topics, {final_lessons} lessons in database")


async def main():
    """Main function"""
    logger.info("=" * 70)
    logger.info("🔄 RESEED ALL TOPICS (190 TOPICS FROM A1 TO C2)")
    logger.info("=" * 70)
    
    # Confirm
    logger.warning("⚠️  This will DELETE all existing topics and reseed 190 topics!")
    logger.info("Press Ctrl+C to cancel, or wait 3 seconds to continue...")
    await asyncio.sleep(3)
    
    try:
        # Step 1: Clear old data
        await clear_old_data()
        
        # Step 2: Seed all topics
        await seed_all_topics()
        
        logger.info("=" * 70)
        logger.success("✅ RESEED COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)
        logger.info("📚 You can now use the application with all 190 topics!")
        
    except Exception as e:
        logger.error(f"❌ Error during reseeding: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
