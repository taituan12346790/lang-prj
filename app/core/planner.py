# app/core/planner.py
from typing import Dict, Any, List, Optional
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
        from app.llm.llm_client import get_llm_client
        self.llm = get_llm_client()  # Use singleton

    async def create_plan(
        self,
        user_input: str,
        user_id: str,
        strategy: Dict[str, Any],
        long_mem: UserProfile,
        analytics_context: Optional[Dict[str, Any]] = None
    ) -> LearningPlan:
        """
        Tạo kế hoạch học tập có cấu trúc
        """
        # Guard clause sớm
        if not user_input or not user_input.strip():
            logger.warning(f"Planner received empty input from user {user_id}")
            return self._get_fallback_plan("Empty request")

        # Build learning context string for plan goal
        learning_context_goal = ""
        steps_context = "Trả lời trực tiếp yêu cầu của người dùng"
        
        if analytics_context and "learning_context" in analytics_context:
            lc = analytics_context["learning_context"]
            topic_name = lc.get('topic_name_vi', lc.get('topic_name', ''))
            grammar_focus = lc.get('grammar_focus', [])
            
            learning_context_goal = f" trong ngữ cảnh chủ đề '{topic_name}'"
            if grammar_focus:
                learning_context_goal += f" (tập trung: {', '.join(grammar_focus[:2])})"
            
            steps_context = f"Trả lời câu hỏi và kết nối với chủ đề '{topic_name}'"

        # Phase 2: Enable LLM planning for intelligent tool selection
        mode = strategy.get('mode', 'general')
        suggested_tools = strategy.get('suggested_tools', [])
        priority_focus = strategy.get('priority_focus', [])
        
        # Map mode to suggested tools if strategy didn't provide
        # Phase 2: Use correct tool names that match registry
        if not suggested_tools or suggested_tools == ["llm_response"]:
            mode_tool_map = {
                "grammar": ["grammar", "llm_response"],  
                "translation": ["translator", "llm_response"],
                "exercise": ["exercise", "llm_response"],  # Re-enabled with fix
                "vocabulary": ["llm_response"],
                "conversation": ["llm_response"],
            }
            suggested_tools = mode_tool_map.get(mode, ["llm_response"])
        
        system_prompt = f"""You are a Learning Planner for an AI Language Tutor.

User request: "{user_input}"
Mode: {mode}
Priority Focus: {', '.join(priority_focus) if priority_focus else 'None'}
Suggested Tools: {', '.join(suggested_tools)}
{learning_context_goal}

Create a 1-3 step plan. Each step should use appropriate tools:
- grammar: Check grammar of user's text (registered as 'grammar' or 'grammar_check')
- translator: Translate between languages (registered as 'translator' or 'translate')
- exercise: Generate practice exercises (registered as 'exercise' or 'generate_exercises')
- llm_response: Generate teaching content / explanations

Return JSON with steps array:
{{
  "overall_goal": "Clear goal statement",
  "reasoning": "Why this plan",
  "steps": [
    {{
      "step": 1,
      "action": "What to do",
      "tool": "tool_name or null (use: grammar, translator, exercise, llm_response)",
      "purpose": "Why",
      "expected_outcome": "What user gets"
    }}
  ],
  "tools_to_use": ["tool1", "tool2"],
  "estimated_duration": "X minutes",
  "personalization_notes": "How it fits user's learning"
}}
"""
        
        # HOTFIX: Disable LLM planning to save API calls
        # Always use fallback plan
        return LearningPlan(
            overall_goal=f"Hỗ trợ yêu cầu: {user_input[:60]}...{learning_context_goal}",
            reasoning=f"Fallback plan for mode={mode}",
            steps=[
                PlanStep(
                    step=1,
                    action=steps_context,
                    tool=suggested_tools[0] if suggested_tools else "llm_response",
                    purpose="Xử lý câu hỏi chính",
                    expected_outcome="Người dùng nhận được câu trả lời"
                )
            ],
            tools_to_use=suggested_tools[:2] if len(suggested_tools) > 1 else suggested_tools,
            estimated_duration="5-8 phút",
            personalization_notes=f"Tập trung vào chủ đề đang học{learning_context_goal}"
        )
        
        # Original LLM planning code (disabled):
        """
        try:
            plan_dict = await self.llm.generate_structured_async(
                system_prompt=system_prompt,
                user_prompt=user_input,
                response_format=LearningPlan,
                temperature=0.3
            )
            
            if plan_dict and isinstance(plan_dict, dict):
                return LearningPlan(**plan_dict)
        except Exception as e:
            logger.warning(f"LLM planning failed: {e}, using fallback")
        """
        
        # Fallback if LLM fails (disabled above)
        return LearningPlan(
            overall_goal=f"Hỗ trợ yêu cầu: {user_input[:60]}...{learning_context_goal}",
            reasoning=f"Fallback plan after LLM error for mode={mode}",
            steps=[
                PlanStep(
                    step=1,
                    action=steps_context,
                    tool=suggested_tools[0] if suggested_tools else "llm_response",
                    purpose="Xử lý câu hỏi chính",
                    expected_outcome="Người dùng nhận được câu trả lời"
                )
            ],
            tools_to_use=suggested_tools[:2] if len(suggested_tools) > 1 else suggested_tools,
            estimated_duration="5-8 phút",
            personalization_notes=f"Tập trung vào chủ đề đang học{learning_context_goal}"
        )

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