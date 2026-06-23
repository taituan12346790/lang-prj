# app/services/writing_service.py
"""Service for handling user writing submissions and AI feedback"""
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from loguru import logger

from app.models.user_writing import UserWriting


class WritingService:
    """Service for user writing submissions"""
    
    async def submit_writing(
        self,
        user_id: UUID,
        lesson_id: UUID,
        topic_id: UUID,
        prompt: str,
        user_text: str,
        word_count: int,
        db: AsyncSession
    ) -> UserWriting:
        """Submit a writing and get attempt number"""
        
        # Get current attempt number for this lesson
        result = await db.execute(
            select(func.max(UserWriting.attempt_number))
            .where(
                UserWriting.user_id == user_id,
                UserWriting.lesson_id == lesson_id
            )
        )
        max_attempt = result.scalar()
        attempt_number = (max_attempt or 0) + 1
        
        # Create writing submission
        writing = UserWriting(
            user_id=user_id,
            lesson_id=lesson_id,
            topic_id=topic_id,
            prompt=prompt,
            user_text=user_text,
            word_count=word_count,
            attempt_number=attempt_number,
            submitted_at=datetime.now(timezone.utc)
        )
        
        db.add(writing)
        await db.commit()
        await db.refresh(writing)
        
        logger.info(f"Writing submitted: user={user_id}, lesson={lesson_id}, attempt={attempt_number}")
        return writing
    
    async def save_feedback(
        self,
        writing_id: UUID,
        feedback: str,
        score_grammar: float,
        score_vocabulary: float,
        score_content: float,
        score_structure: float,
        detailed_feedback: Optional[Dict[str, Any]],
        db: AsyncSession
    ) -> UserWriting:
        """Save AI feedback for a writing submission"""
        
        result = await db.execute(
            select(UserWriting).where(UserWriting.id == writing_id)
        )
        writing = result.scalar_one_or_none()
        
        if not writing:
            raise ValueError(f"Writing {writing_id} not found")
        
        # Calculate total score
        score_total = score_grammar + score_vocabulary + score_content + score_structure
        
        # Update with feedback
        writing.feedback = feedback
        writing.score_grammar = score_grammar
        writing.score_vocabulary = score_vocabulary
        writing.score_content = score_content
        writing.score_structure = score_structure
        writing.score_total = score_total
        writing.detailed_feedback = detailed_feedback
        writing.reviewed_at = datetime.now(timezone.utc)
        
        await db.commit()
        await db.refresh(writing)
        
        logger.info(f"Feedback saved for writing {writing_id}: score={score_total}")
        return writing
    
    async def get_user_writings(
        self,
        user_id: UUID,
        db: AsyncSession,
        lesson_id: Optional[UUID] = None,
        topic_id: Optional[UUID] = None,
        limit: int = 10
    ) -> List[UserWriting]:
        """Get user's writing history"""
        
        query = select(UserWriting).where(UserWriting.user_id == user_id)
        
        if lesson_id:
            query = query.where(UserWriting.lesson_id == lesson_id)
        if topic_id:
            query = query.where(UserWriting.topic_id == topic_id)
        
        query = query.order_by(UserWriting.submitted_at.desc()).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_writing_stats(
        self,
        user_id: UUID,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get writing statistics for a user"""
        
        # Total writings
        total_result = await db.execute(
            select(func.count(UserWriting.id))
            .where(UserWriting.user_id == user_id)
        )
        total = total_result.scalar() or 0
        
        # Average score
        avg_result = await db.execute(
            select(func.avg(UserWriting.score_total))
            .where(
                UserWriting.user_id == user_id,
                UserWriting.score_total.isnot(None)
            )
        )
        avg_score = avg_result.scalar() or 0
        
        # Best score
        best_result = await db.execute(
            select(func.max(UserWriting.score_total))
            .where(UserWriting.user_id == user_id)
        )
        best_score = best_result.scalar() or 0
        
        return {
            "total_writings": total,
            "average_score": round(avg_score, 1),
            "best_score": round(best_score, 1)
        }
