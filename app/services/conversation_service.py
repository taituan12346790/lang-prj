# app/services/conversation_service.py
"""
Service to manage conversation persistence
- Save messages to PostgreSQL
- Load conversation history
- Group sessions by topic
- Clean up old sessions
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, and_
from loguru import logger

from app.models.conversation import Conversation
from app.models.user import User


class ConversationService:
    """Manage chat message persistence and retrieval"""

    # ── Save Message ──────────────────────────────────────────

    @staticmethod
    async def save_message(
        db: AsyncSession,
        user_id: UUID,
        session_id: str,
        role: str,
        message: str,
        model_used: str = "gpt-4",
        tokens: int = 0,
        topic_id: Optional[str] = None,
        learning_mode: str = "normal",
    ) -> Conversation:
        """Save a single message to database"""
        conv = Conversation(
            user_id=user_id,
            session_id=session_id,
            role=role,
            message=message,
            model_used=model_used,
            tokens=tokens,
            topic_id=topic_id,
            learning_mode=learning_mode,
        )
        db.add(conv)
        await db.commit()
        logger.debug(f"✅ Message saved: session={session_id[:8]}..., role={role}")
        return conv

    # ── Load Messages ──────────────────────────────────────────

    @staticmethod
    async def get_messages_by_session(
        db: AsyncSession,
        user_id: UUID,
        session_id: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get all messages from a session"""
        result = await db.execute(
            select(Conversation)
            .where(
                and_(
                    Conversation.user_id == user_id,
                    Conversation.session_id == session_id,
                )
            )
            .order_by(Conversation.created_at)
            .limit(limit)
        )
        messages = result.scalars().all()
        return [
            {
                "role": m.role,
                "content": m.message,
                "timestamp": m.created_at.isoformat() if m.created_at else None,
                "tokens": m.tokens,
                "model": m.model_used,
            }
            for m in messages
        ]

    # ── List Sessions ──────────────────────────────────────────

    @staticmethod
    async def get_sessions_by_user(
        db: AsyncSession,
        user_id: UUID,
        limit: int = 50,
        topic_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get list of sessions for a user with preview"""
        query = select(Conversation).where(Conversation.user_id == user_id)

        if topic_id:
            query = query.where(Conversation.topic_id == topic_id)

        result = await db.execute(query.order_by(desc(Conversation.created_at)))
        all_messages = result.scalars().all()

        # Group by session_id and create session objects
        sessions_map: Dict[str, Dict] = {}
        for msg in all_messages:
            sid = msg.session_id
            if sid not in sessions_map:
                sessions_map[sid] = {
                    "session_id": sid,
                    "topic_id": msg.topic_id,
                    "topic_name": "Tổng quát",  # Default, will be fetched later
                    "learning_mode": msg.learning_mode,
                    "created_at": msg.created_at.isoformat() if msg.created_at else None,
                    "updated_at": msg.updated_at.isoformat() if msg.updated_at else None,
                    "message_count": 0,
                    "preview": "",
                }
            # Count messages
            if "message_count" not in sessions_map[sid]:
                sessions_map[sid]["message_count"] = 0
            sessions_map[sid]["message_count"] += 1

            # Get first user message as preview
            if msg.role == "user" and not sessions_map[sid].get("preview"):
                sessions_map[sid]["preview"] = msg.message[:100]

        # Convert to list
        sessions_list = list(sessions_map.values())
        
        # Fetch topic names for each session
        from app.models.topic import Topic
        for session in sessions_list:
            if session.get("topic_id"):
                try:
                    topic_result = await db.execute(
                        select(Topic).where(Topic.id == session["topic_id"])
                    )
                    topic = topic_result.scalar_one_or_none()
                    if topic:
                        session["topic_name"] = topic.name_vi or topic.name
                except Exception as e:
                    logger.warning(f"Failed to fetch topic name: {e}")
        
        # Sort by created_at descending
        sessions_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return sessions_list[:limit]

    # ── Get Session Detail ──────────────────────────────────────

    @staticmethod
    async def get_session_detail(
        db: AsyncSession,
        user_id: UUID,
        session_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Get full session with all messages"""
        result = await db.execute(
            select(Conversation)
            .where(
                and_(
                    Conversation.user_id == user_id,
                    Conversation.session_id == session_id,
                )
            )
            .order_by(Conversation.created_at)
        )
        messages = result.scalars().all()

        if not messages:
            return None

        first_msg = messages[0]
        return {
            "session_id": session_id,
            "topic_id": first_msg.topic_id,
            "learning_mode": first_msg.learning_mode,
            "created_at": first_msg.created_at,
            "updated_at": messages[-1].updated_at,
            "message_count": len(messages),
            "messages": [
                {
                    "role": m.role,
                    "content": m.message,
                    "timestamp": m.created_at.isoformat() if m.created_at else None,
                    "tokens": m.tokens,
                    "model": m.model_used,
                }
                for m in messages
            ],
        }

    # ── Cleanup ────────────────────────────────────────────────

    @staticmethod
    async def cleanup_old_sessions(
        db: AsyncSession,
        days_old: int = 30,
    ) -> int:
        """Delete conversations older than N days"""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
        result = await db.execute(
            select(func.count(Conversation.id)).where(
                Conversation.created_at < cutoff_date
            )
        )
        count = result.scalar() or 0

        await db.execute(
            select(Conversation).where(Conversation.created_at < cutoff_date)
        )
        await db.commit()
        logger.info(f"🗑️ Cleaned up {count} old conversation messages")
        return count

    # ── Update Session ────────────────────────────────────────

    @staticmethod
    async def update_session_context(
        db: AsyncSession,
        user_id: UUID,
        session_id: str,
        topic_id: Optional[str] = None,
        learning_mode: Optional[str] = None,
    ) -> None:
        """Update topic/mode for a session"""
        result = await db.execute(
            select(Conversation)
            .where(
                and_(
                    Conversation.user_id == user_id,
                    Conversation.session_id == session_id,
                )
            )
            .limit(1)
        )
        conv = result.scalar_one_or_none()

        if conv:
            if topic_id is not None:
                conv.topic_id = topic_id
            if learning_mode is not None:
                conv.learning_mode = learning_mode
            await db.commit()
