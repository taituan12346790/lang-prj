# app/routers/writing.py
"""API endpoints for writing submissions"""
import json
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.writing_service import WritingService
from app.schemas.writing import (
    SubmitWritingRequest,
    WritingFeedbackResponse,
    WritingHistoryItem,
    WritingStatsResponse
)
from app.llm.llm_client import LLMClient
from loguru import logger

router = APIRouter(prefix="/api/writing", tags=["Writing"])
_svc = WritingService()


@router.post("/submit", response_model=WritingFeedbackResponse)
async def submit_writing(
    request: SubmitWritingRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit writing for AI review
    Returns structured feedback with scoring rubric
    """
    try:
        # Fetch lesson and topic information for context-aware grading
        from app.models.lesson import Lesson
        from app.models.topic import Topic
        from sqlalchemy import select
        
        lesson_result = await db.execute(
            select(Lesson).where(Lesson.id == request.lesson_id)
        )
        lesson = lesson_result.scalar_one_or_none()
        
        topic = None
        if lesson:
            topic_result = await db.execute(
                select(Topic).where(Topic.id == lesson.topic_id)
            )
            topic = topic_result.scalar_one_or_none()
        
        # Save submission to database
        writing = await _svc.submit_writing(
            user_id=current_user.id,
            lesson_id=request.lesson_id,
            topic_id=request.topic_id,
            prompt=request.prompt,
            user_text=request.user_text,
            word_count=request.word_count,
            db=db
        )
        
        # Get AI feedback with structured scoring
        llm = LLMClient()
        
        # Build context-aware grading prompt
        topic_context = ""
        if topic and lesson:
            grammar_list = ", ".join(topic.grammar_focus) if topic.grammar_focus else "N/A"
            vocab_list = ", ".join(topic.vocabulary_tags) if topic.vocabulary_tags else "N/A"
            
            topic_context = f"""
**Learning Context:**
- Topic: {topic.name_vi} ({topic.name})
- Level: {topic.level}
- Grammar Focus: {grammar_list}
- Vocabulary Topics: {vocab_list}

**Grading Guidelines for {topic.level} Learners:**
- This is a {"BEGINNER" if topic.level == "A1" else "beginner-intermediate" if topic.level == "A2" else "intermediate" if topic.level in ["B1", "B2"] else "advanced"} level student
- Grade based ONLY on the vocabulary and grammar taught in THIS topic and previous topics
- Be LENIENT - if the student uses the target grammar/vocabulary correctly, give 80-90+ score
- Focus on: "Did they use what they learned?" NOT "Is this perfect English?"
- Minor mistakes are OK for beginners - encourage effort and progress
- For A1/A2: Simple sentences using basic grammar correctly = HIGH SCORE
- Don't expect complex structures, idioms, or advanced vocabulary

"""
        
        review_prompt = f"""You are a supportive English writing teacher. Review this student's writing with encouragement and constructive feedback.

{topic_context}

**Writing Prompt:** {request.prompt}

**Student's Writing:**
{request.user_text}

**Word Count:** {request.word_count} words

Please provide:
1. **Grammar Score (0-25):** Rate grammar accuracy (lenient for beginner level)
2. **Vocabulary Score (0-25):** Rate vocabulary range (based on what was taught in this topic)
3. **Content Score (0-25):** Rate how well they addressed the prompt
4. **Structure Score (0-25):** Rate organization (simple structure is OK for beginners)
5. **General Feedback:** 2-3 encouraging sentences in Vietnamese, highlighting what they did well
6. **Specific Corrections:** List 2-3 specific mistakes (if any) with corrections
7. **Suggestions:** 2-3 suggestions for improvement

**IMPORTANT:** 
- If the student used the target grammar/vocabulary from this topic correctly, score should be 80-90+
- Be encouraging - focus on what they did RIGHT first
- Mistakes are part of learning - be supportive, not harsh
- Vietnamese feedback should be friendly and motivating

Format your response as JSON:
{{
  "score_grammar": 20.0,
  "score_vocabulary": 18.0,
  "score_content": 22.0,
  "score_structure": 20.0,
  "feedback": "Bài viết của bạn rất tốt! Bạn đã sử dụng...",
  "corrections": ["Mistake 1 → Correction", "Mistake 2 → Correction"],
  "suggestions": ["Suggestion 1", "Suggestion 2"]
}}"""
        
        try:
            ai_response = await llm.generate_async(
                user_input=review_prompt,
                system_prompt="You are an expert English writing teacher providing detailed feedback."
            )
            
            # Parse JSON response
            feedback_data = json.loads(ai_response)
            
            # Save feedback to database
            await _svc.save_feedback(
                writing_id=writing.id,
                feedback=feedback_data.get("feedback", "No feedback provided"),
                score_grammar=feedback_data.get("score_grammar", 20.0),
                score_vocabulary=feedback_data.get("score_vocabulary", 20.0),
                score_content=feedback_data.get("score_content", 20.0),
                score_structure=feedback_data.get("score_structure", 20.0),
                detailed_feedback={
                    "corrections": feedback_data.get("corrections", []),
                    "suggestions": feedback_data.get("suggestions", [])
                },
                db=db
            )
            
            # Refresh to get updated data
            await db.refresh(writing)
            
            return WritingFeedbackResponse(
                writing_id=writing.id,
                attempt_number=writing.attempt_number,
                feedback=writing.feedback,
                score_grammar=writing.score_grammar,
                score_vocabulary=writing.score_vocabulary,
                score_content=writing.score_content,
                score_structure=writing.score_structure,
                score_total=writing.score_total,
                detailed_feedback=writing.detailed_feedback,
                submitted_at=writing.submitted_at,
                reviewed_at=writing.reviewed_at
            )
            
        except json.JSONDecodeError:
            # Fallback if AI doesn't return valid JSON
            logger.warning("AI didn't return valid JSON, using fallback scoring")
            
            # Simple fallback scoring
            score_base = 20.0
            await _svc.save_feedback(
                writing_id=writing.id,
                feedback=ai_response[:500],  # Use first 500 chars as feedback
                score_grammar=score_base,
                score_vocabulary=score_base,
                score_content=score_base,
                score_structure=score_base,
                detailed_feedback=None,
                db=db
            )
            
            await db.refresh(writing)
            
            return WritingFeedbackResponse(
                writing_id=writing.id,
                attempt_number=writing.attempt_number,
                feedback=writing.feedback,
                score_grammar=writing.score_grammar,
                score_vocabulary=writing.score_vocabulary,
                score_content=writing.score_content,
                score_structure=writing.score_structure,
                score_total=writing.score_total,
                detailed_feedback=writing.detailed_feedback,
                submitted_at=writing.submitted_at,
                reviewed_at=writing.reviewed_at
            )
        
    except Exception as e:
        logger.exception(f"Error submitting writing: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing writing: {str(e)}")


@router.get("/history", response_model=list[WritingHistoryItem])
async def get_writing_history(
    lesson_id: UUID = None,
    topic_id: UUID = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's writing history"""
    writings = await _svc.get_user_writings(
        user_id=current_user.id,
        db=db,
        lesson_id=lesson_id,
        topic_id=topic_id,
        limit=limit
    )
    return writings


@router.get("/stats", response_model=WritingStatsResponse)
async def get_writing_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's writing statistics"""
    stats = await _svc.get_writing_stats(current_user.id, db)
    return WritingStatsResponse(**stats)
