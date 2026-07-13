"""
Quick update - Chỉ cập nhật từng topic một để tránh timeout
Chạy: python quick_update_db.py <topic_number>
Ví dụ: python quick_update_db.py 20
"""

import asyncio
import sys
from app.core.database import AsyncSessionLocal
from sqlalchemy import text
import json

sys.path.insert(0, '.')
from app.data.topics_data import A1_TOPICS

async def quick_update(topic_order: int):
    """Update một topic cụ thể"""
    
    # Find topic data
    topic_data = None
    for t in A1_TOPICS:
        if t['order'] == topic_order:
            topic_data = t
            break
    
    if not topic_data:
        print(f"❌ Không tìm thấy Topic {topic_order} trong topics_data.py")
        return False
    
    print(f"📚 Cập nhật Topic {topic_order}: {topic_data['name']}")
    
    async with AsyncSessionLocal() as db:
        try:
            # Get topic_id
            result = await db.execute(
                text("SELECT id FROM topics WHERE level = 'A1' AND \"order\" = :order"),
                {"order": topic_order}
            )
            row = result.fetchone()
            
            if not row:
                print(f"❌ Topic {topic_order} không tồn tại trong database")
                return False
            
            topic_id = str(row[0])
            
            # Update topic
            await db.execute(
                text("""
                    UPDATE topics
                    SET name = :name, name_vi = :name_vi,
                        description = :desc, description_vi = :desc_vi
                    WHERE id = :id
                """),
                {
                    "id": topic_id,
                    "name": topic_data['name'],
                    "name_vi": topic_data['name_vi'],
                    "desc": topic_data.get('description', ''),
                    "desc_vi": topic_data.get('description_vi', '')
                }
            )
            print("  ✅ Đã update thông tin topic")
            
            # Update lessons
            for lesson in topic_data.get('lessons', []):
                lesson_type = lesson['lesson_type']
                lesson_order = lesson['order']
                
                # Get lesson_id
                result = await db.execute(
                    text("""
                        SELECT id FROM lessons 
                        WHERE topic_id = :topic_id 
                        AND lesson_type = :type
                        AND "order" = :order
                    """),
                    {
                        "topic_id": topic_id,
                        "type": lesson_type,
                        "order": lesson_order
                    }
                )
                lesson_row = result.fetchone()
                
                if lesson_row:
                    await db.execute(
                        text("""
                            UPDATE lessons
                            SET title = :title, title_vi = :title_vi,
                                content = CAST(:content AS jsonb)
                            WHERE id = :id
                        """),
                        {
                            "id": str(lesson_row[0]),
                            "title": lesson.get('title', ''),
                            "title_vi": lesson.get('title_vi', ''),
                            "content": json.dumps(lesson.get('content', {}))
                        }
                    )
                    print(f"  ✅ Updated {lesson_type}")
            
            await db.commit()
            print(f"✅ Hoàn thành Topic {topic_order}!\n")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            await db.rollback()
            return False

async def update_all_topics():
    """Update tất cả topics 13-20"""
    topics = [13, 14, 15, 16, 17, 18, 19, 20]
    success = 0
    
    for topic_num in topics:
        if await quick_update(topic_num):
            success += 1
        await asyncio.sleep(1)  # Delay giữa các update
    
    print(f"\n🎉 Hoàn thành! Đã cập nhật {success}/{len(topics)} topics")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Update một topic cụ thể
        topic_num = int(sys.argv[1])
        asyncio.run(quick_update(topic_num))
    else:
        # Update tất cả
        print("🚀 Cập nhật tất cả Topics 13-20...\n")
        asyncio.run(update_all_topics())
