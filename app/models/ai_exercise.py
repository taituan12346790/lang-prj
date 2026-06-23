# app/models/ai_exercise.py
"""Models for AI-generated exercises and submissions"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
import enum

from app.core.database import Base


class ExerciseStatus(enum.Enum):
    PENDING = "pending"  # Đã tạo, chưa làm
    IN_PROGRESS = "in_progress"  # Đang làm
    COMPLETED = "completed"  # Đã hoàn thành


class AIExercise(Base):
    """AI-generated exercises for error remediation"""
    __tablename__ = "ai_exercises"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=True, index=True)
    
    # Error context
    error_type = Column(String, nullable=False)  # TENSE_MISMATCH, GRAMMAR_ERROR, etc.
    skill_tag = Column(String, nullable=False)  # present_continuous, past_simple, etc.
    frequency = Column(Integer, default=1)  # Số lần sai lỗi này
    
    # Original error
    original_question = Column(String, nullable=True)
    user_wrong_answer = Column(String, nullable=True)
    correct_answer = Column(String, nullable=True)
    
    # Exercises (array of questions)
    exercises = Column(JSONB, nullable=False)
    # Format: [
    #   {"question": "She ___ (watch) TV", "correct_answer": "is watching", "number": 1},
    #   {"question": "They ___ (play) football", "correct_answer": "are playing", "number": 2}
    # ]
    
    # Status
    status = Column(SQLEnum(ExerciseStatus), default=ExerciseStatus.PENDING, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="ai_exercises")
    submissions = relationship("AIExerciseSubmission", back_populates="exercise", cascade="all, delete-orphan")


class AIExerciseSubmission(Base):
    """User submissions for AI exercises"""
    __tablename__ = "ai_exercise_submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exercise_id = Column(UUID(as_uuid=True), ForeignKey("ai_exercises.id"), nullable=False, index=True)
    
    # Submission
    user_answers = Column(JSONB, nullable=False)
    # Format: [
    #   {"number": 1, "answer": "is watching", "is_correct": true},
    #   {"number": 2, "answer": "are play", "is_correct": false}
    # ]
    
    # Scoring
    score = Column(Integer, nullable=False)  # Số câu đúng (0-5)
    total = Column(Integer, nullable=False)  # Tổng số câu (thường là 5)
    
    # Feedback
    feedback = Column(String, nullable=True)  # General feedback from AI
    
    # Timestamp
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationship
    exercise = relationship("AIExercise", back_populates="submissions")
