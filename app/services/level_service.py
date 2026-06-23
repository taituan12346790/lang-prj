from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.schemas.test import (
    PlacementTestResponse,
    LevelUpTestResult,
    Level,
    SkillType,
    TestType
)
from app.services.test_data import get_test_by_level, get_placement_test


class LevelService:
    async def placement_test(
        self,
        user_id: str,
        answers: Dict[str, str],
        db: AsyncSession
    ) -> PlacementTestResponse:
        try:
            # Get placement test questions and answer key
            questions, answer_key = get_placement_test()
            
            # Calculate score based on correct answers
            total = len(answers)
            correct = 0
            
            for question_id, user_answer in answers.items():
                correct_answer = answer_key.get(question_id)
                if correct_answer and user_answer.strip().lower() == correct_answer.strip().lower():
                    correct += 1
            
            score = (correct / total) * 100 if total > 0 else 0

            # Determine level based on score and performance
            if score >= 87:
                estimated_level = Level.C1
                recommended_focus = ["advanced_speaking", "nuanced_writing"]
            elif score >= 80:
                estimated_level = Level.B2
                recommended_focus = ["professional_english", "advanced_grammar"]
            elif score >= 70:
                estimated_level = Level.B1
                recommended_focus = ["speaking", "complex_grammar"]
            elif score >= 60:
                estimated_level = Level.A2
                recommended_focus = ["vocabulary", "past_tense"]
            else:
                estimated_level = Level.A1
                recommended_focus = ["basic_grammar", "vocabulary"]

            # Analyze strengths/weaknesses by skill type
            strengths = []
            weaknesses = []
            
            for question in questions:
                skill_type = question.get("skill_type")
                question_id = question.get("question_id")
                if question_id in answers:
                    user_answer = answers[question_id]
                    correct_answer = answer_key.get(question_id)
                    if user_answer.strip().lower() == correct_answer.strip().lower():
                        if skill_type not in strengths:
                            strengths.append(skill_type)
                    else:
                        if skill_type not in weaknesses:
                            weaknesses.append(skill_type)

            # B4: Update user profile with estimated level
            from app.models.user_profile import UserProfile
            from sqlalchemy import select
            from uuid import UUID
            
            try:
                result = await db.execute(
                    select(UserProfile).where(UserProfile.user_id == UUID(user_id))
                )
                profile = result.scalar_one_or_none()
                
                if profile:
                    profile.current_level = estimated_level.value
                    profile.placement_score = score  # Store the placement test score
                    db.add(profile)
                    await db.commit()
                    logger.info(f"✅ B4: Updated profile level to {estimated_level.value} (score: {score}%) for user {user_id}")
                else:
                    logger.warning(f"⚠️ B4: No profile found for user {user_id}")
            except Exception as e:
                logger.error(f"❌ B4: Failed to update profile level: {e}")
                await db.rollback()

            return PlacementTestResponse(
                estimated_level=estimated_level,
                score=round(score, 1),
                strengths=strengths,
                weaknesses=weaknesses,
                recommended_focus=recommended_focus,
                message=f"Your estimated level: {estimated_level.value}",
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
            # Get questions for the level
            questions, answer_key = get_test_by_level(current_level)
            
            # Filter questions by test type
            filtered_questions = [q for q in questions if q.get("skill_type").value == test_type.value]
            
            # Limit to requested number of questions
            test_questions = filtered_questions[:num_questions]
            
            # Calculate score
            correct = 0
            for question in test_questions:
                question_id = question.get("question_id")
                if question_id in answers:
                    user_answer = answers[question_id]
                    correct_answer = answer_key.get(question_id)
                    if user_answer.strip().lower() == correct_answer.strip().lower():
                        correct += 1
            
            actual_questions = len(test_questions)
            score = (correct / actual_questions) * 100 if actual_questions > 0 else 0
            passed = score >= 75

            # Determine next level
            new_level = None
            level_progression = {
                Level.A1: Level.A2,
                Level.A2: Level.B1,
                Level.B1: Level.B2,
                Level.B2: Level.C1,
                Level.C1: Level.C2,
            }
            
            if passed and current_level in level_progression:
                new_level = level_progression[current_level]
                
                # Update user's current level in database
                from app.models.user_profile import UserProfile
                from uuid import UUID
                
                profile_result = await db.execute(
                    select(UserProfile).where(UserProfile.user_id == UUID(user_id))
                )
                profile = profile_result.scalar_one_or_none()
                
                if profile:
                    profile.current_level = new_level.value
                    await db.commit()
                    logger.info(f"✅ User {user_id} leveled up: {current_level.value} → {new_level.value}")

            # Analyze skills
            strengths = []
            weaknesses = []
            
            for question in test_questions:
                skill_type = question.get("skill_type")
                question_id = question.get("question_id")
                if question_id in answers:
                    user_answer = answers[question_id]
                    correct_answer = answer_key.get(question_id)
                    if user_answer.strip().lower() == correct_answer.strip().lower():
                        if skill_type not in strengths:
                            strengths.append(skill_type)
                    else:
                        if skill_type not in weaknesses:
                            weaknesses.append(skill_type)

            return LevelUpTestResult(
                passed=passed,
                score=round(score, 1),
                new_level=new_level,
                message="Congratulations! You passed and can level up! 🎉" if passed else "Keep practicing to reach the next level! 💪",
                strengths=strengths,
                weaknesses=weaknesses,
                recommendation="Ready for the next level! Try advanced topics." if passed else "Focus on the weak areas and try again."
            )
        except Exception:
            logger.exception("Level up test error")
            raise
