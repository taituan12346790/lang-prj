from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class SkillType(str, Enum):
    GRAMMAR = "grammar"
    VOCABULARY = "vocabulary"
    LISTENING = "listening"
    READING = "reading"
    SPEAKING = "speaking"
    WRITING = "writing"


class TestType(str, Enum):
    GRAMMAR = "grammar"
    VOCABULARY = "vocabulary"
    SPEAKING = "speaking"
    MIXED = "mixed"


class Level(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


# ---------- Placement test ----------
class PlacementTestQuestion(BaseModel):
    question_id: str
    question: str
    options: List[str] = Field(..., min_items=2, max_items=6)
    skill_type: SkillType
    # Không expose ra API
    correct_answer: Optional[str] = Field(default=None, exclude=True)


class PlacementTestRequest(BaseModel):
    answers: Dict[str, str] = Field(..., description="question_id -> answer")


class PlacementTestResponse(BaseModel):
    estimated_level: Level
    score: float = Field(..., ge=0, le=100)
    strengths: List[SkillType] = Field(default_factory=list)
    weaknesses: List[SkillType] = Field(default_factory=list)
    recommended_focus: List[str] = Field(default_factory=list)
    message: str
    total_questions: int
    correct_answers: int


# ---------- Level-up test ----------
class LevelUpTestRequest(BaseModel):
    test_type: TestType
    current_level: Level
    num_questions: int = Field(10, ge=5, le=30)
    answers: Dict[str, str] = Field(..., description="Đáp án của người dùng: {question_id: answer}")


class LevelUpTestQuestion(BaseModel):
    question_id: str
    question: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = Field(default=None, exclude=True)
    explanation: str
    skill_type: SkillType


class LevelUpTestSubmit(BaseModel):
    answers: Dict[str, str] = Field(..., description="question_id -> answer")


class LevelUpTestResult(BaseModel):
    passed: bool
    score: float = Field(..., ge=0, le=100)
    new_level: Optional[Level] = None
    message: str
    strengths: List[SkillType] = Field(default_factory=list)
    weaknesses: List[SkillType] = Field(default_factory=list)
    recommendation: str


class TestHistoryResponse(BaseModel):
    test_id: UUID
    test_type: TestType
    level: Level
    score: float
    passed: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)