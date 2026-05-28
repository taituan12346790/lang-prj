# app/tools/wrappers/grammar_wrapper.py
from typing import Dict, Any
from loguru import logger

from app.tools.grammar_checker import GrammarChecker


class GrammarCheckerWrapper:
    def __init__(self, tool: GrammarChecker):
        self.tool = tool

    async def execute(self, params: Dict[str, Any]) -> Dict:
        try:
            return await self.tool.check(
                text=params.get("content", ""),
                target_lang=params.get("target_lang", "English"),
                teaching_lang=params.get("teaching_lang", "Vietnamese"),
                user_weaknesses=params.get("weaknesses", [])
            )
        except Exception as e:
            logger.error(f"GrammarCheckerWrapper error: {e}")
            return {
                "success": False,
                "error": "Kiểm tra ngữ pháp thất bại",
                "original_text": params.get("content", "")
            }