# app/models/user_profile.py
from uuid import uuid4
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Integer
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

    last_active = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile {self.user_id} - Level {self.current_level}>"