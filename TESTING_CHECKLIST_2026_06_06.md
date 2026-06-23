# 🧪 Testing Checklist - AI Agent Improvements
**Date:** June 6, 2026  
**Purpose:** Validate end-to-end functionality after improvements

---

## ✅ Pre-deployment Testing Checklist

### 🔧 Unit Tests (Code-level)

- [x] **All Python files compile without syntax errors**
  ```bash
  python -m py_compile app/core/pipeline.py
  python -m py_compile app/services/learning_service.py
  python -m py_compile app/llm/prompts.py
  python -m py_compile app/core/learning_orchestrator.py
  ```
  **Status:** ✅ PASSED

- [x] **Validation test suite passes**
  ```bash
  python test_agent_improvements.py
  ```
  **Result:** 6/6 tests passed ✅

---

### 🎯 Feature Tests (Functional)

#### A1: Learning Context Display
- [ ] Vào Dashboard → Chọn topic → Bấm "Học tiếp"
- [ ] Chat page hiển thị expander "📚 Bạn đang học gì?"
- [ ] Expander shows:
  - [ ] Level (e.g., "A1")
  - [ ] Lesson completed (e.g., "1/4")
  - [ ] Quiz score (e.g., "80%" hoặc "Chưa làm")
  - [ ] Topic name (tiếng Việt)
  - [ ] Grammar focus
  - [ ] Current lesson title

**Expected:** Tất cả thông tin hiển thị chính xác từ backend
**Test by:** Manual UI testing

---

#### A2: Auto-activate Context
- [ ] Restart server
- [ ] Đăng nhập → Đi vào Dashboard → Chọn topic → "Học tiếp"
- [ ] Check backend log:
  ```
  ✅ AUTO-ACTIVATE: Context activated for topic <topic_id>
  ```
- [ ] Vào Chat → Context hiển thị đúng topic vừa chọn

**Expected:** Context tự động activate khi vào chat từ topic
**Test by:** Check backend logs + UI display

---

#### A3: Quiz Review Mode
- [ ] Làm quiz → Submit → Có câu sai
- [ ] Bấm nút "Ôn với AI"
- [ ] Chat page mở với quiz_review_mode = True
- [ ] AI response includes:
  - [ ] Phân loại lỗi
  - [ ] Giải thích lý thuyết
  - [ ] Ví dụ minh họa (3-5 examples)
  - [ ] Bài tập mới (5 bài)

**Expected:** AI phân tích chi tiết + cho bài tập ôn lỗi
**Test by:** Complete quiz with wrong answers

---

#### A4: Auto-save Conversation
- [ ] Gửi message trong chat
- [ ] Check database:
  ```sql
  SELECT * FROM conversations 
  WHERE user_id = '<user_id>' 
  ORDER BY created_at DESC 
  LIMIT 10;
  ```
- [ ] Verify 2 rows per turn (user + assistant)

**Expected:** Mỗi turn tạo 2 rows trong DB
**Test by:** Database query after chat

---

#### A5: Load Short-term from DB
- [ ] Chat 5-10 messages
- [ ] Restart uvicorn server
- [ ] Vào lại cùng chat session
- [ ] Gửi message → AI nhớ context conversation trước

**Expected:** AI reference được tin nhắn cũ trong response
**Test by:** Manual conversation testing after restart

---

#### A6: Lesson Progress in Context
- [ ] Complete lesson 1, 2
- [ ] Vào chat → Check learning context hiển thị "2/4"
- [ ] Làm quiz → Score 75%
- [ ] Vào chat → Check hiển thị "Quiz: 75%"

**Expected:** Progress update real-time
**Test by:** Complete lessons + check UI

---

#### B2: Reflect → Memory
- [ ] Chat về một lỗi ngữ pháp (e.g., past tense)
- [ ] AI giải thích và sửa lỗi
- [ ] Check database:
  ```sql
  SELECT weak_skills FROM user_topic_progress 
  WHERE user_id = '<user_id>' AND topic_id = '<topic_id>';
  ```
- [ ] Verify weak_skills updated with grammar error

**Expected:** Profile tự động update weak_skills
**Test by:** Database query after reflection

---

#### B3: Metadata in Response
- [ ] Gửi chat message
- [ ] Check browser console / Network tab
- [ ] Response có metadata:
  ```json
  {
    "metadata": {
      "current_level": "A1",
      "active_topic_id": "...",
      "learning_context": {...},
      "suggested_actions": [...]
    }
  }
  ```

