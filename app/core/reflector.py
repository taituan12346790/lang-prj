# app/core/reflector.py
from typing import Dict, Any
from loguru import logger
import json

from app.llm.llm_client import LLMClient
from app.memory.memory_service import MemoryService


class Reflector:
    def __init__(self):
        self.llm = LLMClient()
        self.memory_service = MemoryService()

        self.system_prompt = """Bạn là Reflector cho AI Language Tutor.
Nhiệm vụ:
- Phân tích ngắn gọn chất lượng phản hồi
- Gợi ý cải thiện personalization
- Phát hiện kỹ năng yếu nếu có"""

    async def reflect(self, 
                      user_input: str, 
                      assistant_response: str,
                      user_id: str,
                      strategy: Dict = None,
                      plan: Dict = None) -> Dict[str, Any]:
        
        try:
            context = f"""
User Input: {user_input}
Assistant Response: {assistant_response[:800]}
Strategy Mode: {strategy.get('mode') if strategy else 'unknown'}
Plan Goal: {plan.get('overall_goal') if plan else 'unknown'}
"""

            prompt = f"""{self.system_prompt}

{context}

Hãy phân tích và trả về JSON:
{{
  "strengths": ["clear_explanation"],
  "weaknesses": ["too_difficult"],
  "user_engagement": "low|medium|high",
  "suggested_weak_skills": ["past_tense", ...] hoặc [],
  "learning_progress": "Tóm tắt ngắn",
  "update_profile": true/false
}}
"""

            reflection = await self.llm.generate(
                prompt=prompt,
                temperature=0.5,
                max_tokens=700,
                response_format={"type": "json_object"}
            )

            reflection_dict = reflection if isinstance(reflection, dict) else json.loads(reflection)

            # Cập nhật long-term memory nếu cần
            if reflection_dict.get("update_profile", False):
                await self.memory_service.update_long_term_from_reflection(user_id, reflection_dict)

            return reflection_dict

        except Exception:
            logger.exception("Reflector failed")
            return {
                "strengths": "Normal response",
                "weaknesses": "",
                "user_engagement": "medium",
                "suggested_weak_skills": [],
                "update_profile": False
            }