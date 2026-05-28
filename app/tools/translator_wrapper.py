
from typing import Dict, Any
from loguru import logger

from app.tools.translator import TranslatorTool


class TranslatorWrapper:
    def __init__(self, tool: TranslatorTool):
        self.tool = tool

    async def execute(self, params: Dict[str, Any]) -> Dict:
        try:
            result = await self.tool.execute(params)
            
            # Normalize output - result là TranslationOutput (Pydantic model)
            if hasattr(result, "model_dump"):
                return result.model_dump()
            return result
            
        except Exception as e:
            logger.error(f"TranslatorWrapper error: {e}")
            return {
                "success": False,
                "error": "Dịch thất bại",
                "original_text": params.get("content", "")
            }