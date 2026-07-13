"""
FORCE UPDATE - Xóa và tạo lại TẤT CẢ lessons cho 20 topics A1
"""

import sys
import psycopg2
import json
from psycopg2.extras import Json

sys.path.insert(0, '.')
from app.data.topics_data import A1_TOPICS

# Connection string
CONNECTION_STRING = "postgresql://neondb_owner:npg_TBSbNV0XK4dZ@ep-rapid-sea-ao7qnzl8-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def force_update():
    """Force update - XÓA và TẠO LẠI tất cả lessons"""
    
    print("=" * 80)
    print("🚀 FORCE UPDATE - XÓA VÀ TẠO LẠI TẤT CẢ LESSONS")
    print("=" * 80)
    
    try:
        # Connect
        print("🔗 Connecting to Neon Tech...")
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()
        print("✅ Connected!\n")
        
        success_count = 0
        
        for topic_data in A1_TOPICS:
            topic_order = topic_data['order']
            
            # Get topic_id
            cur.execute(
                'SELECT id FROM topics WHERE level = %s AND "order" = %s',
                ('A1', topic_order)
            )
            result = cur.fetchone()
            
            if not result:
                print(f"❌ Topic {topic_order} not found")
                continue
            
            topic_id = str(result[0])
            print(f"📚 Topic {topic_order}: {topic_data['name']}")
            
            # 1. UPDATE topic info
            cur.execute(
                """UPDATE topics 
                   SET name = %s, name_vi = %s, description = %s, description_vi = %s,
                       grammar_focus = %s, vocabulary_tags = %s, estimated_minutes = %s
                   WHERE id = %s""",
                (topic_data['name'], topic_data.get('name_vi', ''),
                 topic_data.get('description', ''), topic_data.get('description_vi', ''),
                 Json(topic_data.get('grammar_focus', [])),
                 Json(topic_data.get('vocabulary_tags', [])),
                 topic_data.get('estimated_minutes', 30),
                 topic_id)
            )
            print(f"   ✅ Updated topic info")
            
            # 2. DELETE all old lessons
            cur.execute('DELETE FROM lessons WHERE topic_id = %s', (topic_id,))
            deleted_count = cur.rowcount
            print(f"   🗑️  Deleted {deleted_count} old lessons")
            
            # 3. INSERT new lessons
            for lesson in topic_data.get('lessons', []):
                cur.execute(
                    """INSERT INTO lessons (id, topic_id, "order", lesson_type, title, title_vi, content)
                       VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s)""",
                    (topic_id,
                     lesson['order'],
                     lesson['lesson_type'],
                     lesson.get('title', ''),
                     lesson.get('title_vi', ''),
                     Json(lesson.get('content', {})))
                )
            
            lesson_count = len(topic_data.get('lessons', []))
            print(f"   ➕ Inserted {lesson_count} new lessons")
            print()
            
            success_count += 1
        
        # Commit
        conn.commit()
        
        print("=" * 80)
        print(f"🎉 HOÀN THÀNH! Đã update {success_count}/20 topics!")
        print("=" * 80)
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    response = input("⚠️  Bạn có chắc muốn XÓA và TẠO LẠI tất cả lessons? (yes/no): ")
    if response.lower() == 'yes':
        force_update()
    else:
        print("❌ Đã hủy!")
