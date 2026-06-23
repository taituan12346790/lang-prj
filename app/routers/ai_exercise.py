# app/routers/ai_exercise.py
"""API endpoints for AI exercises"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.ai_exercise_service import AIExerciseService
from pydantic import BaseModel

router = APIRouter(prefix="/api/ai-exercise", tags=["AI Exercise"])
_svc = AIExerciseService()


@router.get("/pending")
async def get_pending_exercise(
    session_id: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get pending exercise for user"""
    exercise = await _svc.get_pending_exercise(
        user_id=current_user.id,
        session_id=UUID(session_id) if session_id else None,
        db=db
    )
    
    if not exercise:
        return None
    
    return {
        "id": str(exercise.id),
        "error_type": exercise.error_type,
        "skill_tag": exercise.skill_tag,
        "exercises": exercise.exercises,
        "created_at": exercise.created_at.isoformat()
    }


class SubmitAnswersRequest(BaseModel):
    exercise_id: str
    answers: list  # [{"number": 1, "answer": "is watching"}, ...]


@router.post("/submit")
async def submit_answers(
    request: SubmitAnswersRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit answers for an exercise"""
    
    # Get exercise
    from sqlalchemy import select
    from app.models.ai_exercise import AIExercise
    
    result = await db.execute(
        select(AIExercise).where(AIExercise.id == UUID(request.exercise_id))
    )
    exercise = result.scalar_one_or_none()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    if exercise.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your exercise")
    
    # Grade answers (simple matching for now)
    exercises = exercise.exercises
    user_answers = request.answers
    
    graded = []
    score = 0
    
    for user_ans in user_answers:
        num = user_ans["number"]
        answer = user_ans["answer"].strip().lower()
        
        # Find matching exercise
        ex = next((e for e in exercises if e["number"] == num), None)
        if not ex:
            continue
        
        # Simple check: if correct_answer exists, use it; otherwise skip
        correct = ex.get("correct_answer", "").strip().lower()
        
        # For now, mark as correct if answer contains the verb in -ing form
        is_correct = False
        if correct:
            is_correct = answer == correct
        else:
            # Fallback: check if it's a reasonable present continuous form
            verb_hint = ex.get("verb_hint", "")
            is_correct = "ing" in answer or verb_hint in answer
        
        if is_correct:
            score += 1
        
        graded.append({
            "number": num,
            "answer": answer,
            "is_correct": is_correct
        })
    
    # Save submission
    submission = await _svc.submit_exercise(
        exercise_id=UUID(request.exercise_id),
        user_answers=graded,
        score=score,
        total=len(exercises),
        feedback=None,  # AI will provide feedback separately
        db=db
    )
    
    return {
        "submission_id": str(submission.id),
        "score": score,
        "total": len(exercises),
        "graded_answers": graded
    }
