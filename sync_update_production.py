"""
SYNC UPDATE - Dùng psycopg2 (synchronous) để update nhanh
"""

import sys
import psycopg2
import json

sys.path.insert(0, '.')
from app.data.topics_data import A1_TOPICS

# Connection string
CONNECTION_STRING = "postgresql://neondb_owner:npg_TBSbNV0XK4dZ@ep-rapid-sea-ao7qnzl8-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def sync_update():
    """Update đồng bộ - NHANH"""
    
    print("=" * 80)
    print("🚀 SYNC UPDATE - TẤT CẢ 20 TOPICS A1 VÀO PRODUCTION")
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
            print(f"📚 Topic {topic_order}: {topic_data['name']}", end=" ")
            
            # Update topic
            cur.execute(
                """UPDATE topics 
                   SET name = %s, name_vi = %s, description = %s, description_vi = %s
                   WHERE id = %s""",
                (topic_data['name'], topic_data['name_vi'], 
                 topic_data.get('description', ''), topic_data.get('description_vi', ''),
                 topic_id)
            )
            
            # Update lessons
            for lesson in topic_data.get('lessons', []):
                cur.execute(
                    """UPDATE lessons 
                       SET title = %s, title_vi = %s, content = %s
                       WHERE topic_id = %s AND lesson_type = %s AND "order" = %s""",
                    (lesson.get('title', ''), lesson.get('title_vi', ''),
                     json.dumps(lesson.get('content', {})),
                     topic_id, lesson['lesson_type'], lesson['order'])
                )
            
            print("✅")
            success_count += 1
        
        # Commit
        conn.commit()
        
        print()
        print("=" * 80)
        print(f"🎉 THÀNH CÔNG! Đã update {success_count}/20 topics vào PRODUCTION!")
        print("=" * 80)
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    sync_update()
