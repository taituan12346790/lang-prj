"""
FAST UPDATE - Cập nhật TẤT CẢ 20 Topics A1 trong 1 transaction duy nhất
NHANH và HIỆU QUẢ - Update hàng loạt
"""

import asyncio
import sys
import asyncpg
import json

sys.path.insert(0, '.')
from app.data.topics_data import A1_TOPICS

# PRODUCTION Neon Tech connection
DATABASE_CONFIG = {
    "host": "ep-rapid-sea-ao7qnzl8-pooler.c-2.ap-southeast-1.aws.neon.tech",
    "port": 5432,
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_TBSbNV0XK4dZ",
    "ssl": "require"
}

async def fast_update():
    """Update NHANH bằng asyncpg trực tiếp"""
    
    print("=" * 80)
    print("🚀 FAST UPDATE - TẤT CẢ 20 TOPICS A1 VÀO PRODUCTION NEON TECH")
    print("=" * 80)
    
    conn = await asyncpg.connect(**DATABASE_CONFIG)
    
    try:
        # Bắt đầu transaction
        async with conn.transaction():
            success_count = 0
            
            for topic_data in A1_TOPICS:
                topic_order = topic_data['order']
                
                # Get topic_id
                topic_id = await conn.fetchval(
                    "SELECT id FROM topics WHERE level = 'A1' AND \"order\" = $1",
                    topic_order
                )
                
                if not topic_id:
                    print(f"❌ Topic {topic_order} not found")
                    continue
                
                print(f"📚 Topic {topic_order}: {topic_data['name']}")
                
                # Update topic info
                await conn.execute(
                    """UPDATE topics 
                       SET name = $1, name_vi = $2, description = $3, description_vi = $4
                       WHERE id = $5""",
                    topic_data['name'],
                    topic_data['name_vi'],
                    topic_data.get('description', ''),
                    topic_data.get('description_vi', ''),
                    topic_id
                )
                
                # Update HÀNG LOẠT tất cả lessons của topic này
                for lesson in topic_data.get('lessons', []):
                    lesson_type = lesson['lesson_type']
                    lesson_order = lesson['order']
                    
                    # Update lesson
                    result = await conn.execute(
                        """UPDATE lessons 
                           SET title = $1, title_vi = $2, content = $3
                           WHERE topic_id = $4 AND lesson_type = $5 AND "order" = $6""",
                        lesson.get('title', ''),
                        lesson.get('title_vi', ''),
                        json.dumps(lesson.get('content', {})),
                        topic_id,
                        lesson_type,
                        lesson_order
                    )
                
                print(f"   ✅ OK ({len(topic_data.get('lessons', []))} lessons)")
                success_count += 1
            
            print()
            print("=" * 80)
            print(f"🎉 HOÀN THÀNH! Đã update {success_count}/20 topics vào PRODUCTION!")
            print("=" * 80)
            
    except Exception as e:
        print(f"❌ LỖI: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(fast_update())
