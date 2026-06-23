# app/schemas/writing.py
"""Schemas for writing submission and feedback"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime


class SubmitWritingRequest(BaseModel):
    """Request to submit a writing"""
    lesson_id: UUID
    topic_id: UUID
    prompt: str
    user_text: str = Field(..., min_length=10, max_length=2000)
    word_count: int


class WritingFeedbackResponse(BaseModel):
    """AI feedback response"""
    writing_id: UUID
    attempt_number: int
    
    # General feedback
    feedback: str
    
    # Scores
    score_grammar: float = Field(..., ge=0, le=25)
    score_vocabulary: float = Field(..., ge=0, le=25)
    score_content: float = Field(..., ge=0, le=25)
    score_structure: float = Field(..., ge=0, le=25)
    score_total: float = Field(..., ge=0, le=100)
    
    # Detailed feedback
    detailed_feedback: Optional[Dict[str, Any]] = None
    
    # Timestamps
    submitted_at: datetime
    reviewed_at: datetime


class WritingHistoryItem(BaseModel):
    """Writing history item"""
    id: UUID
    lesson_id: UUID
    topic_id: UUID
    attempt_number: int
    prompt: str
    user_text: str
    word_count: int
    feedback: Optional[str] = None
    score_total: Optional[float] = None
    score_grammar: Optional[float] = None
    score_vocabulary: Optional[float] = None
    score_content: Optional[float] = None
    score_structure: Optional[float] = None
    detailed_feedback: Optional[Dict[str, Any]] = None
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class WritingStatsResponse(BaseModel):
    """User writing statistics"""
    total_writings: int
    average_score: float
    best_score: float
