# app/tools/wrappers/exercise_wrapper.py
from typing import Dict, Any
from loguru import logger

from app.tools.exercise_generator import ExerciseGenerator


class ExerciseWrapper:
    def __init__(self, tool: ExerciseGenerator = None):
        self.tool = tool

    async def execute(self, params: Dict[str, Any]) -> Dict:
        try:
            return await self.tool.generate_async(
                topic=params.get("topic", "general"),
                cefr_level=params.get("cefr_level", "B1"),
                user_weaknesses=params.get("weaknesses", []),
                num_exercises=params.get("num", 5),
                lesson_type=params.get("lesson_type", "both")
            )
        except Exception as e:
            logger.error(f"ExerciseWrapper error: {e}")
            return {
                "success": False,
                "error": "Tạo bài tập thất bại",
                "exercises": []
            }