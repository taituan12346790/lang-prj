# app/models/chat_learning_activity.py
"""
Chat Learning Activity Model - Track learning activities from AI Tutor chat
Ghi nhận lesson, practice, quiz được học qua chat (không chỉ curriculum có sẵn)
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Float, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.core.database import Base


class ChatLearningActivity(Base):
    """Log các hoạt động học tập từ AI Tutor chat"""
    __tablename__ = "chat_learning_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Link to chat conversation
    chat_session_id = Column(String, nullable=False, index=True)  # Same as conversations.session_id
    
    # Activity classification
    activity_type = Column(String(50), nullable=False, index=True)  # lesson, practice, quiz, vocabulary
    title = Column(String(200), nullable=False)  # "Past Simple", "Từ vựng du lịch"
    
    # Topic context
    custom_topic = Column(String(100), nullable=True)  # "du lịch", "công nghệ" - user's interest
    curriculum_topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    curriculum_lesson_order = Column(Integer, nullable=True)  # If learning from curriculum
    
    # Content details (flexible JSON structure)
    content = Column(JSONB, default={}, nullable=False)
    """
    Content structure examples:
    
    Practice:
    {
        "question": "She ___ to school yesterday.",
        "user_answer": "go",
        "correct_answer": "went",
        "is_correct": false,
        "ai_feedback": "..."
    }
    
    Lesson:
    {
        "summary": "Giải thích Past Simple...",
        "key_points": ["V2", "yesterday"],
        "examples": ["I went...", "She studied..."]
    }
    
    Quiz (multiple questions in one session):
    {
        "questions": [
            {"q": "...", "user": "A", "correct": "B", "is_correct": false}
        ],
        "total": 5,
        "correct_count": 3
    }
    """
    
    # Performance metrics
    score = Column(Float, nullable=True)  # 0-100 or null for lessons
    
    # Skill tags for analytics
    skill_tags = Column(JSONB, default=[], nullable=False)  # ["past_tense", "vocabulary_travel"]
    
    # Source tracking
    source = Column(String(50), default="ai_tutor_chat", nullable=False)  # Always "ai_tutor_chat"
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="chat_learning_activities")
    topic = relationship("Topic", backref="chat_learning_activities")

    # Composite Indexes for efficient queries
    __table_args__ = (
        Index("ix_chat_activity_user_type", "user_id", "activity_type"),
        Index("ix_chat_activity_user_created", "user_id", "created_at"),
        Index("ix_chat_activity_session", "chat_session_id", "created_at"),
    )

    def __repr__(self):
        return f"<ChatLearningActivity(user_id={self.user_id}, type={self.activity_type}, title={self.title})>"
