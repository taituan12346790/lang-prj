# app/agents/base_agent.py
"""
Base class for all AI Agents in the system.
Each agent is a specialized worker that handles a specific learning domain.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from loguru import logger


class AIAgent(ABC):
    """
    Base class for all AI agents in the multi-agent system.
    
    Each agent:
    - Has a specific role (Grammar Checker, Exercise Generator, Translator)
    - Receives requests with parameters
    - Returns structured results
    - Can fail gracefully with error handling
    """
    
    def __init__(self, agent_name: str, tool_instance=None):
        """
        Initialize AI Agent.
        
        Args:
            agent_name: Name of the agent (e.g., "GrammarAgent", "ExerciseAgent")
            tool_instance: The underlying tool that this agent wraps
        """
        self.agent_name = agent_name
        self.tool = tool_instance
        logger.info(f"🤖 Initialized {agent_name}")
    
    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task.
        
        Args:
            params: Parameters for the task
            
        Returns:
            Dict with results or error info
        """
        pass
    
    async def _safe_execute(self, params: Dict[str, Any], error_message: str) -> Dict[str, Any]:
        """
        Safely execute a task with error handling.
        
        Args:
            params: Task parameters
            error_message: Custom error message if execution fails
            
        Returns:
            Result dict or error dict
        """
        try:
            return await self.execute(params)
        except Exception as e:
            logger.error(f"{self.agent_name} error: {e}")
            return {
                "success": False,
                "error": error_message,
                "details": str(e)
            }
