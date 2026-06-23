from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ChatRequest(BaseModel):
    user_input: str = Field(..., min_length=1, max_length=8000)  # Increased for AI Tutor mode
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking (A4/A5)")
    target_lang: Optional[str] = None
    explain_in: Optional[str] = "vi"
    difficulty: Optional[DifficultyLevel] = None
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0)
    # Sprint 3: Quiz context for focused review
    quiz_wrong_answers: Optional[list] = Field(None, description="Wrong answers from quiz")
    quiz_topic_id: Optional[str] = Field(None, description="Topic ID for quiz review")


class ChatResponse(BaseModel):
    response: str
    metadata: Dict[str, Any] = Field(default_factory=dict, description="B3: learning_context, current_level, active_topic")
    success: bool = True
    error: Optional[str] = None


class ChatHistoryItem(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None


class ChatHistoryResponse(BaseModel):
    history: list[ChatHistoryItem] = Field(default_factory=list)
    total: int = 0