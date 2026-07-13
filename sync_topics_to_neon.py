"""
Script để đồng bộ topics_data.py lên Neon Tech database
Cập nhật tất cả 20 topics A1 với Vietnamese translations mới
"""

import asyncio
import os
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import topics data
try:
    from app.data.topics_data import A1_TOPICS
    print(f"✅ Đã load {len(A1_TOPICS)} topics từ topics_data.py")
except Exception as e:
    print(f"❌ Không thể load topics_data: {e}")
    sys.exit(1)

# Database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://neondb_owner:npg_TBSbNV0XK4dZ@ep-rapid-sea-ao7qnzl8.c-2.ap-southeast-1.aws.neon.tech/neondb?ssl=require')

async def sync_topics_to_database():
    """Sync all A1 topics from topics_data.py to Neon database"""
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("🚀 Bắt đầu đồng bộ topics...")
        
        updated_count = 0
        error_count = 0
        
        for topic_data in A1_TOPICS:
            try:
                level = topic_data['level']
                order = topic_data['order']
                name = topic_data['name']
                name_vi = topic_data['name_vi']
                
                print(f"\n📚 Đang xử lý Topic {order}: {name}")
                
                # 1. Get topic_id from database
                result = await session.execute(
                    text("""
                        SELECT id FROM topics 
                        WHERE level = :level AND "order" = :order
                    """),
                    {"level": level, "order": order}
                )
                topic_row = result.fetchone()
                
                if not topic_row:
                    print(f"❌ Không tìm thấy Topic {order} trong database!")
                    error_count += 1
                    continue
                
                topic_id = topic_row[0]
                
                # 2. Update topic info
                await session.execute(
                    text("""
                        UPDATE topics
                        SET name = :name,
                            name_vi = :name_vi,
                            description = :description,
                            description_vi = :description_vi,
                            estimated_minutes = :estimated_minutes
                        WHERE id = :topic_id
                    """),
                    {
                        "topic_id": str(topic_id),
                        "name": name,
                        "name_vi": name_vi,
                        "description": topic_data.get('description', ''),
                        "description_vi": topic_data.get('description_vi', ''),
                        "estimated_minutes": topic_data.get('estimated_minutes', 30)
                    }
                )
                
                # 3. Update lessons (Grammar, Vocabulary, Practice, Quiz)
                lessons = topic_data.get('lessons', [])
                
                for lesson_data in lessons:
                    lesson_order = lesson_data['order']
                    lesson_type = lesson_data['lesson_type']
                    
                    # Get lesson_id
                    result = await session.execute(
                        text("""
                            SELECT id FROM lessons
                            WHERE topic_id = :topic_id 
                            AND "order" = :order
                            AND lesson_type = :lesson_type
                        """),
                        {
                            "topic_id": str(topic_id),
                            "order": lesson_order,
                            "lesson_type": lesson_type
                        }
                    )
                    lesson_row = result.fetchone()
                    
                    if lesson_row:
                        lesson_id = lesson_row[0]
                        
                        # Update lesson
                        await session.execute(
                            text("""
                                UPDATE lessons
                                SET title = :title,
                                    title_vi = :title_vi,
                                    content = CAST(:content AS jsonb)
                                WHERE id = :lesson_id
                            """),
                            {
                                "lesson_id": str(lesson_id),
                                "title": lesson_data.get('title', ''),
                                "title_vi": lesson_data.get('title_vi', ''),
                                "content": json.dumps(lesson_data.get('content', {}))
                            }
                        )
                        print(f"  ✅ Updated {lesson_type} (order {lesson_order})")
                    else:
                        print(f"  ⚠️ Lesson not found: {lesson_type} (order {lesson_order})")
                
                updated_count += 1
                print(f"✅ Hoàn thành Topic {order}: {name}")
                
            except Exception as e:
                print(f"❌ Lỗi khi xử lý Topic {order}: {e}")
                error_count += 1
                continue
        
        # Commit all changes
        await session.commit()
        print(f"\n🎉 Hoàn thành đồng bộ!")
        print(f"✅ Đã cập nhật: {updated_count} topics")
        print(f"❌ Lỗi: {error_count} topics")
        
        # 4. Update writing lesson for Topic 20 (Animals & Pets)
        print("\n📝 Cập nhật writing lesson cho Topic 20...")
        result = await session.execute(
            text("""
                SELECT id FROM topics 
                WHERE level = 'A1' AND "order" = 20
            """)
        )
        topic_20 = result.fetchone()
        
        if topic_20:
            topic_20_id = topic_20[0]
            
            writing_content = {
                "prompt": "Write a paragraph about your pet or your favorite animal.",
                "prompt_vi": "Viết một đoạn văn về thú cưng của bạn hoặc động vật yêu thích của bạn.",
                "min_words": 40,
                "tips": [
                    "Mention what animal it is (dog, cat, rabbit, etc.)",
                    "Describe what it looks like (color, size)",
                    "Use 'I have a...' or 'My favorite animal is...'",
                    "Say what the animal can do (run, jump, swim, fly)",
                    "Explain why you like this animal"
                ],
                "example": {
                    "title": "My Pet Dog",
                    "text": "I have a dog. His name is Lucky. He is 3 years old. Lucky is a big brown dog. He has long ears and a short tail. He is very friendly and playful. Lucky can run very fast. He likes to play with balls. He eats dog food and meat. I love Lucky very much because he is my best friend.",
                    "translation": "Tôi có một con chó. Tên nó là Lucky. Nó 3 tuổi. Lucky là một con chó lớn màu nâu. Nó có đôi tai dài và cái đuôi ngắn. Nó rất thân thiện và hay nghịch. Lucky có thể chạy rất nhanh. Nó thích chơi với bóng. Nó ăn thức ăn cho chó và thịt. Tôi yêu Lucky rất nhiều vì nó là người bạn tốt nhất của tôi."
                }
            }
            
            result = await session.execute(
                text("""
                    UPDATE lessons
                    SET title = 'Writing: Animals & Pets',
                        title_vi = 'Viết: Động vật & Thú cưng',
                        content = CAST(:content AS jsonb)
                    WHERE topic_id = :topic_id 
                    AND lesson_type = 'writing'
                    RETURNING id
                """),
                {
                    "content": json.dumps(writing_content),
                    "topic_id": str(topic_20_id)
                }
            )
            
            if result.fetchone():
                await session.commit()
                print("✅ Đã cập nhật writing lesson cho Topic 20!")
            else:
                print("⚠️ Không tìm thấy writing lesson cho Topic 20")
        
    await engine.dispose()
    print("\n✅ Đồng bộ hoàn tất!")

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 ĐỒNG BỘ TOPICS LÊN NEON TECH DATABASE")
    print("=" * 60)
    asyncio.run(sync_topics_to_database())
