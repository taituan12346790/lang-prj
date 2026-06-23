#!/usr/bin/env python
"""
Script để seed dữ liệu topics vào database
Chạy: python seed_database.py
"""
import asyncio
from sqlalchemy import select, func
from loguru import logger

from app.core.database import AsyncSessionLocal, async_engine, Base
from app.models.topic import Topic
from app.models.lesson import Lesson
from app.data.topics_data import get_all_topics


async def create_tables():
    """Tạo tất cả tables nếu chưa có"""
    logger.info("🔧 Creating database tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.success("✅ Tables created/verified")


async def seed_topics():
    """Seed topics vào database"""
    async with AsyncSessionLocal() as db:
        # Kiểm tra xem đã có topics chưa
        result = await db.execute(select(func.count()).select_from(Topic))
        count = result.scalar()
        
        if count and count > 0:
            logger.info(f"ℹ️  Database already has {count} topics. Skipping seed.")
            return
        
        logger.info("🌱 Seeding topics into database...")
        topics_data = get_all_topics()
        
        total_lessons = 0
        for i, t_data in enumerate(topics_data, 1):
            lessons_data = t_data.pop("lessons", [])
            
            # Tạo topic
            topic = Topic(**t_data)
            db.add(topic)
            await db.flush()  # Lấy topic.id
            
            # Tạo lessons cho topic này
            for l_data in lessons_data:
                lesson = Lesson(topic_id=topic.id, **l_data)
                db.add(lesson)
                total_lessons += 1
            
            # Log progress
            if i % 10 == 0:
                logger.info(f"   Seeded {i}/{len(topics_data)} topics...")
        
        await db.commit()
        logger.success(f"✅ Successfully seeded {len(topics_data)} topics with {total_lessons} lessons")
        
        # Verify
        result = await db.execute(select(func.count()).select_from(Topic))
        final_count = result.scalar()
        logger.info(f"📊 Total topics in database: {final_count}")


async def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("🚀 DATABASE SEEDING SCRIPT")
    logger.info("=" * 60)
    
    try:
        # Step 1: Create tables
        await create_tables()
        
        # Step 2: Seed topics
        await seed_topics()
        
        logger.info("=" * 60)
        logger.success("✅ SEEDING COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Error during seeding: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
