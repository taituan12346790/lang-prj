from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
from enum import Enum


class LearningStyle(str, Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING = "reading"
    KINESTHETIC = "kinesthetic"
    BALANCED = "balanced"


class Level(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    native_language: Optional[str] = None
    target_language: Optional[str] = None
    learning_style: Optional[LearningStyle] = None
    interests: Optional[List[str]] = Field(None, max_length=20)
    goals: Optional[List[str]] = Field(None, max_length=10)
    preferred_topics: Optional[List[str]] = Field(None, max_length=10)


class UserProfileResponse(BaseModel):
    user_id: UUID
    email: str
    full_name: Optional[str] = None
    native_language: str
    target_language: str
    current_level: Level
    placement_score: float = Field(0.0, ge=0, le=100)
    learning_style: LearningStyle = LearningStyle.BALANCED
    interests: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    preferred_topics: List[str] = Field(default_factory=list)
    total_sessions: int = 0
    streak_days: int = 0
    last_active: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)



class PlacementTestResponse(BaseModel):
    level: Level
    score: float = Field(..., ge=0, le=100)
    recommended_focus: List[str] = Field(default_factory=list)
    message: str