**Expected:** Full metadata trả về
**Test by:** Browser DevTools

---

#### C1: Preset Buttons
- [ ] Vào chat với active context
- [ ] Click "📖 Giải thích bài"
  - [ ] AI giải thích lesson content
- [ ] Click "✏️ 5 câu luyện"
  - [ ] AI tạo 5 bài tập
- [ ] Click "💬 Chat tự do"
  - [ ] Input field focus, không auto-send

**Expected:** Preset buttons work correctly
**Test by:** Manual button clicks

---

#### C2: Sidebar Chat History
- [ ] Chat với 2-3 topics khác nhau
- [ ] Refresh page
- [ ] Check sidebar:
  - [ ] Sessions grouped by topic
  - [ ] Show last 3 sessions per topic
  - [ ] Click session → Load history

**Expected:** History organized by topic
**Test by:** Manual sidebar testing

---

#### C3: Auto-activate Next Lesson
- [ ] Vào lesson 1 → Complete
- [ ] Check backend log:
  ```
  ✨ C3: Auto-activated next lesson 2 for user <user_id>
  ```
- [ ] Profile active_lesson_order = 2
- [ ] Vào chat → Context shows lesson 2

**Expected:** Next lesson auto-activated after complete
**Test by:** Complete lesson + check logs/DB

---

### 🎭 Phase 3: Orchestrator & Suggested Actions

#### Suggested Actions Display
- [ ] Chat trong lesson context
- [ ] AI response có nút gợi ý (1-3 buttons)
- [ ] Buttons show correct labels:
  - [ ] "✏️ Làm 3-5 câu luyện tập" (OFFER_PRACTICE)
  - [ ] "✅ Hoàn thành bài X" (COMPLETE_LESSON)
  - [ ] "🎯 Làm quiz kiểm tra" (START_QUIZ)
  - [ ] "🚀 Thi lên level" (START_LEVEL_UP_TEST)

**Expected:** Actions relevant to current state
**Test by:** Manual conversation + check actions

#### Action Execution
- [ ] Click "✅ Hoàn thành bài 1"
  - [ ] Success toast
  - [ ] Redirect to lesson 2
  - [ ] DB updated: lesson_completed = 1
- [ ] Click "🎯 Làm quiz"
  - [ ] Redirect to quiz page
  - [ ] Quiz loads correctly
- [ ] Click "🚀 Thi lên level"
  - [ ] Redirect to level-up test
  - [ ] Test loads

**Expected:** Actions execute and redirect correctly
**Test by:** Click each action type

---

### 🔄 Integration Tests (End-to-End Flow)

#### Flow 1: New User → First Lesson → Chat
1. [ ] Register new account
2. [ ] Placement test → Level A1
3. [ ] Dashboard → Choose "Greetings & Introductions"
4. [ ] Click "Học tiếp" → Lesson 1
5. [ ] Read lesson → Click "Chat với AI Tutor"
6. [ ] Chat shows context: Topic, Lesson 1, Grammar focus
7. [ ] Ask question → AI explains với context
8. [ ] Click preset "✏️ 5 câu luyện"
9. [ ] AI generates 5 exercises
10. [ ] Suggested action: "✅ Hoàn thành bài 1"
11. [ ] Click → Redirect to Lesson 2
12. [ ] Check DB: lesson_completed = 1, active_lesson_order = 2

**Expected:** Smooth flow from lesson → chat → practice → complete
**Duration:** ~10 minutes

---

#### Flow 2: Quiz → Wrong Answers → Review
1. [ ] Login existing user
2. [ ] Go to topic with 4 lessons completed
3. [ ] Click "Làm quiz"
4. [ ] Answer quiz with 3 wrong answers
5. [ ] Results page shows wrong answers
6. [ ] Click "Ôn với AI"
7. [ ] Chat opens in quiz_review_mode
8. [ ] AI analyzes all 3 mistakes
9. [ ] AI provides:
   - [ ] Error classification
   - [ ] Theory explanation
   - [ ] 3-5 examples
   - [ ] 5 practice exercises
10. [ ] User does exercises → Chat again → AI remembers

**Expected:** Quiz review comprehensive and helpful
**Duration:** ~15 minutes

---

