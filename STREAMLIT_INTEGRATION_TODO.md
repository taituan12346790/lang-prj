# Streamlit Frontend Integration - Sprint 1

## Current State
- Streamlit frontend exists at `streamlit_app.py`
- Backend Sprint 1 is complete with new learning context endpoints

## What Streamlit Needs to Do

### 1. Load Learning Context on Startup (After Login)
**Location:** After user logs in and profile is loaded

```python
def _fetch_learning_context():
    """Fetch current learning context from backend"""
    ok, data, err = _get("/api/learning/context")
    if ok:
        st.session_state.learning_context = data
        return data
    return None

# After login, call:
_fetch_learning_context()
```

### 2. Activate Context When User Selects Topic
**Location:** In `page_topic()` or when user clicks "Học tiếp"

```python
def api_activate_learning_context(topic_id: str, lesson_order: int = 1) -> bool:
    """Activate topic/lesson as current learning context"""
    ok, _, err = _post("/api/learning/activate-context", {
        "topic_id": str(topic_id),
        "lesson_order": lesson_order,
        "learning_mode": "normal"  # or "quiz_review" if from quiz
    })
    if ok:
        # Refresh context
        _fetch_learning_context()
        return True
    return False

# When user clicks "Học tiếp" button:
if st.button("▶️ Học tiếp"):
    success = api_activate_learning_context(topic_id)
    if success:
        st.session_state.page = "chat"
        st.rerun()
    else:
        st.error("Không thể activate context")
```

### 3. Display Learning Context in AI Tutor Header
**Location:** In `page_chat()` at the top

```python
def _show_learning_context_header():
    """Display current learning context"""
    ctx = st.session_state.get("learning_context", {})
    
    if ctx.get("topic_name"):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"📚 **{ctx.get('topic_name')}**")
        with col2:
            lesson = ctx.get("lesson_title", "")
            if lesson:
                st.markdown(f"📖 Bài: {lesson}")
        with col3:
            level = ctx.get("current_level", "")
            if level:
                st.markdown(f"🎯 {level}")
    else:
        st.info("💬 Free Chat - Không có context")

# In page_chat():
_show_learning_context_header()
```

### 4. Automatic Context on Quiz Finish
**Location:** In `page_quiz_result()` after user finishes quiz

```python
# After quiz is submitted and results shown:
if st.button("🤖 Ôn bài với AI Tutor"):
    # Activate context with quiz_review mode
    ok, _, _ = _post("/api/learning/activate-context", {
        "topic_id": str(topic_id),
        "learning_mode": "quiz_review"
    })
    if ok:
        st.session_state.page = "chat"
        st.rerun()
```

### 5. Pass Context to Chat API (Optional)
**Location:** In `page_chat()` when sending message

Currently chat API doesn't need `topic_id` because backend loads it from profile. But if you want to be explicit:

```python
# In the chat input section:
ok, reply, _ = api_chat(
    msg=user_inp,
    # Backend will automatically use active_topic_id from profile
    # No need to pass here - just for reference if Sprint 2 changes this
)
```

---

## Complete Example: Adding "Học tiếp" Button to Dashboard

```python
# In page_dashboard() or page_topics():

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"### 📚 {topic['name']} ({topic['level']})")
    
with col2:
    if topic['progress']['status'] == 'in_progress':
        if st.button("▶️ Học tiếp", key=f"btn_continue_{topic['id']}"):
            # 1. Activate context
            ok, _, err = _post("/api/learning/activate-context", {
                "topic_id": str(topic['id']),
                "lesson_order": topic['progress']['lesson_completed'] + 1,
                "learning_mode": "normal"
            })
            if ok:
                # 2. Update local state
                st.session_state.learning_context = {
                    "topic_name": topic['name'],
                    "active_topic_id": topic['id'],
                    "learning_mode": "normal"
                }
                # 3. Navigate to chat
                st.session_state.page = "chat"
                st.rerun()
            else:
                st.error(f"Lỗi: {err}")
    
    elif topic['progress']['status'] == 'not_started':
        if st.button("▶️ Bắt đầu", key=f"btn_start_{topic['id']}"):
            ok, _, err = _post("/api/learning/activate-context", {
                "topic_id": str(topic['id']),
                "lesson_order": 1,
                "learning_mode": "normal"
            })
            if ok:
                st.session_state.page = "chat"
                st.rerun()
```

---

## Session State Variables to Add

```python
# In _init() function:
defaults = {
    ...existing...
    # NEW - Sprint 1
    "learning_context": None,  # Current learning context from backend
}
```

---

## Summary of Changes Needed

| Component | Changes |
|-----------|---------|
| Session State | Add `learning_context` |
| Functions | Add `api_activate_learning_context()` |
| Functions | Add `_fetch_learning_context()` |
| Dashboard | Add "Học tiếp" buttons that activate context |
| Chat Header | Show current topic/lesson being studied |
| Chat | Optionally show that context is active |
| Quiz Result | Add "Ôn với AI" button (sets mode=quiz_review) |

---

## Testing Checklist

After implementing:
- [ ] User logs in
- [ ] Learning context loads (can check with st.write(st.session_state.learning_context))
- [ ] Click "Học tiếp" on topic
- [ ] Navigate to chat
- [ ] Chat header shows topic name and lesson
- [ ] Send chat message - AI should mention the topic
- [ ] Complete quiz
- [ ] Click "Ôn bài với AI"
- [ ] Chat shows quiz_review mode

---

## Expected Behavior After Implementation

**Before (Current):**
```
User: Opens chat
AI: "Xin chào! Bạn muốn hỏi gì?"
```

**After (With Context):**
```
User: Clicks "Học tiếp" on "Present Simple" topic
User: Opens chat
Header: 📚 Present Simple | 📖 Bài: Affirmative Form | 🎯 A1

User: "Giải thích hộ"
AI: "Ừ, trong bài 'Affirmative Form' của 'Present Simple', chúng ta học cách sử dụng động từ 'to be' ở dạng khẳng định..."
```

---

**Status:** Ready for implementation
**Difficulty:** Easy (mostly HTTP calls)
**Time Estimate:** 1-2 hours
