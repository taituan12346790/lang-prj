# Sprints 2-5 Complete Implementation Plan

**Status:** This document provides the complete remaining work. Due to scope, I've prioritized the core changes needed.

---

## SPRINT 2: Chat History PostgreSQL ✅

### Completed:
- ✅ Migration 005 created: `005_add_conversation_context.py`
- ✅ Conversation model updated with `topic_id` and `learning_mode`
- ✅ ConversationService created with methods:
  - `save_message()` - Save single message
  - `get_messages_by_session()` - Get chat history
  - `get_sessions_by_user()` - List sessions
  - `get_session_detail()` - Full session info
  - `cleanup_old_sessions()` - Clean old messages
- ✅ Chat router updated to use ConversationService
- ✅ Migration applied successfully

### What This Does:
- Saves every chat message to PostgreSQL
- Groups messages by session_id
- Each message tracks: role, content, model_used, tokens, topic_id, learning_mode
- Can retrieve full chat history at any time

---

## SPRINT 3: Quiz ↔ Chat Integration

### File: `app/services/quiz_service_enhanced.py` (NEW)

```python
async def submit_quiz_and_get_weak_skills(
    topic_id: UUID,
    user_id: UUID,
    request: QuizSubmitRequest,
    db: AsyncSession,
) -> Dict[str, Any]:
    """Submit quiz and return weak skills for AI review"""
    # 1. Grade quiz (existing logic)
    response = await TopicService.submit_quiz(topic_id, user_id, request, db)
    
    # 2. Extract wrong answers
    weak_skills = []
    for result in response.results:
        if not result.is_correct:
            weak_skills.append({
                "question": result.question,
                "user_answer": result.your_answer,
                "correct": result.correct_answer,
                "explanation": result.explanation,
            })
    
    # 3. Update user_topic_progress.weak_skills
    prog_result = await db.execute(
        select(UserTopicProgress).where(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.topic_id == topic_id,
        )
    )
    prog = prog_result.scalar_one_or_none()
    if prog:
        prog.weak_skills = weak_skills
        await db.commit()
    
    return {
        "quiz_response": response,
        "weak_skills": weak_skills,
        "recommendation": "Review with AI Tutor" if weak_skills else "Excellent!"
    }
```

### Chat Request Update: `app/schemas/chat.py`

```python
class ChatRequest(BaseModel):
    user_input: str
    target_lang: Optional[str] = None
    explain_in: Optional[str] = "vi"
    difficulty: Optional[str] = None
    temperature: Optional[float] = 0.7
    
    # Sprint 3: Quiz context
    quiz_wrong_answers: Optional[List[Dict]] = None  # From quiz results
    quiz_topic_id: Optional[str] = None  # Which topic quiz was about
```

### Quiz Router Update: `app/routers/quiz.py`

```python
@router.post("/topic/{topic_id}/submit", response_model=QuizSubmitResponse)
async def submit_quiz_enhanced(
    topic_id: UUID,
    request: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit quiz and link to AI Tutor if needed"""
    from app.services.quiz_service_enhanced import submit_quiz_and_get_weak_skills
    
    result = await submit_quiz_and_get_weak_skills(
        topic_id=topic_id,
        user_id=current_user.id,
        request=request,
        db=db,
    )
    
    # If user failed and has weak skills, add button for AI review
    if result["weak_skills"]:
        # Store in session for chat to pick up
        result["ai_review_enabled"] = True
        result["ai_review_url"] = f"/api/chat/quiz-review?topic_id={topic_id}"
    
    return result
```

---

## SPRINT 4: Level-Up / Placement Unified

### File: `app/services/level_service_unified.py` (NEW)

```python
class LevelService:
    """Unified eligibility and level management"""
    
    @staticmethod
    async def get_eligibility(
        user_id: UUID,
        db: AsyncSession,
    ) -> Dict[str, Any]:
        """Check level-up eligibility - unified logic"""
        dashboard = await TopicService().get_dashboard(user_id, db)
        lp = dashboard.level_progress
        
        return {
            "can_level_up": lp.can_level_up,
            "current_level": dashboard.current_level,
            "next_level": get_next_level(dashboard.current_level),
            "completion_pct": lp.completion_percentage,
            "requirements": {
                "min_topics_pct": 75,
                "min_quiz_score": 70,
                "topics_completed": lp.completed_topics,
                "topics_needed": int(lp.total_topics * 0.75),
            },
            "message": lp.level_up_message,
            "test_url": "/api/test/level-up" if lp.can_level_up else None,
        }
    
    @staticmethod
    async def complete_level_up_test(
        user_id: UUID,
        current_level: str,
        test_answers: Dict[str, str],
        db: AsyncSession,
    ) -> bool:
        """Complete level-up test and promote user"""
        # 1. Grade test
        score = grade_test(test_answers)  # Your logic
        
        # 2. If passed, promote
        if score >= 70:
            prof_result = await db.execute(
                select(UserProfile).where(UserProfile.user_id == user_id)
            )
            prof = prof_result.scalar_one_or_none()
            if prof:
                next_level = get_next_level(current_level)
                prof.current_level = next_level
                
                # Clear active context when leveling up
                prof.active_topic_id = None
                prof.active_lesson_order = None
                
                await db.commit()
                return True
        
        return False
```

### Update Placement Test: `app/routers/test.py`

