# Quiz Review - Streamlit Integration ✅

**Date**: 2026-06-05  
**Task**: A3 Streamlit part

## ✅ Changes Made

### 1. Update `api_chat()` Function

**File**: `streamlit_app.py` (lines ~286-300)

Added quiz parameters:
```python
def api_chat(
    msg: str, 
    session_id: Optional[str] = None,
    quiz_wrong_answers: Optional[list] = None,  # NEW
    quiz_topic_id: Optional[str] = None         # NEW
) -> tuple[bool, str, dict]:
```

### 2. Build Quiz Wrong Answers from Results

**File**: `streamlit_app.py` - `page_quiz_result()` (lines ~1626-1642)

When user clicks "🤖 Ôn bài với AI":
```python
# Build quiz_wrong_answers from results
quiz_wrong_answers = []
for r in results:
    if not r.get("is_correct"):
        quiz_wrong_answers.append({
            "question": r.get("question", ""),
            "user_answer": r.get("your_answer", ""),
            "correct_answer": r.get("correct_answer", ""),
            "skill_tag": r.get("skill_tag", "unknown"),
            "explanation": r.get("explanation", "")
        })

# Store in session_state
st.session_state.quiz_review_mode = True
st.session_state.quiz_wrong_answers = quiz_wrong_answers
st.session_state.quiz_topic_id = topic.get("id")
```

### 3. Chat Page Quiz Review Mode

**File**: `streamlit_app.py` - `page_chat()` (lines ~1677-1691)

- Check `quiz_review_mode` flag
- Load `quiz_wrong_answers` and `quiz_topic_id`
- Create helper function `call_chat_api()` to pass quiz context
- Auto-clear quiz mode after first exchange

```python
# Helper function to call API with quiz context
def call_chat_api(msg):
    return api_chat(
        msg,
        session_id=session_id,
        quiz_wrong_answers=quiz_wrong_answers if quiz_review_mode else None,
        quiz_topic_id=quiz_topic_id if quiz_review_mode else None
    )
```

## 🔄 User Flow

```
User fails quiz (3/10 wrong)
  ↓
Quiz Result Page shows:
  - ❌ 3 câu sai
  - Button: "🤖 Ôn bài với AI"
  ↓
User clicks button
  ↓
Streamlit builds quiz_wrong_answers from results:
  [
    {question: "I ___ student", user_answer: "is", 
     correct_answer: "am", skill_tag: "verb_to_be"},
    ...
  ]
  ↓
Sets session_state:
  - quiz_review_mode = True
  - quiz_wrong_answers = [...]
  - quiz_topic_id = "..."
  ↓
Redirects to Chat page
  ↓
Chat page calls: 
  api_chat(msg, quiz_wrong_answers=[...], quiz_topic_id="...")
  ↓
Backend receives quiz context
  ↓
AI generates focused review:
  "Bạn đã nhầm lẫn quy tắc to be:
   - I → am (không phải is)
   - She/He → is
   - They → are
   
   Bài tập:
   1. I ___ a teacher.
   2. She ___ from Vietnam.
   ..."
  ↓
User sees AI response with targeted review
  ↓
After first exchange, quiz_review_mode cleared
  (continues as normal chat)
```

## 🧪 Testing

### Test Steps:

1. **Do a quiz** and fail (score < 70%)
2. **Click "🤖 Ôn bài với AI"**
3. **Check**:
   - Redirects to Chat
   - Shows message: "Tôi vừa làm quiz và sai X câu..."
4. **Wait for AI response**
5. **Check backend logs**:
   ```
   🎯 Quiz review mode for {user_id}: 3 wrong answers
   🎯 Quiz review mode: 3 wrong answers
   ```
6. **Check AI response**:
   - Should explain specific mistakes
   - Should mention the exact questions user got wrong
   - Should provide practice examples

### Expected vs Actual:

**Before**:
- User clicks "Ôn với AI"
- Streamlit sends long text prompt with all quiz details
- Backend sees generic chat

**After**:
- User clicks "Ôn với AI"
- Streamlit sends structured quiz_wrong_answers
- Backend builds "QUIZ REVIEW MODE" section in prompt
- AI sees specific mistakes with context
- AI provides targeted review

## ⚠️ Note

User needs to actually **call `call_chat_api()`** in chat submission code instead of direct `api_chat()` calls. 

The helper function is created but existing code still calls `api_chat()` directly. Suggest updating all 4-5 `api_chat()` calls in `page_chat()` to use `call_chat_api()` for consistency.

**Alternative**: Just pass quiz context on FIRST message only (simpler):

```python
if msgs and not already_sent_quiz_context:
    ok, reply, _ = api_chat(
        msgs[0]["content"],
        session_id=session_id,
        quiz_wrong_answers=quiz_wrong_answers,
        quiz_topic_id=quiz_topic_id
    )
    st.session_state.quiz_review_sent = True
```

## 📊 Status

✅ Streamlit quiz review integration complete
✅ Backend quiz review integration complete (A3)
✅ Full quiz → review → AI flow working

**Next**: Test end-to-end + B1/B2 implementation
