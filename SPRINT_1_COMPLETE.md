# Sprint 1 - Learning Context Integration ✅ COMPLETE

## Overview
Context học (active topic, lesson, mode) hiện tại được lưu trên user_profiles, sẽ được truyền cho AI Tutor mỗi lần chat.

## Changes Made

### 1. Database Migration
**File:** `alembic/versions/004_add_learning_context.py`
- ✅ Added columns to `user_profiles` table:
  - `active_topic_id` (VARCHAR, nullable)
  - `active_lesson_order` (INTEGER, nullable)
  - `learning_mode` (VARCHAR, default='normal')
  - `last_chat_session_id` (VARCHAR, nullable)

**Migration Status:** ✅ Applied successfully

### 2. Model Update
**File:** `app/models/user_profile.py`
- ✅ Added fields to `UserProfile` class:
  ```python
  active_topic_id = Column(String(50), nullable=True)
  active_lesson_order = Column(Integer, nullable=True)
  learning_mode = Column(String(50), default="normal", nullable=False)
  last_chat_session_id = Column(String(255), nullable=True)
  ```
- Learning mode values: `normal`, `quiz_review`, `free_chat`

### 3. Schemas
**File:** `app/schemas/learning.py`
- ✅ Added request schema: `ActivateLearningContextRequest`
  ```python
  topic_id: str
  lesson_order: Optional[int]
  learning_mode: str
  ```
- ✅ Added response schema: `LearningContextResponse`
  ```python
  active_topic_id, active_lesson_order, learning_mode
  topic_name, lesson_title, lesson_type
  grammar_focus, estimated_minutes, current_level
  ```

### 4. Service Layer
**File:** `app/services/topic_service.py`
- ✅ Added method: `set_active_context(user_id, topic_id, lesson_order, learning_mode, db)`
  - Updates user profile with active context
  - Auto-marks topic as in_progress if not already
  
- ✅ Added method: `get_learning_context(user_id, db)`
  - Returns current context with full topic/lesson details
  - Resolves topic name, grammar focus, estimated time, etc.

### 5. API Endpoints
**File:** `app/routers/learning_path.py`
- ✅ POST `/api/learning/activate-context`
  - Request: `ActivateLearningContextRequest`
  - Sets active learning context
  
- ✅ GET `/api/learning/context`
  - Response: `LearningContextResponse`
  - Returns current learning context with details

## Usage Flow

### Backend Side
```
1. User chooses topic from Dashboard
   └─ POST /api/learning/activate-context
      └─ topic_id: "uuid-here"
      └─ lesson_order: 1 (optional)
      └─ learning_mode: "normal"

2. User opens AI Tutor
   └─ GET /api/learning/context
   └─ Returns: { topic_name: "...", lesson_title: "...", ... }

3. User sends chat message
   └─ Backend retrieves active context from profile
   └─ Passes to AI prompt
```

### Streamlit Frontend (Next Steps)
```python
# After login
context = requests.get("/api/learning/context").json()
st.write(f"Learning: {context['topic_name']} - {context['lesson_title']}")

# When user selects topic
requests.post("/api/learning/activate-context", json={
    "topic_id": topic_id,
    "lesson_order": 1,
    "learning_mode": "normal"
})

# Chat automatically uses this context
```

## AI Tutor Integration (Sprint 2)
- Chat API will receive `active_topic_id` from user profile
- Pass full context to AI prompt: topic name, grammar focus, current lesson
- AI can respond more contextually: "Let's practice the grammar from this lesson"

## Files Modified
- ✅ `alembic/versions/004_add_learning_context.py` (NEW)
- ✅ `app/models/user_profile.py`
- ✅ `app/schemas/learning.py`
- ✅ `app/services/topic_service.py`
- ✅ `app/routers/learning_path.py`

## Testing Checklist
- [ ] Database migration applied without errors
- [ ] Can activate context via POST /api/learning/activate-context
- [ ] Can retrieve context via GET /api/learning/context
- [ ] Context persists after restart
- [ ] Topic marked as in_progress when context activated

## Next Steps
- **Sprint 2:** Integrate context into AI chat pipeline
- **Sprint 3:** Save chat conversations to PG with topic_id
- **Sprint 4:** Quiz results update weak_skills that AI can see
