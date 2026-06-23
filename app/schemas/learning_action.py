# app/schemas/learning_action.py
"""
Phase 3: Learning Action schemas for Agent → UI communication
Agent suggests actions, UI renders buttons, user confirms, backend executes
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import Enum


class SuggestedActionType(str, Enum):
    """Types of actions Agent can suggest"""
    CONTINUE_LESSON = "continue_lesson"          # Keep explaining current lesson
    OFFER_PRACTICE = "offer_practice"            # Generate practice exercises
    COMPLETE_LESSON = "complete_lesson"          # Mark lesson as done
    GO_TO_LESSON = "go_to_lesson"                # Move to specific lesson
    START_QUIZ = "start_quiz"                    # Open topic quiz
    QUIZ_REVIEW = "quiz_review"                  # Review quiz mistakes
    REVIEW_WEAK_SKILL = "review_weak_skill"      # Spaced repetition review
    START_LEVEL_UP_TEST = "start_level_up_test"  # Suggest level-up test
    FREE_CHAT = "free_chat"                      # Continue free conversation


class SuggestedAction(BaseModel):
    """A single suggested action from Agent"""
    type: SuggestedActionType
    label: str = Field(..., max_length=100, description="Button text for UI")
    reasoning: str = Field(..., max_length=200, description="Why Agent suggests this")
    params: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    priority: int = Field(default=1, ge=1, le=3, description="1=highest, 3=lowest")


class ExecuteActionRequest(BaseModel):
    """Request to execute an action suggested by Agent"""
    action_type: SuggestedActionType
    params: Dict[str, Any] = Field(default_factory=dict)


class ExecuteActionResponse(BaseModel):
    """Response after executing action"""
    success: bool
    message: str
    redirect_page: Optional[str] = None  # "quiz", "lesson", "level_up", etc.
    data: Dict[str, Any] = Field(default_factory=dict)
