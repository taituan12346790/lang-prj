from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ChatRequest(BaseModel):
    user_input: str = Field(..., min_length=1, max_length=2000)
    target_lang: Optional[str] = None
    explain_in: Optional[str] = "vi"
    difficulty: Optional[DifficultyLevel] = None
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0)


class ChatResponse(BaseModel):
    response: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None


class ChatHistoryItem(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None


class ChatHistoryResponse(BaseModel):
    history: list[ChatHistoryItem] = Field(default_factory=list)
    total: int = 0