# app/schemas/learning.py
"""Pydantic schemas cho Learning Path API"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum


class LessonType(str, Enum):
    GRAMMAR = "grammar"
    VOCABULARY = "vocabulary"
    PRACTICE = "practice"
    WRITING = "writing"
    QUIZ = "quiz"
    # Vietnamese aliases (for backward compatibility with old data)
    NGU_PHAP = "ngữ pháp"
    TU_VUNG = "từ vựng"
    THUC_HANH = "thực hành"
    VIET = "viết"
    KIEM_TRA = "kiểm tra"


class TopicStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# ── Error Analysis ────────────────────────────────────────────────────────────

class AnalyzeErrorRequest(BaseModel):
    """Request schema for error analysis"""
    question: str
    user_answer: str
    correct_answer: str
    skill_tag: Optional[str] = None
    lesson_id: Optional[UUID] = None
    topic_id: Optional[UUID] = None


# ── Lesson ───────────────────────────────────────────────────────────────────

class LessonResponse(BaseModel):
    id: UUID
    topic_id: UUID
    order: int
    lesson_type: LessonType
    title: str
    title_vi: Optional[str] = None
    content: Dict[str, Any] = {}
    model_config = ConfigDict(from_attributes=True)


class LessonSummary(BaseModel):
    id: UUID
    order: int
    lesson_type: LessonType
    title: str
    title_vi: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# ── Topic ─────────────────────────────────────────────────────────────────────

class TopicProgressInfo(BaseModel):
    """Tiến độ của user trên 1 chủ đề"""
    status: TopicStatus = TopicStatus.NOT_STARTED
    lesson_completed: int = 0      # 0-4
    quiz_score: Optional[float] = None
    quiz_attempts: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TopicResponse(BaseModel):
    id: UUID
    level: str
    order: int
    name: str
    name_vi: str
    description: Optional[str] = None
    description_vi: Optional[str] = None
    grammar_focus: List[str] = []
    vocabulary_tags: List[str] = []
    estimated_minutes: int = 30
    lesson_count: int = 4
    # User progress overlaid
    progress: TopicProgressInfo = Field(default_factory=TopicProgressInfo)
    model_config = ConfigDict(from_attributes=True)


class TopicDetailResponse(TopicResponse):
    lessons: List[LessonSummary] = []


# ── Dashboard / Level Progress ────────────────────────────────────────────────

class LevelProgressResponse(BaseModel):
    level: str
    total_topics: int
    completed_topics: int
    in_progress_topics: int
    completion_percentage: float
    average_quiz_score: Optional[float] = None
    can_level_up: bool = False
    level_up_message: str = ""


class DashboardResponse(BaseModel):
    current_level: str
    level_progress: LevelProgressResponse
    next_topic: Optional[TopicResponse] = None       # Chủ đề tiếp theo cần học
    current_topic: Optional[TopicResponse] = None    # Chủ đề đang học dở
    recent_completed: List[TopicResponse] = []       # Vừa hoàn thành


# ── Topic Progress Update ────────────────────────────────────────────────────

class UpdateLessonProgressRequest(BaseModel):
    lesson_order: int = Field(..., ge=1, le=4)


class UpdateLessonProgressResponse(BaseModel):
    topic_id: UUID
    lesson_completed: int
    status: TopicStatus
    message: str


# ── Quiz ─────────────────────────────────────────────────────────────────────

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    # correct & explanation NOT exposed in list


class QuizQuestionsResponse(BaseModel):
    topic_id: UUID
    topic_name: str
    questions: List[QuizQuestion]
    total: int


class QuizSubmitRequest(BaseModel):
    answers: Dict[str, str] = Field(..., description="question_id -> chosen_option")


class QuizQuestionResult(BaseModel):
    id: str
    question: str
    your_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str


class QuizSubmitResponse(BaseModel):
    topic_id: UUID
    score: float           # 0-100
    passed: bool           # score >= 70
    correct_count: int
    total_count: int
    results: List[QuizQuestionResult]
    feedback: str
    topic_completed: bool  # True if all 5 lessons done + quiz passed


# ── Learning Context Activation (Sprint 1) ────────────────────────────────────

class ActivateLearningContextRequest(BaseModel):
    """Request to set active topic/lesson for a user"""
    topic_id: str = Field(..., description="Topic ID to activate")
    lesson_order: Optional[int] = Field(None, ge=1, le=5, description="Lesson order (1-5)")
    learning_mode: str = Field("normal", description="normal | quiz_review | free_chat")


class LearningContextResponse(BaseModel):
    """Current learning context for user with progress"""
    active_topic_id: Optional[str] = None
    active_lesson_order: Optional[int] = None
    learning_mode: str = "normal"
    topic_name: Optional[str] = None
    topic_name_vi: Optional[str] = None
    lesson_title: Optional[str] = None
    lesson_type: Optional[str] = None
    grammar_focus: List[str] = []
    estimated_minutes: int = 0
    current_level: str
    # Progress fields
    lesson_completed: int = 0
    total_lessons: int = 0
    quiz_score: Optional[int] = None
    quiz_attempts: int = 0
    status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
