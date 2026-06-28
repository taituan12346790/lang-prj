# app/agents/grammar_agent.py
"""
Grammar Agent: Specialized AI Agent for grammar checking and error analysis.
Role: Analyze student writing and provide grammar corrections with explanations.
"""
from typing import Dict, Any
from loguru import logger

from app.agents.base_agent import AIAgent
from app.tools.grammar_checker import GrammarChecker


class GrammarAgent(AIAgent):
    """
    Grammar Agent handles all grammar-related tasks:
    - Grammar checking
    - Error detection and classification
    - Explanation of grammar rules
    - Personalized correction suggestions
    """
    
    def __init__(self, tool: GrammarChecker):
        """
        Initialize Grammar Agent.
        
        Args:
            tool: GrammarChecker instance
        """
        super().__init__(agent_name="GrammarAgent", tool_instance=tool)
        self.tool = tool
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute grammar checking task.
        
        Args:
            params: Must contain:
                - content: Text to check
                - target_lang: Target language (default: English)
                - teaching_lang: Teaching language (default: Vietnamese)
                - weaknesses: Optional list of known weak areas
                
        Returns:
            Dict with grammar errors and corrections
        """
        try:
            logger.debug(f"{self.agent_name} executing grammar check")
            
            result = await self.tool.check(
                text=params.get("content", ""),
                target_lang=params.get("target_lang", "English"),
                teaching_lang=params.get("teaching_lang", "Vietnamese"),
                user_weaknesses=params.get("weaknesses", [])
            )
            
            logger.debug(f"{self.agent_name} completed task successfully")
            return result
            
        except Exception as e:
            logger.error(f"{self.agent_name} error: {e}")
            return {
                "success": False,
                "error": "Kiểm tra ngữ pháp thất bại",
                "original_text": params.get("content", ""),
                "details": str(e)
            }