#### Flow 3: Multi-session Memory
1. [ ] Login
2. [ ] Chat 5-10 messages about past tense
3. [ ] Logout
4. [ ] Restart server
5. [ ] Login same user
6. [ ] Go to chat (same session_id)
7. [ ] Ask follow-up question about past tense
8. [ ] AI references previous conversation

**Expected:** AI remembers past conversation
**Duration:** ~8 minutes

---

### ⚡ Performance Tests

#### Response Time
- [ ] Chat response < 5 seconds (normal mode)
- [ ] Chat response < 8 seconds (quiz_review mode)
- [ ] Learning context API < 500ms
- [ ] Suggested actions generate < 100ms

**Expected:** Fast response times
**Test by:** Browser DevTools Network tab

#### Database Load
- [ ] Monitor DB queries per chat turn
- [ ] Should be < 10 queries per turn
- [ ] Check for N+1 queries

**Expected:** Efficient DB access
**Test by:** Django Debug Toolbar / logging

---

### 🐛 Error Handling Tests

#### Missing Context
- [ ] New user (no active topic)
- [ ] Vào chat → Warning message hiển thị
- [ ] "⚠️ Bạn chưa chọn bài học nào..."
- [ ] Button "🏠 Về Dashboard"

**Expected:** Graceful degradation
**Test by:** New user → chat directly

#### Backend Errors
- [ ] Stop backend
- [ ] Try to chat → Error message friendly
- [ ] Start backend → Resume chat

**Expected:** No crash, clear error messages
**Test by:** Simulate backend down

---

## 📊 Test Summary Template

```
============================================================
🧪 TESTING RESULTS - AI AGENT IMPROVEMENTS
============================================================

Date: _______________________
Tester: _____________________

UNIT TESTS:
  [x] Code compilation: PASS
  [x] Validation suite: 6/6 PASS

FEATURE TESTS:
  [ ] A1: Learning Context Display
  [ ] A2: Auto-activate Context
  [ ] A3: Quiz Review Mode
  [ ] A4: Auto-save Conversation
  [ ] A5: Load Short-term from DB
  [ ] A6: Lesson Progress
  [ ] B2: Reflect → Memory
  [ ] B3: Metadata
  [ ] C1: Preset Buttons
  [ ] C2: Sidebar History
  [ ] C3: Auto-activate Next

ORCHESTRATOR:
  [ ] Suggested Actions Display
  [ ] Action Execution

END-TO-END FLOWS:
  [ ] Flow 1: New User → First Lesson → Chat
  [ ] Flow 2: Quiz → Wrong Answers → Review
  [ ] Flow 3: Multi-session Memory

PERFORMANCE:
  [ ] Response time < 5s
  [ ] DB queries efficient

ERROR HANDLING:
  [ ] Missing context handled
  [ ] Backend errors graceful

OVERALL STATUS: _______________ (PASS / FAIL / PARTIAL)

BLOCKERS:
  - 
  - 

NOTES:
  - 
  - 

============================================================
```

---

## 🚦 Go/No-Go Decision Criteria

### ✅ GO (Deploy to Staging):
- All unit tests pass
- Critical features work (A1-A6)
- No P0 bugs
- Core flows complete (Flow 1, 2)

### ⚠️ CONDITIONAL GO (Deploy with warnings):
- Minor UI issues (polish)
- Performance slightly slower (but < 10s)
- Non-critical features have issues (C2, C3)

### 🛑 NO-GO (Fix before deploy):
- Unit tests fail
- P0 bugs exist
- Core features broken (A1-A4)
- Data loss or corruption risk
- Security vulnerabilities

---

## 📝 Bug Report Template

```
**Bug ID:** BUG-YYYYMMDD-##
**Severity:** P0 / P1 / P2 / P3
**Feature:** [A1 / A2 / etc.]
**Summary:** One-line description

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected:**

**Actual:**

**Screenshots/Logs:**

**Environment:**
- Browser: 
- Backend version: 
- Database: 

**Assigned to:**
**Status:** Open / In Progress / Fixed / Closed
```

---

## ✅ Sign-off

**Testing Plan Created by:** Kiro AI Agent  
**Date:** June 6, 2026  
**Status:** Ready for QA Team

**Note:** Đây là checklist toàn diện. Ưu tiên test các features nhóm A trước, sau đó B, C. End-to-end flows là critical để validate tích hợp.
