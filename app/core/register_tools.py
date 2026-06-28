# app/core/register_tools.py
from loguru import logger

from app.tools.tool_registry import tool_registry

# Import Tools
from app.tools.translator import TranslatorTool
from app.tools.exercise_generator import ExerciseGenerator
from app.tools.grammar_checker import GrammarChecker

# Import Agents (replacing wrappers)
from app.agents.translator_agent import TranslatorAgent
from app.agents.grammar_agent import GrammarAgent
from app.agents.exercise_agent import ExerciseAgent


def register_all_tools(llm_client):
    """
    Đăng ký tất cả AI Agents khi ứng dụng khởi động.
    
    The system uses a multi-agent architecture where:
    - GrammarAgent: Handles grammar checking and error analysis
    - ExerciseAgent: Generates personalized exercises
    - TranslatorAgent: Provides translations and vocabulary support
    """
    try:
        # Initialize tool instances
        grammar_tool = GrammarChecker(llm=llm_client)
        translator_tool = TranslatorTool(llm=llm_client)
        exercise_tool = ExerciseGenerator(llm=llm_client)

        # Initialize AI Agents - each is a specialized worker
        grammar_agent = GrammarAgent(tool=grammar_tool)
        translator_agent = TranslatorAgent(tool=translator_tool)
        exercise_agent = ExerciseAgent(tool=exercise_tool)

        # Register agents with multiple aliases for flexibility
        tool_registry.register("translator", translator_agent.execute)
        tool_registry.register("translate", translator_agent.execute)

        tool_registry.register("grammar_check", grammar_agent.execute)
        tool_registry.register("grammar", grammar_agent.execute)
        tool_registry.register("grammar_checker", grammar_agent.execute)

        tool_registry.register("exercise", exercise_agent.execute)
        tool_registry.register("generate_exercises", exercise_agent.execute)
        tool_registry.register("exercise_generator", exercise_agent.execute)
        tool_registry.register("lesson", exercise_agent.execute)

        logger.success("🎉 Multi-agent system initialized successfully!")
        logger.info("  ✓ GrammarAgent registered")
        logger.info("  ✓ ExerciseAgent registered")
        logger.info("  ✓ TranslatorAgent registered")

    except Exception as e:
        logger.error(f"Failed to register agents: {e}")
        raise