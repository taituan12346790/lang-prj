# app/agents/error_analyzer_agent.py
"""
Error Analyzer Agent: Specialized AI Agent for error analysis and classification.
Role: Analyze student errors from quizzes/practice and provide detailed feedback.
"""
from typing import Dict, Any
from loguru import logger

from app.agents.base_agent import AIAgent
from app.core.error_analyzer import ErrorAnalyzer


class ErrorAnalyzerAgent(AIAgent):
    """
    Error Analyzer Agent handles error analysis tasks:
    - Classify errors from quiz answers
    - Detect skill gaps from practice
    - Track weak areas over time
    - Provide targeted learning suggestions
    """
    
    def __init__(self, tool: ErrorAnalyzer):
        """
        Initialize Error Analyzer Agent.
        
        Args:
            tool: ErrorAnalyzer instance
        """
        super().__init__(agent_name="ErrorAnalyzerAgent", tool_instance=tool)
        self.tool = tool
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute error analysis task.
        
        Args:
            params: Must contain:
                - question: The question text
                - user_answer: User's answer
                - correct_answer: Correct answer
                - skill_tag: Optional skill tag hint
                
        Returns:
            Dict with error classification and analysis
        """
        try:
            logger.debug(f"{self.agent_name} analyzing error")
            
            result = await self.tool.analyze(
                question=params.get("question", ""),
                user_answer=params.get("user_answer", ""),
                correct_answer=params.get("correct_answer", ""),
                skill_tag=params.get("skill_tag")
            )
            
            logger.debug(f"{self.agent_name} completed analysis successfully")
            return result
            
        except Exception as e:
            logger.error(f"{self.agent_name} error: {e}")
            return {
                "success": False,
                "error": "Phân tích lỗi thất bại",
                "detected_skill": "unknown",
                "details": str(e)
            }
