# app/services/quiz_enhanced.py
"""Enhanced quiz service - links quiz results to chat"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.models.user_topic_progress import UserTopicProgress
from app.services.topic_service import TopicService
from app.schemas.learning import QuizSubmitRequest, QuizSubmitResponse


class QuizEnhancedService:
    """Quiz service with chat integration"""

    @staticmethod
    async def submit_quiz_with_chat_context(
        topic_id: UUID,
        user_id: UUID,
        request: QuizSubmitRequest,
        db: AsyncSession,
    ) -> Dict[str, Any]:
        """
        Submit quiz and prepare context for AI review if needed
        Returns: quiz results + weak_skills for AI Tutor
        """
        # 1. Submit quiz (existing logic)
        quiz_response: QuizSubmitResponse = await TopicService().submit_quiz(
            topic_id=topic_id,
            user_id=user_id,
            request=request,
            db=db,
        )

        # 2. Extract wrong answers for AI review
        weak_skills = []
        for result in quiz_response.results:
            if not result.is_correct:
                weak_skills.append({
                    "question": result.question,
                    "user_answer": result.your_answer,
                    "correct_answer": result.correct_answer,
                    "explanation": result.explanation,
                    "question_id": result.id,
                })

        # 3. Update user_topic_progress with weak skills
        from sqlalchemy import select
        prog_result = await db.execute(
            select(UserTopicProgress).where(
                UserTopicProgress.user_id == user_id,
                UserTopicProgress.topic_id == topic_id,
            )
        )
        prog = prog_result.scalar_one_or_none()
        if prog and weak_skills:
            prog.weak_skills = {
                "from_quiz": weak_skills,
                "count": len(weak_skills),
            }
            await db.commit()

        logger.info(
            f"✅ Quiz submitted for {user_id}, weak_skills: {len(weak_skills)}"
        )

        # 4. Return with AI context
        return {
            "quiz_response": quiz_response.model_dump(),
            "weak_skills": weak_skills,
            "ai_review_enabled": len(weak_skills) > 0,
            "ai_review_prompt": build_quiz_review_prompt(weak_skills),
            "topic_id": str(topic_id),
        }


def build_quiz_review_prompt(weak_skills: List[Dict[str, str]]) -> str:
    """Build AI prompt for quiz review"""
    if not weak_skills:
        return ""

    prompt = "[QUIZ REVIEW MODE]\n"
    prompt += f"Học viên vừa làm quiz sai {len(weak_skills)} câu:\n\n"

    for i, item in enumerate(weak_skills, 1):
        prompt += f"{i}. Câu: {item['question']}\n"
        prompt += f"   Trả lời: {item['user_answer']}\n"
        prompt += f"   Đúng: {item['correct_answer']}\n"
        prompt += f"   Giải thích: {item['explanation']}\n\n"

    prompt += "Hãy giải thích chi tiết về những lỗi này, "
    prompt += "cho ví dụ minh họa, và đưa ra 5 bài tập tương tự để học viên luyện tập.\n"
    prompt += "Trả lời TOÀN BỘ trong một message duy nhất."

    return prompt
