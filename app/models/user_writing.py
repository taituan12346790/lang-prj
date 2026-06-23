# app/models/user_writing.py
"""Model for tracking user writing submissions"""
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.core.database import Base


class UserWriting(Base):
    __tablename__ = "user_writings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False, index=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False, index=True)
    
    # Writing content
    prompt = Column(Text, nullable=False)  # The writing prompt
    user_text = Column(Text, nullable=False)  # What user wrote
    word_count = Column(Integer, nullable=False)
    
    # Attempt tracking
    attempt_number = Column(Integer, default=1)  # 1st, 2nd, 3rd attempt...
    
    # AI Feedback & Scoring
    feedback = Column(Text, nullable=True)  # AI general feedback
    score_grammar = Column(Float, nullable=True)  # 0-25
    score_vocabulary = Column(Float, nullable=True)  # 0-25
    score_content = Column(Float, nullable=True)  # 0-25
    score_structure = Column(Float, nullable=True)  # 0-25
    score_total = Column(Float, nullable=True)  # 0-100
    
    # Detailed feedback (JSON)
    detailed_feedback = Column(JSONB, nullable=True)  # {corrections: [], suggestions: []}
    
    # Timestamps
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reviewed_at = Column(DateTime(timezone=True), nullable=True)  # When AI reviewed
    
    # Relationships
    user = relationship("User", back_populates="writings")
    lesson = relationship("Lesson")
    topic = relationship("Topic")
