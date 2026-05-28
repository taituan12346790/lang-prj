# app/memory/memory_service.py
from typing import Dict, Any, Tuple, Optional
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from .long_term import LongTermMemory
from .short_term import ShortTermMemory
from app.models.user_profile import UserProfile


class MemoryService:
    """
    Memory Service chính - Orchestrator cho Long-term & Short-term Memory
    """

    def __init__(self):
        self.long_term = LongTermMemory()
        # In-memory short-term cache (temporary, non-persistent)
        # Lưu ý: Restart server sẽ mất dữ liệu short-term
        self.short_term_dict: Dict[str, ShortTermMemory] = {}

    def _get_short_term(self, user_id: str) -> ShortTermMemory:
        if user_id not in self.short_term_dict:
            self.short_term_dict[user_id] = ShortTermMemory(max_history=20)
        return self.short_term_dict[user_id]

    # ====================== ASYNC METHODS ======================

    async def load_long_term(self, user_id: str, db: AsyncSession) -> UserProfile:
        """Load Long-term memory (UserProfile)"""
        return await self.long_term.load(user_id, db)

    async def load(
        self, user_id: str, db: AsyncSession
    ) -> Tuple[ShortTermMemory, UserProfile]:
        """Load cả Short-term và Long-term"""
        short_mem = self._get_short_term(user_id)
        long_mem = await self.load_long_term(user_id, db)
        return short_mem, long_mem

    async def update(
        self,
        user_id: str,
        user_input: str,
        assistant_response: str,
        intent: str = "general",
        analysis: Optional[Dict[str, Any]] = None,
        db: Optional[AsyncSession] = None
    ):
        """Cập nhật memory sau mỗi tương tác"""
        try:
            short_mem = self._get_short_term(user_id)
            short_mem.add_interaction(user_input, assistant_response, intent)

            if db is not None and analysis and len(analysis) > 0:
                await self.long_term.update_from_analysis(user_id, analysis, db)

        except Exception as e:
            logger.error(f"Memory update error for user {user_id}: {e}")

    def build_context(
        self,
        short_mem: ShortTermMemory,
        long_mem: UserProfile
    ) -> str:
        """
        Xây dựng context đẹp, dễ đọc cho LLM.
        """
        # Format đẹp hơn
        weak_skills_str = (
            ", ".join(list(long_mem.weak_skills.keys())[:7])
            if long_mem.weak_skills else "None"
        )

        goals_str = (
            ", ".join(long_mem.goals[:4])
            if long_mem.goals else "None"
        )

        interests_str = (
            ", ".join(long_mem.interests[-6:])
            if long_mem.interests else "None"
        )

        context = f"""User Profile:
- Target Language: {long_mem.target_language}
- Current Level: {long_mem.current_level}
- Learning Style: {long_mem.learning_style}
- Interests: {interests_str}
- Weak Skills: {weak_skills_str}
- Goals: {goals_str}

Recent Conversation:
{short_mem.get_context_for_prompt()}
"""
        return context

    def clear_short_term_session(self, user_id: str):
        """Xóa session hiện tại"""
        if user_id in self.short_term_dict:
            self.short_term_dict[user_id].clear_session()