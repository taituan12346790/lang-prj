# app/core/strategy.py
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from loguru import logger
import traceback

from app.llm.llm_client import LLMClient
from app.core.language_parser import LanguageParser
from app.models.user_profile import UserProfile


# Whitelist các mode hợp lệ
ALLOWED_MODES = {
    "translation",
    "grammar",
    "exercise",
    "general",
    "conversation",
    "vocabulary",
    "onboarding"
}


class StrategyDecision(BaseModel):
    mode: str
    reasoning: str = Field(..., max_length=250)
    priority_focus: List[str] = Field(default_factory=list)
    suggested_tools: List[str] = Field(default_factory=list)
    difficulty_adjustment: str = "maintain"


class StrategySelector:
    def __init__(self):
        self.parser = LanguageParser()
        self.llm = LLMClient()

    def _fallback_strategy(self, reason: str) -> Dict[str, Any]:
        """Trả về chiến lược mặc định khi không thể quyết định"""
        return {
            "mode": "general",
            "reasoning": reason,
            "priority_focus": [],
            "suggested_tools": [],
            "difficulty_adjustment": "maintain",
            "learning_target": None,
            "teaching_language": "vi",
            "source_language": "unknown",
            "user_explicit_override": False,
            "input_type": "general",
            "personalization": {
                "level": "A1",
                "weak_skills": [],
                "interests": []
            }
        }

    async def decide(
        self,
        user_id: str,
        user_input: str,
        long_mem: UserProfile,
        analytics_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        # Guard: missing profile
        if long_mem is None:
            logger.warning(f"Missing long_mem for user {user_id}, using fallback")
            return self._fallback_strategy("Missing user profile")

        if not user_input or not user_input.strip():
            return self._fallback_strategy("Empty input")

        # Normalize input
        normalized_input = user_input.strip()
        text_lower = normalized_input.lower()

        target_lang = getattr(long_mem, "target_language", None)
        teaching_lang = getattr(long_mem, "teaching_language", None) or "vi"  

        if not target_lang:
            return {
                **self._fallback_strategy("Missing target language"),
                "mode": "onboarding",
                "response": (
                    "Bạn muốn học ngôn ngữ nào? "
                    "Ví dụ: English, Korean, Japanese..."
                )
            }      

        parsed = self.parser.parse(
            normalized_input,
            target_lang,
            teaching_lang
        )

        base_mode = self._rule_based_intent(text_lower)

        # LLM decision with analytics
        decision = await self._llm_decide(normalized_input, long_mem, base_mode, analytics_context)

        if not isinstance(decision, StrategyDecision):
            logger.warning(f"LLM returned invalid type for {user_id}, using fallback")
            decision = StrategyDecision(
                mode=base_mode,
                reasoning="Invalid LLM response, using fallback"
            )

        # Validate mode
        mode = decision.mode
        if mode not in ALLOWED_MODES:
            logger.warning(f"Invalid mode from LLM: {mode}, falling back to {base_mode}")
            mode = base_mode

        # Normalize priority_focus
        priority_focus = decision.priority_focus
        if not isinstance(priority_focus, list):
            priority_focus = []
        priority_focus = list(dict.fromkeys(priority_focus))[:3]

        # Normalize suggested_tools
        suggested_tools = decision.suggested_tools
        if not isinstance(suggested_tools, list):
            suggested_tools = []
        suggested_tools = list(dict.fromkeys(suggested_tools))

        final_strategy = {
            "mode": mode,
            "reasoning": decision.reasoning,
            "priority_focus": priority_focus,
            "suggested_tools": suggested_tools,
            "difficulty_adjustment": decision.difficulty_adjustment,

            "learning_target": target_lang,
            "teaching_language": teaching_lang,
            "source_language": parsed.get("source_lang", "unknown"),

            "user_explicit_override": parsed.get("user_explicit_override", False),
            "input_type": parsed.get("input_type", "general"),

            "personalization": {
                "level": getattr(long_mem, 'current_level', 'A1'),
                "weak_skills": list(long_mem.weak_skills.keys())[:5] if long_mem.weak_skills else [],
                "interests": long_mem.interests[-5:] if long_mem.interests else [],
            }
        }

        logger.info(
            f"[Strategy] User={user_id} | Mode={final_strategy['mode']} "
            f"| InputType={final_strategy['input_type']}"
        )
        return final_strategy

    def _rule_based_intent(self, text_lower: str) -> str:
        # Translation: có thể refine sau
        if any(k in text_lower for k in ["dịch", "translate"]):
            return "translation"
        if "nghĩa" in text_lower:
            return "translation"
        if any(k in text_lower for k in ["sửa", "grammar", "ngữ pháp", "cấu trúc", "thì"]):
            return "grammar"
        if any(k in text_lower for k in ["bài tập", "exercise", "luyện", "quiz"]):
            return "exercise"
        return "general"

    async def _llm_decide(
        self,
        user_input: str,
        long_mem: UserProfile,
        base_mode: str,
        analytics_context: Optional[Dict[str, Any]] = None
    ) -> StrategyDecision:
        weak_skills = getattr(long_mem, 'weak_skills', None)
        weak_skills_str = ", ".join(list(weak_skills.keys())[:6]) if weak_skills else "None"
        target_lang = getattr(long_mem, 'target_language', None) or "Unknown"
        current_level = getattr(long_mem, 'current_level', 'A1')
        
        # Add analytics info to prompt
        analytics_info = ""
        if analytics_context:
            weak_from_analytics = analytics_context.get("weak_skills", {})
            if weak_from_analytics:
                top_weak = sorted(weak_from_analytics.items(), key=lambda x: x[1])[:3]
                analytics_info = f"\nWeak skills from recent quizzes: {', '.join([f'{s} ({a*100:.0f}%)' for s, a in top_weak])}"
            
            if analytics_context.get("needs_review"):
                analytics_info += f"\n⚠️ User has {analytics_context.get('due_reviews_count', 0)} topics due for review (spaced repetition)"
        
        # Add learning context (active topic/lesson) - CRITICAL for topic awareness
        learning_context_str = ""
        priority_focus = []
        if analytics_context and "learning_context" in analytics_context:
            lc = analytics_context["learning_context"]
            learning_context_str = f"\n\n🎯 ACTIVE LEARNING CONTEXT:\nTopic: {lc.get('topic_name', 'N/A')} ({lc.get('topic_name_vi', '')})\nLevel: {lc.get('level', 'N/A')}\nGrammar Focus: {', '.join(lc.get('grammar_focus', []))}"
            if "lesson_title" in lc:
                learning_context_str += f"\nCurrent Lesson: {lc.get('lesson_title', '')} ({lc.get('lesson_type', '')})"
            learning_context_str += "\n\n⚠️ IMPORTANT: User is currently studying this topic. Prioritize responses related to this topic's content and grammar focus!"
            
            # Extract priority focus from grammar_focus
            priority_focus = lc.get('grammar_focus', [])[:3]

        # Phase 2: Enable LLM structured call for intelligent strategy decision
        system_prompt = f"""You are a Strategy Selector for an AI Language Tutor.

Target Language: {target_lang}
User Level: {current_level}
Weak Skills: {weak_skills_str}
{analytics_info}
{learning_context_str}

Base mode from keywords: {base_mode}

User input: "{user_input}"

Choose the best teaching mode and suggest tools. Consider:
1. If user is in active learning context, prioritize that topic's focus
2. Weak skills should influence difficulty and focus
3. Due reviews should trigger review mode if appropriate

Return JSON:
{{
  "mode": "grammar|translation|exercise|vocabulary|conversation|general",
  "reasoning": "short explanation",
  "priority_focus": ["grammar_point1", "grammar_point2"],
  "suggested_tools": ["translator", "grammar_checker", "exercise_generator", "llm_response"],
  "difficulty_adjustment": "increase|decrease|maintain"
}}
"""
        
        try:
            decision_dict = await self.llm.generate_structured_async(
                user_input=user_input,
                system_prompt=system_prompt,
                response_model=StrategyDecision,
                temperature=0.3
            )
            
            if decision_dict and isinstance(decision_dict, dict):
                return StrategyDecision(**decision_dict)
        except Exception as e:
            logger.warning(f"LLM strategy decision failed: {e}, using fallback")
        
        # Fallback if LLM fails
        reasoning = f"Fallback after LLM error: mode={base_mode}"
        if learning_context_str:
            reasoning += f" | Active topic detected"
        
        return StrategyDecision(
            mode=base_mode,
            reasoning=reasoning,
            priority_focus=priority_focus,
            suggested_tools=["llm_response"],
            difficulty_adjustment="maintain"
        )