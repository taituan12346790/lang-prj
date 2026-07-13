# app/core/reflector_enhanced.py
"""
Enhanced Reflector for Auto Profile Update
After each AI response, analyze learning and update weak/strong skills
"""

from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.llm.llm_client import LLMClient
from app.models.user_topic_progress import UserTopicProgress
from app.models.conversation import Conversation


class ReflectorEnhanced:
    """Enhanced reflector that updates user weak/strong skills"""

    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = """Bạn là Reflector cho AI Language Tutor.
Nhiệm vụ:
- Phân tích cuộc hội thoại giữa AI và học viên
- Xác định chủ đề/kỹ năng được thảo luận
- Đánh giá mức độ hiểu biết của học viên
- Gợi ý kỹ năng yếu nếu có
- Phát hiện hoạt động học (lesson, practice, quiz, vocabulary)

Trả về JSON với:
{
  "topics_discussed": ["past_tense", "vocabulary"],
  "weak_skills": ["past_tense"],
  "strong_skills": ["vocabulary"],
  "engagement_level": "high|medium|low",
  "understanding": "poor|fair|good|excellent",
  "chat_activity": {
    "type": "lesson|practice|quiz|vocabulary|none",
    "title": "Past Simple",
    "custom_topic": "du lịch",
    "skill_tags": ["past_tense"],
    "items": [
      {
        "question": "She ___ to school yesterday.",
        "user_answer": "go",
        "correct_answer": "went",
        "is_correct": false,
        "skill_tag": "past_tense"
      }
    ],
    "summary": "Giải thích về thì quá khứ...",
    "key_points": ["V2", "yesterday"],
    "examples": ["I went", "She studied"],
    "words": [{"word": "luggage", "meaning": "hành lý"}]
  }
}

⚠️ CRITICAL - Phân loại chính xác theo STAGE:

**Detect by AI response structure:**

1. type="lesson" - Stage 1 & 2: Theory + Examples
   - AI có headers: "PHẦN 1: LÝ THUYẾT", "PHẦN 2: VÍ DỤ"
   - AI giải thích grammar rules, cấu trúc, khái niệm
   - Có "Khái niệm", "Công thức", "Ví dụ"
   - User hỏi: "giải thích...", "cách dùng...", "khác nhau như thế nào..."
   → Cần: title, summary, key_points, examples

2. type="vocabulary" - Vocabulary teaching
   - AI có header: "TỪ VỰNG", "VOCABULARY"
   - AI dạy từ vựng mới (5+ words)
   - User hỏi: "cho tôi từ vựng về...", "các từ liên quan đến..."
   - Có danh sách từ với nghĩa
   → Cần: title, words=[{word, meaning}], custom_topic

3. type="practice" - Stage 3: Practice exercises
   - AI có header: "PHẦN 3: LUYỆN TẬP", "PRACTICE"
   - AI đưa 3-5 bài tập cụ thể, numbered
   - AI nói "Hãy làm bài tập", "Gửi câu trả lời"
   - OR User đang submit answers và AI chấm điểm
   → Cần: title, items=[{question, user_answer, correct_answer, is_correct, skill_tag}]
   
   **Important:** If AI just ASSIGNED exercises (hasn't graded yet), create items with:
   - question: [the exercise question]
   - user_answer: null (not answered yet)
   - correct_answer: null
   - is_correct: null
   - skill_tag: [relevant skill]

4. type="quiz" - Stage 4: Quiz/Test
   - AI có header: "PHẦN 4: KIỂM TRA", "QUIZ"
   - User làm nhiều câu hỏi liên tiếp (3+)
   - Có format câu hỏi rõ ràng: multiple choice, true/false, fill blank
   - OR AI chấm quiz và tính điểm
   → Cần: title, items=[...], score

5. type="none" - Chat thường
   - Xã giao, không có nội dung học
   - "xin chào", "cảm ơn", "tạm biệt"

**Special cases:**

- If AI response has BOTH theory explanation AND practice exercises → type="lesson" (Stage 1+2+3 combined)
- If User submitted answers and AI is correcting → type="practice" with is_correct values
- If conversation just started (no previous learning) → likely "lesson"
- If building on previous lesson → check what stage we're at

**Priority detection:**
1. Check for stage headers (PHẦN 1, PHẦN 2, PHẦN 3, PHẦN 4)
2. If has 5+ vocabulary words → "vocabulary"
3. If has grammar explanation with công thức → "lesson"
4. If has numbered exercises AND asking user to submit → "practice"
5. If has quiz format (multiple choice, T/F) → "quiz"
6. If correcting user's answers → "practice"
"""

    async def reflect_and_update(
        self,
        user_id: UUID,
        user_input: str,
        ai_response: str,
        current_topic_id: Optional[UUID],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Analyze conversation and update user weak/strong skills
        Called after each AI response
        
        Returns:
            {
                "updated": bool,
                "weak_skills": [...],
                "strong_skills": [...],
                "topics_discussed": [...],
                "engagement": "high|medium|low"
            }
        """
        try:
            # Extract insights from conversation
            insights = await self._analyze_conversation(
                user_input=user_input,
                ai_response=ai_response,
                current_topic_id=current_topic_id
            )

            # Update user's weak/strong skills in relevant topics
            updated_topics = []
            if current_topic_id:
                updated = await self._update_topic_skills(
                    user_id=user_id,
                    topic_id=current_topic_id,
                    weak_skills=insights.get("weak_skills", []),
                    strong_skills=insights.get("strong_skills", []),
                    db=db
                )
                if updated:
                    updated_topics.append(str(current_topic_id))

            logger.info(
                f"Reflector updated {len(updated_topics)} topics for user {user_id}"
            )

            return {
                "updated": len(updated_topics) > 0,
                "weak_skills": insights.get("weak_skills", []),
                "strong_skills": insights.get("strong_skills", []),
                "topics_discussed": insights.get("topics_discussed", []),
                "engagement": insights.get("engagement_level", "medium"),
                "understanding": insights.get("understanding", "fair"),  # Fixed: was "understanding_level"
                "updated_topics": updated_topics,
                "chat_activity": insights.get("chat_activity"),  # NEW: Pass chat activity data
            }

        except Exception as e:
            logger.exception(f"Reflector error for user {user_id}: {e}")
            return {
                "updated": False,
                "weak_skills": [],
                "strong_skills": [],
                "topics_discussed": [],
                "engagement": "medium",
                "error": str(e),
                "chat_activity": {"type": "none"},  # Add missing field
            }

    async def _analyze_conversation(
        self,
        user_input: str,
        ai_response: str,
        current_topic_id: Optional[UUID]
    ) -> Dict[str, Any]:
        """
        Use LLM to analyze conversation and extract insights
        DISABLED: To save tokens and avoid rate limit
        """
        # DISABLED: Skip LLM analysis to save ~2400 tokens per request
        logger.info("⏭️  Skipping LLM conversation analysis (disabled to save tokens)")
        return {
            "topics_discussed": [],
            "weak_skills": [],
            "strong_skills": [],
            "engagement_level": "medium",
            "understanding": "fair",
            "chat_activity": {"type": "none"},
        }

    async def _update_topic_skills(
        self,
        user_id: UUID,
        topic_id: UUID,
        weak_skills: List[str],
        strong_skills: List[str],
        db: AsyncSession
    ) -> bool:
        """
        Update user's weak_skills/strong_skills for a topic
        """
        try:
            # Get or create progress record
            progress_result = await db.execute(
                select(UserTopicProgress).where(
                    UserTopicProgress.user_id == user_id,
                    UserTopicProgress.topic_id == topic_id,
                )
            )
            progress = progress_result.scalar_one_or_none()

            if not progress:
                logger.warning(
                    f"No progress found for user {user_id} on topic {topic_id}"
                )
                return False

            # Get current weak_skills dict
            current_weak_skills = progress.weak_skills or {}
            if isinstance(current_weak_skills, str):
                import json
                current_weak_skills = json.loads(current_weak_skills)

            # Update with new weak skills (score = 0.3 to 0.7 for weak)
            for skill in weak_skills:
                if skill not in current_weak_skills:
                    current_weak_skills[skill] = 0.4
                else:
                    # Decrease score (weaker)
                    current_weak_skills[skill] = max(0.0, current_weak_skills[skill] - 0.1)

            # Update with strong skills (score = 0.8+ for strong)
            for skill in strong_skills:
                if skill in current_weak_skills:
                    # Increase score (stronger)
                    current_weak_skills[skill] = min(1.0, current_weak_skills[skill] + 0.15)
                else:
                    current_weak_skills[skill] = 0.85

            # Save back to database
            progress.weak_skills = current_weak_skills
            await db.commit()

            logger.info(
                f"Updated skills for user {user_id} on topic {topic_id}: "
                f"weak={len(weak_skills)}, strong={len(strong_skills)}"
            )
            return True

        except Exception as e:
            logger.exception(f"Error updating topic skills: {e}")
            return False
