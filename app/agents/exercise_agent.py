# app/agents/exercise_agent.py
"""
Exercise Agent: Specialized AI Agent for exercise generation and adaptive practice.
Role: Generate personalized exercises based on student level, weaknesses, and learning context.
"""
from typing import Dict, Any
from loguru import logger

from app.agents.base_agent import AIAgent
from app.tools.exercise_generator import ExerciseGenerator


class ExerciseAgent(AIAgent):
    """
    Exercise Agent handles all exercise-related tasks:
    - Exercise generation based on CEFR levels
    - Adaptive difficulty adjustment
    - Topic-specific practice problems
    - Student weakness remediation through targeted exercises
    """
    
    def __init__(self, tool: ExerciseGenerator):
        """
        Initialize Exercise Agent.
        
        Args:
            tool: ExerciseGenerator instance
        """
        super().__init__(agent_name="ExerciseAgent", tool_instance=tool)
        self.tool = tool
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute exercise generation task.
        
        Args:
            params: Must contain:
                - topic: Learning topic (default: general)
                - cefr_level: CEFR level (A1-C2, default: B1)
                - weaknesses: Known weak areas to focus on
                - num: Number of exercises to generate (default: 5)
                - lesson_type: Type of lesson (grammar/vocabulary/both)
                
        Returns:
            Dict with generated exercises
        """
        try:
            logger.debug(f"{self.agent_name} executing exercise generation")
            
            result = await self.tool.generate_async(
                topic=params.get("topic", "general"),
                cefr_level=params.get("cefr_level", "B1"),
                user_weaknesses=params.get("weaknesses", []),
                num_exercises=params.get("num", 5),
                lesson_type=params.get("lesson_type", "both")
            )
            
            logger.debug(f"{self.agent_name} completed task successfully")
            return result
            
        except Exception as e:
            logger.error(f"{self.agent_name} error: {e}")
            return {
                "success": False,
                "error": "Tạo bài tập thất bại",
                "exercises": [],
                "details": str(e)
            }
