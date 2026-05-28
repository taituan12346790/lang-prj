# app/models/learning_session.py
from uuid import uuid4
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)  # Bỏ index=True

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    session_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    level = Column(String, nullable=False)
    duration_minutes = Column(Integer, default=0)
    
    metrics = Column(
        JSONB,
        nullable=False,
        default=dict
    )
    
    summary = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="learning_sessions")
    exercise_results = relationship(
        "ExerciseResult", 
        back_populates="session", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<LearningSession {self.id} - Level {self.level}>"