# app/core/register_tools.py
from loguru import logger

from app.tools.tool_registry import tool_registry

# Import Tools
from app.tools.translator import TranslatorTool
from app.tools.exercise_generator import ExerciseGenerator
from app.tools.grammar_checker import GrammarChecker

# Import Wrappers
from app.tools.translator_wrapper import TranslatorWrapper
from app.tools.grammar_checker_wrapper import GrammarCheckerWrapper
from app.tools.exercise_generator_wrapper import ExerciseWrapper


def register_all_tools(llm_client):
    """
    Đăng ký tất cả tools + wrappers khi ứng dụng khởi động
    """
    try:
        # Khởi tạo tool instances - truyền llm_client cho cả 3 tools
        grammar_tool = GrammarChecker(llm=llm_client)
        translator_tool = TranslatorTool(llm=llm_client)
        exercise_tool = ExerciseGenerator(llm=llm_client)

        # Khởi tạo wrappers - truyền tool instances
        grammar_wrapper = GrammarCheckerWrapper(tool=grammar_tool)
        translator_wrapper = TranslatorWrapper(tool=translator_tool)
        exercise_wrapper = ExerciseWrapper(tool=exercise_tool)

        # Đăng ký vào registry
        tool_registry.register("translator", translator_wrapper.execute)
        tool_registry.register("translate", translator_wrapper.execute)

        tool_registry.register("grammar_check", grammar_wrapper.execute)
        tool_registry.register("grammar", grammar_wrapper.execute)

        tool_registry.register("exercise", exercise_wrapper.execute)
        tool_registry.register("generate_exercises", exercise_wrapper.execute)
        tool_registry.register("lesson", exercise_wrapper.execute)

        logger.success("🎉 All tools and wrappers registered successfully!")

    except Exception as e:
        logger.error(f"Failed to register tools: {e}")
        raise