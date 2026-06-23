# app/models/user_profile.py
from uuid import uuid4
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )

    native_language = Column(String, default="vi", nullable=False)
    target_language = Column(String, nullable=False)   # không default
    current_level = Column(String, default="A1", nullable=False)
    placement_score = Column(Float, default=0.0)

    # Mutable JSONB để SQLAlchemy detect thay đổi khi append/modify
    weak_skills = Column(MutableDict.as_mutable(JSONB), default=dict)
    strong_skills = Column(MutableDict.as_mutable(JSONB), default=dict)
    
    learning_style = Column(String, default="balanced", nullable=False)

    interests = Column(MutableList.as_mutable(JSONB), default=list)
    goals = Column(MutableList.as_mutable(JSONB), default=list)
    preferred_topics = Column(MutableList.as_mutable(JSONB), default=list)

    total_sessions = Column(Integer, default=0)
    total_conversations = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    
    # Onboarding flag for OAuth users
    onboarding_completed = Column(Boolean, default=True, nullable=False)  # True for email/password, False for OAuth initially

    # Learning context - Sprint 1
    active_topic_id = Column(String(50), nullable=True)
    active_lesson_order = Column(Integer, nullable=True)
    learning_mode = Column(String(50), default="normal", nullable=False)  # normal, quiz_review, free_chat
    last_chat_session_id = Column(String(255), nullable=True)

    last_active = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile {self.user_id} - Level {self.current_level}>"