"""Manually add writing lessons to all topics"""
import asyncio
import json
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

async def add_writing_lessons():
    DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_TBSbNV0XK4dZ@ep-rapid-sea-ao7qnzl8.c-2.ap-southeast-1.aws.neon.tech/neondb?ssl=require"
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 1. Update quiz lessons from order=4 to order=5
        result = await session.execute(
            text("UPDATE lessons SET \"order\" = 5 WHERE lesson_type IN ('quiz', 'kiểm tra') AND \"order\" = 4")
        )
        print(f"✅ Updated {result.rowcount} quiz lessons from order=4 to order=5")
        
        # 2. Get all topics
        result = await session.execute(
            text("SELECT id, level, name, name_vi FROM topics ORDER BY level, \"order\"")
        )
        topics = result.all()
        print(f"\n📚 Found {len(topics)} topics\n")
        
        # 3. Add writing lesson for each topic
        for topic in topics:
            topic_id, level, name, name_vi = topic
            
            # Check if writing lesson already exists
            check = await session.execute(
                text("SELECT id FROM lessons WHERE topic_id = :topic_id AND \"order\" = 4"),
                {"topic_id": topic_id}
            )
            if check.first():
                print(f"   ⏭️  {name}: Writing lesson already exists")
                continue
            
            # Generate content
            level_word_counts = {"A1": 40, "A2": 50, "B1": 80, "B2": 120, "C1": 150, "C2": 200}
            min_words = level_word_counts.get(level, 50)
            
            content = {
                "prompt": f"Write a short paragraph about: {name}",
                "prompt_vi": f"Viết một đoạn văn ngắn về: {name_vi or name}",
                "min_words": min_words,
                "tips": [
                    f"Use vocabulary and grammar from the {name} lesson",
                    "Write clear and simple sentences",
                    "Check your spelling and grammar before submitting",
                    f"Write at least {min_words} words"
                ]
            }
            
            # Insert writing lesson
            await session.execute(
                text("""
                    INSERT INTO lessons (id, topic_id, "order", lesson_type, title, title_vi, content)
                    VALUES (:id, :topic_id, :order, :lesson_type, :title, :title_vi, CAST(:content AS jsonb))
                """),
                {
                    "id": str(uuid.uuid4()),
                    "topic_id": str(topic_id),
                    "order": 4,
                    "lesson_type": "writing",
                    "title": f"Writing: {name}",
                    "title_vi": f"Viết: {name_vi or name}",
                    "content": json.dumps(content)
                }
            )
            print(f"   ✅ {name}: Added writing lesson")
        
        await session.commit()
        print(f"\n✅ Completed! Added writing lessons to {len(topics)} topics")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(add_writing_lessons())
