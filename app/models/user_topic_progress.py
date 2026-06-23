# app/models/user_topic_progress.py
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class UserTopicProgress(Base):
    """Tiến độ học của user cho từng chủ đề"""
    __tablename__ = "user_topic_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    topic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Progress tracking
    status = Column(String(20), default="not_started", nullable=False)
    # Values: not_started / in_progress / completed

    lesson_completed = Column(Integer, default=0)   # 0–5 (bài 1-5 hoàn thành)
    quiz_score = Column(Float, nullable=True)        # Điểm quiz cuối (0-100)
    quiz_attempts = Column(Integer, default=0)       # Số lần làm quiz

    # NEW: Spaced repetition & weak skills
    next_review_date = Column(DateTime(timezone=True), nullable=True)  # Khi nào cần ôn lại
    weak_skills = Column(JSONB, nullable=True)  # {"grammar_past_tense": 0.33, "vocabulary": 0.5}

    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="topic_progress")
    topic = relationship("Topic", back_populates="user_progress")

    # Unique constraint: 1 record per user per topic
    __table_args__ = (
        Index("ix_user_topic_unique", "user_id", "topic_id", unique=True),
    )

    def __repr__(self):
        return f"<UserTopicProgress user={self.user_id} topic={self.topic_id} status={self.status}>"
