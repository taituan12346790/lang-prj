"""add_writing_lesson_to_all_topics

Revision ID: c8e5271d513c
Revises: f6c7b58afddd
Create Date: 2026-06-10 15:04:17.127987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid


# revision identifiers, used by Alembic.
revision: str = 'c8e5271d513c'
down_revision: Union[str, Sequence[str], None] = 'f6c7b58afddd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add writing lesson (order=4) to all existing topics.
    Update quiz lessons to order=5.
    """
    # Get connection
    conn = op.get_bind()
    
    # 1. Update all quiz lessons from order=4 to order=5
    conn.execute(
        sa.text("""
            UPDATE lessons 
            SET "order" = 5 
            WHERE lesson_type = 'quiz' AND "order" = 4
        """)
    )
    
    print("✅ Updated quiz lessons from order=4 to order=5")
    
    # 2. Get all topics
    result = conn.execute(sa.text("""
        SELECT id, level, name, name_vi 
        FROM topics 
        ORDER BY level, "order"
    """))
    topics = result.fetchall()
    
    print(f"📚 Found {len(topics)} topics")
    
    # 3. For each topic, create a writing lesson
    import json
    
    for topic in topics:
        topic_id, level, topic_name, topic_name_vi = topic
        
        # Generate writing prompt based on topic name
        writing_content = generate_writing_content(topic_name, topic_name_vi, level)
        
        # Insert writing lesson
        conn.execute(
            sa.text("""
                INSERT INTO lessons (id, topic_id, "order", lesson_type, title, title_vi, content)
                VALUES (:id, :topic_id, :order, :lesson_type, :title, :title_vi, CAST(:content AS jsonb))
            """),
            {
                "id": str(uuid.uuid4()),
                "topic_id": str(topic_id),
                "order": 4,
                "lesson_type": "writing",
                "title": f"Writing: {topic_name}",
                "title_vi": f"Viết: {topic_name_vi or topic_name}",
                "content": json.dumps(writing_content)
            }
        )
    
    print(f"✅ Added writing lessons to {len(topics)} topics")


def downgrade() -> None:
    """
    Remove all writing lessons and restore quiz lessons to order=4.
    """
    conn = op.get_bind()
    
    # 1. Delete all writing lessons
    conn.execute(sa.text("DELETE FROM lessons WHERE lesson_type = 'writing'"))
    
    print("✅ Deleted all writing lessons")
    
    # 2. Restore quiz lessons back to order=4
    conn.execute(
        sa.text("""
            UPDATE lessons 
            SET "order" = 4 
            WHERE lesson_type = 'quiz' AND "order" = 5
        """)
    )
    
    print("✅ Restored quiz lessons to order=4")


def generate_writing_content(topic_name: str, topic_name_vi: str, level: str) -> dict:
    """
    Generate writing lesson content based on topic name and level.
    """
    # Word count by level
    level_word_counts = {
        "A1": 40,
        "A2": 50,
        "B1": 80,
        "B2": 120,
        "C1": 150,
        "C2": 200
    }
    
    min_words = level_word_counts.get(level, 50)
    
    # Generate prompt
    content = {
        "prompt": f"Write a short paragraph about: {topic_name}",
        "prompt_vi": f"Viết một đoạn văn ngắn về: {topic_name_vi or topic_name}",
        "min_words": min_words,
        "tips": [
            f"Use vocabulary and grammar from the {topic_name} lesson",
            "Write clear and simple sentences",
            "Check your spelling and grammar before submitting",
            f"Write at least {min_words} words"
        ],
        "example": {
            "title": f"Example about {topic_name}",
            "text": f"This is an example paragraph about {topic_name}. You should write about your own experience using the vocabulary and grammar you learned in this lesson. Make it personal and interesting.",
            "translation": f"Đây là đoạn văn mẫu về {topic_name_vi or topic_name}. Bạn nên viết về trải nghiệm của mình sử dụng từ vựng và ngữ pháp đã học. Làm cho nó mang tính cá nhân và thú vị."
        }
    }
    
    return content

