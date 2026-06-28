# app/agents/translator_agent.py
"""
Translator Agent: Specialized AI Agent for language translation and vocabulary support.
Role: Provide contextual translations and vocabulary explanations.
"""
from typing import Dict, Any
from loguru import logger

from app.agents.base_agent import AIAgent
from app.tools.translator import TranslatorTool


class TranslatorAgent(AIAgent):
    """
    Translator Agent handles all translation-related tasks:
    - Text translation between languages
    - Contextual vocabulary explanations
    - Idiom and expression handling
    - Bilingual support for vocabulary learning
    """
    
    def __init__(self, tool: TranslatorTool):
        """
        Initialize Translator Agent.
        
        Args:
            tool: TranslatorTool instance
        """
        super().__init__(agent_name="TranslatorAgent", tool_instance=tool)
        self.tool = tool
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute translation task.
        
        Args:
            params: Task parameters (depends on translator implementation)
                - content: Text to translate
                - source_lang: Source language
                - target_lang: Target language
                - context: Optional context for better translation
                
        Returns:
            Dict with translation results
        """
        try:
            logger.debug(f"{self.agent_name} executing translation task")
            
            result = await self.tool.execute(params)
            
            # Normalize output - result có thể là Pydantic model
            if hasattr(result, "model_dump"):
                result = result.model_dump()
            
            logger.debug(f"{self.agent_name} completed task successfully")
            return result
            
        except Exception as e:
            logger.error(f"{self.agent_name} error: {e}")
            return {
                "success": False,
                "error": "Dịch thất bại",
                "original_text": params.get("content", ""),
                "details": str(e)
            }
