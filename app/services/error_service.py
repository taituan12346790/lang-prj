# app/services/error_service.py
"""
Error Service - Manage user error history and provide suggestions
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timezone, timedelta
from loguru import logger

from app.models.error_log import UserErrorLog
from app.llm.llm_client import LLMClient


class ErrorService:
    """Service to manage user errors and provide personalized feedback"""
    
    @staticmethod
    async def log_error(
        user_id: str,
        error_data: Dict[str, Any],
        question: str,
        user_answer: str,
        correct_answer: str,
        db: AsyncSession,
        lesson_id: Optional[str] = None,
        topic_id: Optional[str] = None
    ) -> UserErrorLog:
        """Log error to database"""
        try:
            error_log = UserErrorLog(
                user_id=user_id,
                error_type=error_data.get("error_type", "GENERAL_ERROR"),
                skill_tag=error_data.get("skill_tag", "general"),
                severity=error_data.get("severity", "MEDIUM"),
                user_input=question,
                user_answer=user_answer,
                correct_form=correct_answer,
                question=question,
                lesson_id=lesson_id,
                topic_id=topic_id,
                explanation=error_data.get("explanation", ""),
                suggestion=error_data.get("suggestion", ""),
                extra_data=error_data
            )
            
            db.add(error_log)
            await db.commit()
            await db.refresh(error_log)
            
            logger.info(f"Error logged for user {user_id}: {error_data.get('error_type')}")
            return error_log
            
        except Exception as e:
            logger.error(f"Failed to log error for user {user_id}: {e}")
            await db.rollback()
            raise
    
    @staticmethod
    async def get_error_frequency(
        user_id: str,
        error_type: str,
        db: AsyncSession,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get frequency of a specific error type for user"""
        try:
            since_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            stmt = select(func.count(UserErrorLog.id)).where(
                UserErrorLog.user_id == user_id,
                UserErrorLog.error_type == error_type,
                UserErrorLog.created_at >= since_date
            )
            
            result = await db.execute(stmt)
            count = result.scalar() or 0
            
            return {
                "error_type": error_type,
                "frequency": count,
                "period_days": days
            }
            
        except Exception as e:
            logger.error(f"Failed to get error frequency: {e}")
            return {"error_type": error_type, "frequency": 0, "period_days": days}
    
    @staticmethod
    async def get_error_pattern(
        user_id: str,
        db: AsyncSession,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get user's error pattern (most frequent errors)"""
        try:
            stmt = select(
                UserErrorLog.error_type,
                UserErrorLog.skill_tag,
                func.count(UserErrorLog.id).label("count")
            ).where(
                UserErrorLog.user_id == user_id
            ).group_by(
                UserErrorLog.error_type,
                UserErrorLog.skill_tag
            ).order_by(
                desc("count")
            ).limit(limit)
            
            result = await db.execute(stmt)
            patterns = result.all()
            
            return [
                {
                    "error_type": row.error_type,
                    "skill_tag": row.skill_tag,
                    "frequency": row.count
                }
                for row in patterns
            ]
            
        except Exception as e:
            logger.error(f"Failed to get error pattern: {e}")
            return []
    
    @staticmethod
    async def generate_suggestion(
        user_id: str,
        error_data: Dict[str, Any],
        frequency: int,
        db: AsyncSession
    ) -> str:
        """Generate personalized suggestion based on error frequency"""
        error_type = error_data.get("error_type", "GENERAL_ERROR")
        skill_tag = error_data.get("skill_tag", "general")
        
        # Get recent similar errors
        stmt = select(UserErrorLog).where(
            UserErrorLog.user_id == user_id,
            UserErrorLog.error_type == error_type
        ).order_by(desc(UserErrorLog.created_at)).limit(5)
        
        result = await db.execute(stmt)
        recent_errors = result.scalars().all()
        
        # Build context
        context = f"""
User error pattern:
- Error type: {error_type}
- Skill: {skill_tag}
- Frequency: {frequency} times (recent period)
- Recent occurrences: {len(recent_errors)}
"""
        
        # Generate suggestion based on frequency
        from app.llm.llm_client import get_llm_client
        llm = get_llm_client()  # Use singleton
        
        if frequency == 1:
            # First time error
            prompt = f"""{context}

Học viên mới lần đầu mắc lỗi này. Hãy:
1. Giải thích ngắn gọn (2-3 câu) tại sao sai
2. Đưa ra 1 ví dụ minh họa
3. Khuyến khích học viên

Trả lời ngắn gọn, tích cực, dưới 150 từ."""
        
        elif frequency <= 3:
            # 2-3 times
            prompt = f"""{context}

Học viên đã sai lỗi này {frequency} lần. Hãy:
1. Nhắc lại rule ngữ pháp liên quan
2. Đưa ra 2 ví dụ để so sánh
3. Gợi ý làm 2-3 bài tập cùng loại

Trả lời dưới 200 từ."""
        
        else:
            # 4+ times - need intensive practice
            prompt = f"""{context}

Học viên đã sai lỗi này {frequency} lần (persistent error). Hãy:
1. Chỉ ra nguyên nhân sâu xa (concept misunderstanding?)
2. Đề xuất quay lại học bài cơ bản về skill này
3. Gợi ý làm quiz 5-10 câu để củng cố

Trả lời nghiêm túc nhưng động viên, dưới 250 từ."""
        
        try:
            suggestion = await llm.generate_async(
                system_prompt="Bạn là Language Learning Coach chuyên nghiệp, tận tâm và động viên.",
                user_prompt=prompt,
                temperature=0.7
            )
            return suggestion.strip()
        
        except Exception as e:
            logger.error(f"Failed to generate suggestion: {e}")
            return ErrorService._fallback_suggestion(frequency)
    
    @staticmethod
    def _fallback_suggestion(frequency: int) -> str:
        """Fallback suggestion when LLM fails"""
        if frequency == 1:
            return "Lần đầu mắc lỗi này thôi, đừng lo! Hãy xem lại giải thích và thử lại nhé 😊"
        elif frequency <= 3:
            return f"Bạn đã sai lỗi này {frequency} lần rồi. Mình gợi ý ôn lại lý thuyết và làm thêm vài bài tập nhé!"
        else:
            return f"Lỗi này xuất hiện nhiều ({frequency} lần). Hãy quay lại học bài cơ bản và làm quiz để củng cố kiến thức nhé!"
