# app/models/exercise_result.py
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class ExerciseResult(Base):
    __tablename__ = "exercise_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)  # Bỏ index=True

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("learning_sessions.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    exercise_id = Column(String, nullable=True)  # AI-generated hoặc external id
    exercise_type = Column(String, nullable=False, index=True)
    
    user_answer = Column(Text, nullable=True)
    expected_answer = Column(Text, nullable=True)
    
    is_correct = Column(Boolean, nullable=False, default=False)
    
    skill_tag = Column(String, nullable=False, index=True)
    difficulty = Column(String, default="medium", nullable=False)   # Có thể đổi Enum sau

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )

    # Relationships
    user = relationship("User", back_populates="exercise_results")
    session = relationship("LearningSession", back_populates="exercise_results")

    # Composite Indexes
    __table_args__ = (
        Index("ix_exercise_user_skill", "user_id", "skill_tag"),
        Index("ix_exercise_user_created", "user_id", "created_at"),
        Index("ix_exercise_session_created", "session_id", "created_at"), 
    )

    def __repr__(self):
        return f"<ExerciseResult {self.skill_tag} - Correct: {self.is_correct}>"