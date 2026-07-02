# app/services/error_analytics_service.py
"""
Error Analytics Service - Phân tích error logs cho dashboard
"""
from typing import Dict, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timedelta, timezone
from loguru import logger

from app.models.error_log import UserErrorLog


class ErrorAnalyticsService:
    """Service để phân tích error logs cho dashboard analytics"""
    
    @staticmethod
    async def get_error_stats(
        db: AsyncSession,
        user_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Lấy thống kê lỗi tổng quan
        
        Returns:
        {
            "total_errors": 87,
            "by_type": {"GRAMMAR_ERROR": 60, "VOCABULARY_ERROR": 27},
            "by_severity": {"HIGH": 30, "MEDIUM": 50, "LOW": 7},
            "period_days": 30
        }
        """
        try:
            since_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            # Total errors
            total_stmt = select(func.count(UserErrorLog.id)).where(
                UserErrorLog.user_id == user_id,
                UserErrorLog.created_at >= since_date
            )
            total_result = await db.execute(total_stmt)
            total = total_result.scalar() or 0
            
            # By error_type (Cấp độ 1)
            type_stmt = select(
                UserErrorLog.error_type,
                func.count(UserErrorLog.id).label("count")
            ).where(
                UserErrorLog.user_id == user_id,
                UserErrorLog.created_at >= since_date
            ).group_by(UserErrorLog.error_type)
            
            type_result = await db.execute(type_stmt)
            by_type = {row.error_type: row.count for row in type_result.all()}
            
            # By severity
            severity_stmt = select(
                UserErrorLog.severity,
                func.count(UserErrorLog.id).label("count")
            ).where(
                UserErrorLog.user_id == user_id,
                UserErrorLog.created_at >= since_date
            ).group_by(UserErrorLog.severity)
            
            severity_result = await db.execute(severity_stmt)
            by_severity = {row.severity: row.count for row in severity_result.all()}
            
            return {
                "total_errors": total,
                "by_type": by_type,
                "by_severity": by_severity,
                "period_days": days
            }
            
        except Exception as e:
            logger.error(f"Failed to get error stats: {e}")
            return {
                "total_errors": 0,
                "by_type": {},
                "by_severity": {},
                "period_days": days
            }
    
    @staticmethod
    async def get_top_skill_tags(
        db: AsyncSession,
        user_id: str,
        limit: int = 10,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Lấy top skill_tags bị lỗi nhiều nhất (Cấp độ 2 - CHI TIẾT!)
        
        Returns:
        [
            {
                "skill_tag": "present_simple",
                "count": 15,
                "error_type": "GRAMMAR_ERROR"
            },
            {
                "skill_tag": "articles",
                "count": 10,
                "error_type": "GRAMMAR_ERROR"
            }
        ]
        """
        try:
            since_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            stmt = select(
                UserErrorLog.skill_tag,
                UserErrorLog.error_type,
                func.count(UserErrorLog.id).label("count")
            ).where(
                UserErrorLog.user_id == user_id,
                UserErrorLog.created_at >= since_date
            ).group_by(
                UserErrorLog.skill_tag,
                UserErrorLog.error_type
            ).order_by(
                desc("count")
            ).limit(limit)
            
            result = await db.execute(stmt)
            rows = result.all()
            
            return [
                {
                    "skill_tag": row.skill_tag,
                    "count": row.count,
                    "error_type": row.error_type
                }
                for row in rows
            ]
            
        except Exception as e:
            logger.error(f"Failed to get top skill tags: {e}")
            return []
    
    @staticmethod
    async def get_skill_tag_breakdown(
        db: AsyncSession,
        user_id: str,
        days: int = 30
    ) -> Dict[str, Dict[str, Any]]:
        """
        Phân tích chi tiết từng skill_tag
        
        Returns:
        {
            "present_simple": {
                "total_errors": 15,
                "error_type": "GRAMMAR_ERROR",
                "severity_avg": 2.5,
                "recent_count": 5
            },
            "articles": {
                "total_errors": 10,
                "error_type": "GRAMMAR_ERROR",
                "severity_avg": 2.2,
                "recent_count": 3
            }
        }
        """
        try:
            since_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            # Get all skill tags with counts and avg severity  
            from sqlalchemy import case
            
            severity_case = case(
                (UserErrorLog.severity == "CRITICAL", 4),
                (UserErrorLog.severity == "HIGH", 3),
                (UserErrorLog.severity == "MEDIUM", 2),
                else_=1
            )
            
            stmt = select(
                UserErrorLog.skill_tag,
                UserErrorLog.error_type,
                func.count(UserErrorLog.id).label("count"),
                func.avg(severity_case).label("avg_severity")
            ).where(
                UserErrorLog.user_id == user_id,
                UserErrorLog.created_at >= since_date
            ).group_by(
                UserErrorLog.skill_tag,
                UserErrorLog.error_type
            )
            
            result = await db.execute(stmt)
            rows = result.all()
            
            # Organize by skill_tag
            breakdown = {}
            for row in rows:
                skill = row.skill_tag
                breakdown[skill] = {
                    "total_errors": row.count,
                    "error_type": row.error_type,
                    "severity_avg": float(row.avg_severity) if row.avg_severity else 2.0,
                    "recent_count": row.count
                }
            
            return breakdown
            
        except Exception as e:
            logger.error(f"Failed to get skill tag breakdown: {e}")
            return {}
    
    @staticmethod
    async def get_recent_errors(
        db: AsyncSession,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Lấy danh sách lỗi gần đây
        
        Returns:
        [
            {
                "id": "uuid",
                "error_type": "GRAMMAR_ERROR",
                "skill_tag": "present_simple",
                "user_input": "He go to school",
                "correct_form": "He goes to school",
                "severity": "HIGH",
                "created_at": "2026-06-04T07:12:00"
            }
        ]
        """
        try:
            stmt = select(UserErrorLog).where(
                UserErrorLog.user_id == user_id
            ).order_by(desc(UserErrorLog.created_at)).limit(limit)
            
            result = await db.execute(stmt)
            errors = result.scalars().all()
            
            return [
                {
                    "id": str(error.id),
                    "error_type": error.error_type,
                    "skill_tag": error.skill_tag,
                    "user_input": error.user_input,
                    "correct_form": error.correct_form,
                    "severity": error.severity,
                    "created_at": error.created_at.isoformat()
                }
                for error in errors
            ]
            
        except Exception as e:
            logger.error(f"Failed to get recent errors: {e}")
            return []
