# app/services/ai_exercise_service.py
"""Service for AI-generated exercises"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from loguru import logger

from app.models.ai_exercise import AIExercise, AIExerciseSubmission, ExerciseStatus


class AIExerciseService:
    
    async def create_exercise(
        self,
        user_id: UUID,
        session_id: Optional[UUID],
        error_type: str,
        skill_tag: str,
        frequency: int,
        exercises: List[Dict[str, Any]],
        original_question: Optional[str] = None,
        user_wrong_answer: Optional[str] = None,
        correct_answer: Optional[str] = None,
        db: AsyncSession = None
    ) -> AIExercise:
        """Create a new exercise set"""
        
        exercise = AIExercise(
            user_id=user_id,
            session_id=session_id,
            error_type=error_type,
            skill_tag=skill_tag,
            frequency=frequency,
            original_question=original_question,
            user_wrong_answer=user_wrong_answer,
            correct_answer=correct_answer,
            exercises=exercises,
            status=ExerciseStatus.PENDING,
            created_at=datetime.now(timezone.utc)
        )
        
        db.add(exercise)
        await db.commit()
        await db.refresh(exercise)
        
        logger.info(f"Created exercise set {exercise.id} for user {user_id}")
        return exercise
    
    async def submit_exercise(
        self,
        exercise_id: UUID,
        user_answers: List[Dict[str, Any]],
        score: int,
        total: int,
        feedback: Optional[str],
        db: AsyncSession
    ) -> AIExerciseSubmission:
        """Submit user's answers for an exercise"""
        
        # Create submission
        submission = AIExerciseSubmission(
            exercise_id=exercise_id,
            user_answers=user_answers,
            score=score,
            total=total,
            feedback=feedback,
            submitted_at=datetime.now(timezone.utc)
        )
        
        db.add(submission)
        
        # Update exercise status
        result = await db.execute(
            select(AIExercise).where(AIExercise.id == exercise_id)
        )
        exercise = result.scalar_one_or_none()
        
        if exercise:
            exercise.status = ExerciseStatus.COMPLETED
            exercise.completed_at = datetime.now(timezone.utc)
        
        await db.commit()
        await db.refresh(submission)
        
        logger.info(f"Submission created for exercise {exercise_id}: score={score}/{total}")
        return submission
    
    async def get_pending_exercise(
        self,
        user_id: UUID,
        session_id: Optional[UUID],
        db: AsyncSession
    ) -> Optional[AIExercise]:
        """Get the most recent pending exercise for this user/session"""
        
        query = select(AIExercise).where(
            and_(
                AIExercise.user_id == user_id,
                AIExercise.status == ExerciseStatus.PENDING
            )
        )
        
        if session_id:
            query = query.where(AIExercise.session_id == session_id)
        
        query = query.order_by(AIExercise.created_at.desc()).limit(1)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_exercise_history(
        self,
        user_id: UUID,
        limit: int = 10,
        db: AsyncSession = None
    ) -> List[AIExercise]:
        """Get user's exercise history"""
        
        result = await db.execute(
            select(AIExercise)
            .where(AIExercise.user_id == user_id)
            .order_by(AIExercise.created_at.desc())
            .limit(limit)
        )
        
        return list(result.scalars().all())
    
    async def get_exercise_stats(
        self,
        user_id: UUID,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get statistics for user's exercises"""
        
        # Get all completed exercises
        result = await db.execute(
            select(AIExercise)
            .where(
                and_(
                    AIExercise.user_id == user_id,
                    AIExercise.status == ExerciseStatus.COMPLETED
                )
            )
        )
        exercises = list(result.scalars().all())
        
        if not exercises:
            return {
                "total_exercises": 0,
                "total_questions": 0,
                "average_score": 0
            }
        
        # Calculate stats
        total_score = 0
        total_questions = 0
        
        for ex in exercises:
            # Get latest submission
            sub_result = await db.execute(
                select(AIExerciseSubmission)
                .where(AIExerciseSubmission.exercise_id == ex.id)
                .order_by(AIExerciseSubmission.submitted_at.desc())
                .limit(1)
            )
            submission = sub_result.scalar_one_or_none()
            
            if submission:
                total_score += submission.score
                total_questions += submission.total
        
        avg_score = (total_score / total_questions * 100) if total_questions > 0 else 0
        
        return {
            "total_exercises": len(exercises),
            "total_questions": total_questions,
            "average_score": round(avg_score, 1)
        }