```python
# Use unified LevelService for all eligibility checks
# Replace duplicate logic with single source of truth
```

---

## SPRINT 5: AI Auto-Updates Profile (Reflector Node)

### File: `app/core/reflector_enhanced.py` (NEW)

```python
async def reflect_and_update(
    state: dict,
    user_id: UUID,
    db: AsyncSession,
) -> dict:
    """
    After AI responds, analyze what user learned
    Update user_topic_progress with new weak/strong skills
    """
    from app.services.topic_service import TopicService
    
    # Extract insights from conversation
    insights = await analyze_conversation_insights(
        messages=state.get("messages", []),
        topic_id=state.get("active_topic_id"),
    )
    
    # Update user profile if active topic
    if state.get("active_topic_id"):
        from uuid import UUID as UUID_type
        try:
            topic_uuid = UUID_type(state["active_topic_id"])
            
            prog_result = await db.execute(
                select(UserTopicProgress).where(
                    UserTopicProgress.user_id == user_id,
                    UserTopicProgress.topic_id == topic_uuid,
                )
            )
            prog = prog_result.scalar_one_or_none()
            if prog:
                # Merge new weak/strong skills
                if insights.get("weak_skills"):
                    existing = prog.weak_skills or {}
                    existing.update(insights["weak_skills"])
                    prog.weak_skills = existing
                
                if insights.get("strong_skills"):
                    existing = prog.strong_skills or {}
                    existing.update(insights["strong_skills"])
                    prog.strong_skills = existing
                
                await db.commit()
        except Exception as e:
            logger.warning(f"Could not update progress: {e}")
    
    return state
```

### Update Learning Service: `app/services/learning_service.py`

```python
# At end of process():
# Call reflector to update profile based on conversation
result = await reflect_and_update(state, user_id, db)
```

---

## Complete Integration Flow

### User Journey After All Sprints:

```
1. LOGIN
   └─ GET /api/learning/context
   └─ Load previous learning context

2. SELECT TOPIC (Dashboard)
   └─ POST /api/learning/activate-context
   └─ active_topic_id saved to profile

3. STUDY LESSON
   └─ Click "Học tiếp"
   └─ Navigate to Chat
   └─ Context shown in header

4. CHAT WITH AI
   └─ POST /api/chat/
   └─ Backend loads context from profile
   └─ AI Tutor responds about THIS topic
   └─ Message saved to PostgreSQL with topic_id

5. TAKE QUIZ
   └─ POST /api/quiz/topic/{id}/submit
   └─ If failed: Weak skills saved
   └─ Show "Ôn bài với AI" button

6. REVIEW WITH AI
   └─ POST /api/chat/ with quiz_context
   └─ AI focuses on weak areas
   └─ Reflector updates user_topic_progress.weak_skills

7. COMPLETE TOPICS
   └─ GET /api/learning/eligibility
   └─ If 75% + avg 70: Can level-up
   └─ POST /api/test/level-up
   └─ If passed: Promoted, context cleared
```

---

## What Each Sprint Adds

| Sprint | Adds | Impact |
|--------|------|--------|
| 1 | Learning context on profile | AI knows topic/lesson |
| 2 | Chat history to PostgreSQL | Persistent conversation history |
| 3 | Quiz weak skills to chat | AI focuses on failed questions |
| 4 | Unified eligibility logic | Consistent level-up rules |
| 5 | Auto-update profile after chat | Learning reflected in profile |

---

## Implementation Priority

### Must Have (Sprints 1-2):
✅ Learning context  
✅ Chat history persistence

### Should Have (Sprint 3):
⚠️ Quiz integration  
⚠️ Weak skills tracking

### Nice to Have (Sprint 4-5):
🔹 Unified eligibility  
🔹 Auto profile updates

---

## Database State After All Sprints

```
user_profiles:
  - active_topic_id ✅
  - active_lesson_order ✅
  - learning_mode ✅
  - last_chat_session_id ✅

user_topic_progress:
  - weak_skills (updated by Quiz + Reflector) ✅
  - strong_skills (updated by Reflector) ✅

conversations:
  - topic_id ✅
  - learning_mode ✅
```

---

## API Endpoints After All Sprints

```
LEARNING:
  POST /api/learning/activate-context
  GET  /api/learning/context

CHAT:
  POST /api/chat/
  GET  /api/chat/history/{session_id}
  GET  /api/chat/sessions

QUIZ:
  POST /api/quiz/topic/{topic_id}/submit
  GET  /api/quiz/topic/{topic_id}/questions

TEST:
  POST /api/test/placement
  POST /api/test/level-up
  GET  /api/learning/eligibility
```

---

## Next: Manual Streamlit Updates Needed

After all backend sprints, Streamlit needs:

1. **Dashboard**: Add "Học tiếp" buttons that call `activate-context`
2. **Chat**: Display current topic in header
3. **Quiz**: Add "Ôn bài với AI" button if failed
4. **Sidebar**: Show learning context
5. **Session Load**: Reload previous context after login

---

## Status

✅ **Sprint 1:** COMPLETE - Learning context ✅ Deployed  
✅ **Sprint 2:** COMPLETE - Chat history ✅ Deployed  
⏳ **Sprint 3-5:** DESIGNED - Ready to implement

**Estimated Time to Complete:** 2-3 hours for remaining sprints

**Recommendation:** Focus on Sprint 3 next (Quiz integration) as it has highest user impact.
