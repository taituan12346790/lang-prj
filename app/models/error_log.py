# app/models/error_log.py
"""
User Error Log Model - Track learning mistakes for personalized feedback
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.core.database import Base


class UserErrorLog(Base):
    """Log của lỗi sai mà user mắc phải trong quá trình học"""
    __tablename__ = "user_error_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Error classification
    error_type = Column(String(100), nullable=False, index=True)  # TENSE_MISMATCH, SUBJECT_VERB, etc.
    skill_tag = Column(String(100), nullable=False, index=True)   # past_tense, subject_verb_agreement, etc.
    severity = Column(String(20), default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    
    # Content
    user_input = Column(Text, nullable=False)  # Câu user gõ sai
    user_answer = Column(Text)  # Đáp án user chọn (nếu là quiz)
    correct_form = Column(Text, nullable=False)  # Correct answer
    
    # Context
    question = Column(Text)  # Câu hỏi gốc (nếu là practice/quiz)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    
    # Metadata
    explanation = Column(Text)  # AI-generated explanation
    suggestion = Column(Text)  # AI-generated suggestion
    extra_data = Column(JSONB, default={})  # Additional info
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="error_logs")
    lesson = relationship("Lesson", backref="error_logs")
    topic = relationship("Topic", backref="error_logs")

    def __repr__(self):
        return f"<UserErrorLog(user_id={self.user_id}, error_type={self.error_type}, skill={self.skill_tag})>"
