from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from enum import Enum
import logging
import asyncio

logger = logging.getLogger(__name__)

EXERCISE_SYSTEM_PROMPT = """Bạn là giáo viên ngoại ngữ chuyên nghiệp, am hiểu sâu CEFR.
Tạo nội dung rõ ràng, logic, thực tế và phù hợp với học viên người Việt.
Chỉ trả về JSON thuần theo đúng schema được yêu cầu.
KHÔNG thêm markdown, KHÔNG code block, KHÔNG giải thích thêm."""


# ========================== MODELS ==========================
class ExerciseType(str, Enum):
    multiple_choice = "multiple_choice"
    fill_in_blank = "fill_in_blank"
    sentence_transformation = "sentence_transformation"
    writing = "writing"
    matching = "matching"
    open_question = "open_question"


class DifficultyLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class VocabularyItem(BaseModel):
    word: str
    meaning: str
    example: str
    pronunciation: Optional[str] = None


class Exercise(BaseModel):
    exercise_type: ExerciseType
    question: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str
    difficulty: DifficultyLevel


class ExerciseList(BaseModel):
    exercises: List[Exercise]


class LessonSection(BaseModel):
    title: str
    content: str
    key_points: List[str] = Field(default_factory=list)
    examples: List[str] = Field(default_factory=list)
    common_mistakes: Optional[List[str]] = None


class FullLesson(BaseModel):
    topic: str
    cefr_level: str
    objective: str
    sections: List[LessonSection] = Field(..., min_items=1, max_items=5)
    vocabulary: List[VocabularyItem] = Field(..., max_items=12)
    exercises: List[Exercise] = Field(..., max_items=8)
    practice_suggestion: str


class LessonOnly(BaseModel):
    topic: str
    cefr_level: str
    objective: str
    sections: List[LessonSection] = Field(..., min_items=1, max_items=5)
    vocabulary: List[VocabularyItem] = Field(..., max_items=12)
    practice_suggestion: str


class ExerciseGenerator:
    """Exercise Generator"""

    def __init__(self, llm):
        self.llm = llm
        self.max_retries = 3
        self.timeout_seconds = 50

    async def _safe_generate(self, user_prompt: str, response_format, lesson_type: str, temperature: float):
        for attempt in range(self.max_retries):
            try:
                logger.info(f"ExerciseGenerator [{lesson_type}] Attempt {attempt+1}/{self.max_retries}")

                result = await asyncio.wait_for(
                    self.llm.generate_structured_async(
                        system_prompt=EXERCISE_SYSTEM_PROMPT,
                        user_prompt=user_prompt,
                        response_format=response_format,
                        temperature=temperature,
                        max_retries=0,
                    ),
                    timeout=self.timeout_seconds,
                )
                if result is not None:
                    return result

            except asyncio.TimeoutError:
                logger.warning(f"Timeout at attempt {attempt+1}")
            except ValidationError as ve:
                logger.warning(f"Validation failed (attempt {attempt+1}): {ve}")
            except Exception as e:
                error_str = str(e).lower()
                if any(x in error_str for x in ["rate limit", "timeout", "connection", "overloaded", "busy"]):
                    logger.warning(f"Retryable error (attempt {attempt+1}): {e}")
                else:
                    logger.error(f"Non-retryable error: {e}")
                    raise

            if attempt < self.max_retries - 1:
                await asyncio.sleep(2 ** attempt)

        logger.error(f"ExerciseGenerator failed after {self.max_retries} attempts")
        return None

    def _get_robust_fallback(self, lesson_type: str, topic: str, cefr_level: str) -> Dict:
        fallback = {
            "topic": topic or "General English",
            "cefr_level": cefr_level,
            "objective": "Có lỗi khi tạo nội dung. Vui lòng thử lại sau.",
            "sections": [],
            "vocabulary": [],
            "practice_suggestion": "Hãy thử lại với chủ đề khác."
        }

        if lesson_type == "exercise_only":
            return {"exercises": []}
        elif lesson_type == "lesson_only":
            return fallback
        else:
            fallback["exercises"] = []
            return fallback

    async def generate_async(
        self,
        topic: str,
        cefr_level: str = "B1",
        user_weaknesses: Optional[List[str]] = None,
        num_exercises: int = 5,
        lesson_type: str = "both"
    ) -> Dict[str, Any]:
        
        weaknesses_str = ", ".join(user_weaknesses) if user_weaknesses else "không có"

        user_input = f"""
Chủ đề: {topic}
Level: {cefr_level}
Điểm yếu: {weaknesses_str}
Số bài tập: {num_exercises}

Yêu cầu:
- Ngôn ngữ đơn giản, dễ hiểu với người Việt
- Tập trung khắc phục điểm yếu
- Nội dung thực tế, ứng dụng cao
- Tối đa 5 sections, 12 từ vựng, 8 bài tập
"""

        if lesson_type in ["lesson_only", "both"]:
            user_input += "\nTạo bài học đầy đủ."
        if lesson_type in ["exercise_only", "both"]:
            user_input += "\nTạo bài tập đa dạng kèm đáp án và giải thích."

        try:
            if lesson_type == "lesson_only":
                response_format = LessonOnly
                temperature = 0.35
            elif lesson_type == "exercise_only":
                response_format = ExerciseList
                temperature = 0.3
            else:
                response_format = FullLesson
                temperature = 0.35

            result = await self._safe_generate(
                user_input.strip(),
                response_format,
                lesson_type,
                temperature,
            )

            if result is None:
                return self._get_robust_fallback(lesson_type, topic, cefr_level)

            if hasattr(result, "model_dump"):
                data = result.model_dump()
                if lesson_type == "exercise_only" and isinstance(result, ExerciseList):
                    data = {"exercises": data.get("exercises", [])}
                return data

            return result

        except Exception as e:
            logger.error(f"Unexpected error in generate_async: {e}")
            return self._get_robust_fallback(lesson_type, topic, cefr_level)

    # Convenience methods
    async def generate_exercises_only(self, topic: str, cefr_level: str, user_weaknesses=None, num=6):
        return await self.generate_async(topic, cefr_level, user_weaknesses, num, "exercise_only")

    async def generate_full_lesson(self, topic: str, cefr_level: str, user_weaknesses=None):
        return await self.generate_async(topic, cefr_level, user_weaknesses, lesson_type="lesson_only")