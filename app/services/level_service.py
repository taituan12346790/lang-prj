from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.schemas.test import (
    PlacementTestResponse,
    LevelUpTestResult,
    Level,
    SkillType,
    TestType
)


class LevelService:
    async def placement_test(
        self,
        user_id: str,
        answers: Dict[str, str],
        db: AsyncSession
    ) -> PlacementTestResponse:
        try:
            # TODO: replace mock scoring with real answer validation (compare with correct answers from DB)
            total = len(answers)
            correct = int(total * 0.8) if total > 0 else 0
            score = (correct / total) * 100 if total > 0 else 0

            if score >= 85:
                estimated_level = Level.B1
                recommended_focus = ["speaking", "grammar"]
            elif score >= 65:
                estimated_level = Level.A2
                recommended_focus = ["vocabulary", "listening"]
            else:
                estimated_level = Level.A1
                recommended_focus = ["basic_grammar", "vocabulary"]

            strengths = [SkillType.LISTENING] if score > 70 else []
            weaknesses = [SkillType.SPEAKING] if score < 70 else []

            return PlacementTestResponse(
                estimated_level=estimated_level,
                score=round(score, 1),
                strengths=strengths,
                weaknesses=weaknesses,
                recommended_focus=recommended_focus,
                message=f"Level phù hợp: {estimated_level.value}",
                total_questions=total,
                correct_answers=correct
            )
        except Exception:
            logger.exception("Placement test error")
            raise

    async def level_up_test(
        self,
        user_id: str,
        test_type: TestType,
        current_level: Level,
        num_questions: int,
        answers: Dict[str, str],
        db: AsyncSession
    ) -> LevelUpTestResult:
        try:
            answered = min(len(answers), num_questions)
            correct = int(answered * 0.85) if answered > 0 else 0
            score = (correct / num_questions) * 100 if num_questions > 0 else 0
            passed = score >= 75

            new_level = None
            if passed and current_level == Level.A2:
                new_level = Level.B1
            elif passed and current_level == Level.B1:
                new_level = Level.B2

            strengths = [SkillType.GRAMMAR] if score > 80 else []
            weaknesses = [SkillType.SPEAKING] if score < 70 else []

            return LevelUpTestResult(
                passed=passed,
                score=round(score, 1),
                new_level=new_level,
                message="Chúc mừng! Bạn đã đủ điều kiện lên level." if passed else "Cần luyện thêm.",
                strengths=strengths,
                weaknesses=weaknesses,
                recommendation="Luyện speaking và nghe" if not passed else "Thử level cao hơn"
            )
        except Exception:
            logger.exception("Level up test error")
            raise