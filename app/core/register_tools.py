# app/core/register_tools.py
from loguru import logger

from app.tools.tool_registry import tool_registry

# Import Tools
from app.tools.translator import TranslatorTool
from app.tools.exercise_generator import ExerciseGenerator
from app.tools.grammar_checker import GrammarChecker
from app.core.error_analyzer import ErrorAnalyzer
from app.services.writing_service import WritingService

# Import Agents
# 3 Core Agents (from thesis architecture)
from app.agents.error_analyzer_agent import ErrorAnalyzerAgent
from app.agents.exercise_agent import ExerciseAgent
from app.agents.writing_agent import WritingAgent

# Support Agents (helper tools)
from app.agents.translator_agent import TranslatorAgent
from app.agents.grammar_agent import GrammarAgent


def register_all_tools(llm_client):
    """
    Đăng ký tất cả AI Agents khi ứng dụng khởi động.
    
    The system uses a multi-agent architecture with:
    
    **3 Core Agents (from thesis):**
    - ErrorAnalyzerAgent: Analyze student errors and detect skill gaps
    - ExerciseAgent: Generate personalized exercises based on weaknesses
    - WritingAgent: Evaluate writing submissions with detailed feedback
    
    **Support Agents (helper tools):**
    - GrammarAgent: Grammar checking and corrections
    - TranslatorAgent: Translation and vocabulary support
    """
    try:
        # ========================================
        # Initialize tools for Core Agents
        # ========================================
        error_analyzer_tool = ErrorAnalyzer()  # Uses get_llm_client() internally
        exercise_tool = ExerciseGenerator(llm=llm_client)
        writing_service = WritingService()
        
        # ========================================
        # Initialize tools for Support Agents
        # ========================================
        grammar_tool = GrammarChecker(llm=llm_client)
        translator_tool = TranslatorTool(llm=llm_client)

        # ========================================
        # Initialize Core Agents
        # ========================================
        error_analyzer_agent = ErrorAnalyzerAgent(tool=error_analyzer_tool)
        exercise_agent = ExerciseAgent(tool=exercise_tool)
        writing_agent = WritingAgent(service=writing_service)
        
        # ========================================
        # Initialize Support Agents
        # ========================================
        grammar_agent = GrammarAgent(tool=grammar_tool)
        translator_agent = TranslatorAgent(tool=translator_tool)

        # ========================================
        # Register Core Agents
        # ========================================
        tool_registry.register("error_analyzer", error_analyzer_agent.execute)
        tool_registry.register("analyze_error", error_analyzer_agent.execute)
        
        tool_registry.register("exercise", exercise_agent.execute)
        tool_registry.register("generate_exercises", exercise_agent.execute)
        tool_registry.register("exercise_generator", exercise_agent.execute)
        tool_registry.register("lesson", exercise_agent.execute)
        
        tool_registry.register("writing_evaluator", writing_agent.execute)
        tool_registry.register("evaluate_writing", writing_agent.execute)
        tool_registry.register("grade_writing", writing_agent.execute)

        # ========================================
        # Register Support Agents
        # ========================================
        tool_registry.register("grammar_check", grammar_agent.execute)
        tool_registry.register("grammar", grammar_agent.execute)
        tool_registry.register("grammar_checker", grammar_agent.execute)
        
        tool_registry.register("translator", translator_agent.execute)
        tool_registry.register("translate", translator_agent.execute)

        logger.success("🎉 Multi-agent system initialized successfully!")
        logger.info("  ✅ Core Agents:")
        logger.info("     • ErrorAnalyzerAgent registered")
        logger.info("     • ExerciseAgent registered")
        logger.info("     • WritingAgent registered")
        logger.info("  ✅ Support Agents:")
        logger.info("     • GrammarAgent registered")
        logger.info("     • TranslatorAgent registered")

    except Exception as e:
        logger.error(f"Failed to register agents: {e}")
        raise