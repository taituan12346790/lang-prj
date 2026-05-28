# app/core/planner.py
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from loguru import logger

from app.llm.llm_client import LLMClient
from app.models.user_profile import UserProfile


class PlanStep(BaseModel):
    """Cấu trúc từng bước trong kế hoạch"""
    step: int
    action: str
    tool: str | None = None
    purpose: str
    expected_outcome: str | None = None


class LearningPlan(BaseModel):
    """Structured Learning Plan - Dùng cho LangGraph"""
    overall_goal: str
    reasoning: str = Field(..., max_length=250)
    steps: List[PlanStep] = Field(..., min_length=1, max_length=5)
    tools_to_use: List[str] = Field(default_factory=list)
    estimated_duration: str
    personalization_notes: str = Field(default="")


class ReActPlanner:
    """ReAct Planner - Tối ưu cho LangGraph"""

    def __init__(self):
        self.llm = LLMClient()

    async def create_plan(
        self,
        user_input: str,
        user_id: str,
        strategy: Dict[str, Any],
        long_mem: UserProfile
    ) -> LearningPlan:
        """
        Tạo kế hoạch học tập có cấu trúc
        """
        # Guard clause sớm
        if not user_input or not user_input.strip():
            logger.warning(f"Planner received empty input from user {user_id}")
            return self._get_fallback_plan("Empty request")

        try:
            # Xây dựng context an toàn
            weak_skills_str = (
                ", ".join(list(long_mem.weak_skills.keys())[:6])
                if long_mem.weak_skills else "None"
            )
            interests_str = (
                ", ".join(long_mem.interests[-5:])
                if long_mem.interests else "None"
            )

            context = f"""
User Level: {long_mem.current_level}
Target Language: {long_mem.target_language}
Weak Skills: {weak_skills_str}
Interests: {interests_str}
"""

            prompt = f"""Bạn là Senior Language Learning Planner chuyên nghiệp.

{context}

CURRENT REQUEST: {user_input}
CURRENT STRATEGY: {strategy.get('mode', 'general')}

Tạo kế hoạch học tập thông minh, thực tế, tối đa 5 bước.
Mỗi bước phải rõ ràng, có tool (nếu cần) và mục đích cụ thể.

Trả về JSON theo đúng schema LearningPlan."""

            plan = await self.llm.generate_structured_async(
                system_prompt="Bạn là Senior Language Learning Planner chuyên nghiệp.",
                user_prompt=prompt,
                response_format=LearningPlan,
                temperature=0.35
            )

            if plan is None:
                logger.warning(f"Planner returned None for user {user_id}, using fallback")
                return self._get_fallback_plan(user_input)

            # Nếu trả về dict thì convert sang model
            if isinstance(plan, dict):
                return LearningPlan.model_validate(plan)

            return plan

        except Exception:
            logger.exception(f"Planner failed for user {user_id}")
            return self._get_fallback_plan(user_input)

    def _get_fallback_plan(self, user_input: str) -> LearningPlan:
        """Fallback plan an toàn"""
        return LearningPlan(
            overall_goal=f"Hỗ trợ yêu cầu: {user_input[:60]}...",
            reasoning="Fallback plan do planner lỗi",
            steps=[
                PlanStep(
                    step=1,
                    action="Trả lời trực tiếp yêu cầu của người dùng",
                    tool="llm_response",
                    purpose="Xử lý câu hỏi chính",
                    expected_outcome="Người dùng nhận được câu trả lời hữu ích"
                )
            ],
            tools_to_use=["llm_response"],
            estimated_duration="5-8 phút",
            personalization_notes="Sử dụng fallback plan"
        )