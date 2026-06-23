"""add writing lesson to all topics

Revision ID: 008_add_writing_lesson
Revises: 007_add_chat_learning_activities
Create Date: 2026-06-10

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

# revision identifiers, used by Alembic.
revision = '008_add_writing_lesson'
down_revision = '007_add_chat_learning_activities'
branch_labels = None
depends_on = None


def upgrade():
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
    
    # 2. Get all topics
    result = conn.execute(sa.text("SELECT id, level, name FROM topics ORDER BY level, \"order\""))
    topics = result.fetchall()
    
    # 3. For each topic, create a writing lesson
    for topic in topics:
        topic_id, level, topic_name = topic
        
        # Generate writing prompt based on topic name
        writing_content = generate_writing_content(topic_name, level)
        
        # Insert writing lesson
        conn.execute(
            sa.text("""
                INSERT INTO lessons (id, topic_id, "order", lesson_type, title, title_vi, content)
                VALUES (:id, :topic_id, :order, :lesson_type, :title, :title_vi, :content)
            """),
            {
                "id": str(uuid.uuid4()),
                "topic_id": str(topic_id),
                "order": 4,
                "lesson_type": "writing",
                "title": f"Writing: {topic_name}",
                "title_vi": f"Viết đoạn văn: {topic_name}",
                "content": writing_content
            }
        )
    
    print(f"✅ Added writing lessons to {len(topics)} topics")


def downgrade():
    """
    Remove all writing lessons and restore quiz lessons to order=4.
    """
    conn = op.get_bind()
    
    # 1. Delete all writing lessons
    conn.execute(sa.text("DELETE FROM lessons WHERE lesson_type = 'writing'"))
    
    # 2. Restore quiz lessons back to order=4
    conn.execute(
        sa.text("""
            UPDATE lessons 
            SET "order" = 4 
            WHERE lesson_type = 'quiz' AND "order" = 5
        """)
    )
    
    print("✅ Removed all writing lessons and restored quiz order")


def generate_writing_content(topic_name: str, level: str) -> dict:
    """
    Generate writing lesson content based on topic name and level.
    """
    # Default writing prompts by level
    level_word_counts = {
        "A1": 30,
        "A2": 50,
        "B1": 80,
        "B2": 120,
        "C1": 150,
        "C2": 200
    }
    
    min_words = level_word_counts.get(level, 50)
    
    # Generate prompt based on topic
    content = {
        "prompt": f"Write a short paragraph about: {topic_name}",
        "prompt_vi": f"Viết một đoạn văn ngắn về: {topic_name}",
        "min_words": min_words,
        "tips": [
            "Use vocabulary and grammar from this topic",
            "Write clear and simple sentences",
            "Check your spelling and grammar before submitting",
            f"Write at least {min_words} words"
        ],
        "example": {
            "title": "Example paragraph",
            "text": f"This is an example paragraph about {topic_name}. You should write your own paragraph using the vocabulary and grammar you learned in this lesson.",
            "translation": "Đây là đoạn văn mẫu. Bạn nên viết đoạn văn của riêng mình sử dụng từ vựng và ngữ pháp đã học."
        }
    }
    
    return content
