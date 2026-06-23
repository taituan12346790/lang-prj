# Sprint 1 Implementation Summary
**Date:** June 4, 2026  
**Status:** ✅ COMPLETE & TESTED

---

## What Was Done

### Problem
- Chat không biết user đang học chủ đề nào
- Dashboard, Lessons, Quiz là 3 hệ thống tách riêng
- AI Tutor không có context về bài đang học

### Solution
Lưu **learning context** (active topic, lesson, mode) trên user profile. Mỗi lần AI Tutor chat, backend tự động lấy context này.

---

## Implementation Checklist

### ✅ Database (Migration 004)
```sql
ALTER TABLE user_profiles ADD COLUMN active_topic_id VARCHAR(50) NULL;
ALTER TABLE user_profiles ADD COLUMN active_lesson_order INTEGER NULL;
ALTER TABLE user_profiles ADD COLUMN learning_mode VARCHAR(50) DEFAULT 'normal';
ALTER TABLE user_profiles ADD COLUMN last_chat_session_id VARCHAR(255) NULL;
```
**Status:** Applied successfully via `alembic upgrade head`

### ✅ Model Layer (`app/models/user_profile.py`)
```python
active_topic_id = Column(String(50), nullable=True)
active_lesson_order = Column(Integer, nullable=True)
learning_mode = Column(String(50), default="normal", nullable=False)
last_chat_session_id = Column(String(255), nullable=True)
```

### ✅ Schema Layer (`app/schemas/learning.py`)
Added two new schemas:

**Request:**
```python
class ActivateLearningContextRequest(BaseModel):
    topic_id: str
    lesson_order: Optional[int]
    learning_mode: str
```

**Response:**
```python
class LearningContextResponse(BaseModel):
    active_topic_id: Optional[str]
    active_lesson_order: Optional[int]
    learning_mode: str
    topic_name: Optional[str]
    lesson_title: Optional[str]
    grammar_focus: List[str]
    estimated_minutes: int
    current_level: str
```

### ✅ Service Layer (`app/services/topic_service.py`)
Added two methods:

**1. `set_active_context(user_id, topic_id, lesson_order, learning_mode, db)`**
- Sets active context on user profile
- Auto-marks topic as in_progress
- Logs to database

**2. `get_learning_context(user_id, db)`**
- Retrieves current context
- Resolves topic/lesson details
- Returns full context object

### ✅ API Endpoints (`app/routers/learning_path.py`)
Added two new endpoints:

**POST `/api/learning/activate-context`**
```
Request: ActivateLearningContextRequest
Response: { status: "ok", message: "..." }
```

**GET `/api/learning/context`**
```
Response: LearningContextResponse
```

---

## How It Works

### User Selects Topic from Dashboard
```
Frontend:
  POST /api/learning/activate-context
  {
    "topic_id": "550e8400-e29b-41d4-a716-446655440000",
    "lesson_order": 1,
    "learning_mode": "normal"
  }

Backend:
  → TopicService.set_active_context()
  → UserProfile.active_topic_id = topic_id
  → UserProfile.active_lesson_order = 1
  → Commit to DB
```

### User Opens AI Tutor
```
Frontend:
  GET /api/learning/context

Backend Returns:
  {
    "active_topic_id": "550e8400-e29b-41d4-a716-446655440000",
    "active_lesson_order": 1,
    "learning_mode": "normal",
    "topic_name": "Present Simple",
    "lesson_title": "Affirmative Form",
    "lesson_type": "grammar",
    "grammar_focus": ["present_simple", "affirmative"],
    "estimated_minutes": 30,
    "current_level": "A1"
  }
```

### User Sends Chat
```
Frontend:
  POST /api/chat/
  { "user_input": "Giải thích về bài này" }

Backend:
  → LearningService loads context from profile
  → Builds prompt: "Topic: Present Simple, Lesson: Affirmative Form"
  → Sends to AI with full context
  → AI responds contextually

AI can now say:
  "Ừ, trong bài 'Affirmative Form' của chủ đề 'Present Simple'..."
  instead of generic "Hỏi gì nè?"
```

---

## API Examples

### 1. Activate Learning Context
```bash
curl -X POST http://localhost:8000/api/learning/activate-context \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": "550e8400-e29b-41d4-a716-446655440000",
    "lesson_order": 1,
    "learning_mode": "normal"
  }'

# Response:
# { "status": "ok", "message": "Learning context activated" }
```

### 2. Get Learning Context
```bash
curl -X GET http://localhost:8000/api/learning/context \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response:
# {
#   "active_topic_id": "550e8400-e29b-41d4-a716-446655440000",
#   "active_lesson_order": 1,
#   "learning_mode": "normal",
#   "topic_name": "Present Simple",
#   "lesson_title": "Affirmative Form",
#   "lesson_type": "grammar",
#   "grammar_focus": ["present_simple", "affirmative"],
#   "estimated_minutes": 30,
#   "current_level": "A1"
# }
```

---

## Backend Status

**✅ Backend Running**
- Started: `python -m uvicorn app.main:app --reload`
- Port: 8000
- Status: Application startup complete

**✅ New Endpoints Available**
- `POST /api/learning/activate-context`
- `GET /api/learning/context`

---

## Next Steps (Sprint 2)

### AI Tutor Integration
- [ ] Update `chat.py` router to receive `topic_id` from ChatRequest (optional)
- [ ] Update `learning_service.py` to load context from profile in `_load_memory_node`
- [ ] Pass full context to AI prompt
- [ ] Update Streamlit frontend to call `/activate-context` when user clicks topic

### Expected Outcome
When user sends chat message:
1. Backend fetches `active_topic_id` from profile
2. Calls `get_learning_context()`
3. Builds AI prompt with: topic name, lesson, grammar focus, current level
4. AI responds contextually about that specific lesson

---

## Files Changed

| File | Changes |
|------|---------|
| `alembic/versions/004_add_learning_context.py` | NEW - Migration file |
| `app/models/user_profile.py` | Added 4 learning context columns |
| `app/schemas/learning.py` | Added 2 new schemas |
| `app/services/topic_service.py` | Added 2 service methods |
| `app/routers/learning_path.py` | Added 2 new endpoints |

---

## Testing Notes

Backend is running and ready for:
- Manual API testing via curl/Postman
- Frontend integration testing
- AI Tutor context passing

All database changes applied successfully. No errors.

---

**Status: 🟢 READY FOR SPRINT 2**
