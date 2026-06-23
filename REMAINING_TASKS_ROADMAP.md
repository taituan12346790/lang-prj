# Remaining Tasks Roadmap
## Current Progress: 82% → Goal: 100%

---

## 🎯 PRIORITY ORDER

### 🔴 HIGH PRIORITY (Core Functionality)

#### B3: Add Metadata to ChatResponse ⏱️ ~30 min
**Why**: Debugging and UI transparency - frontend should know what context backend used

**Tasks:**
1. Update `app/schemas/chat.py` - Add fields to `ChatResponse`:
   ```python
   learning_context: Optional[Dict[str, Any]] = None
   current_level: Optional[str] = None
   active_topic_id: Optional[str] = None
   active_topic_name: Optional[str] = None
   ```

2. Update `app/routers/chat.py` - Extract metadata before returning:
   ```python
   # Get user profile
   profile = await db.execute(select(UserProfile).where(...))
   
   # Build metadata
   metadata = {
       "learning_context": learning_context,
       "current_level": profile.current_level,
       "active_topic_id": str(profile.active_topic_id) if profile.active_topic_id else None,
       # ...
   }
   
   return ChatResponse(response=result, metadata=metadata)
   ```

3. **Test**: Call `/api/chat/` and verify response includes metadata

---

#### B4: Placement/Level-Up Updates Profile ⏱️ ~45 min
**Why**: After placement test or level-up test, `user_profiles.current_level` must update

**Tasks:**
1. Check `app/services/level_service.py` - Does `submit_placement_test()` update profile?
   ```python
   async def submit_placement_test(...):
       # ... calculate level ...
       
       # UPDATE PROFILE
       profile = await db.execute(select(UserProfile).where(...))
       profile.current_level = estimated_level
       db.add(profile)
       await db.commit()
   ```

2. Check `app/services/level_service.py` - Does `submit_level_up_test()` update profile?
   ```python
   async def submit_level_up_test(...):
       if passed:
           # UPDATE PROFILE TO NEXT LEVEL
           profile.current_level = next_level
           db.add(profile)
           await db.commit()
   ```

3. **Test**: 
   - Take placement test → check database: `SELECT current_level FROM user_profiles WHERE user_id = '...'`
   - Take level-up test → verify level increased

**Possible Files:**
- `app/services/level_service.py`
- `app/services/test_service.py` (if placement logic is here)
- `app/routers/test.py`

---

#### C1: Make Preset Buttons Functional ⏱️ ~20 min
**Why**: Users see "📖 Giải thích bài", "✏️ 5 câu luyện" buttons but they may not work correctly

**Tasks:**
1. In `streamlit_app.py` - Find preset button click handlers (~line 1730):
   ```python
   if st.button("📖 Giải thích bài"):
       # Should append to messages with specific prompt
       user_msg = "Giải thích chi tiết về bài học hiện tại"
       st.session_state.messages.append({"role": "user", "content": user_msg})
       st.rerun()
   ```

2. Verify each preset sends appropriate prompt:
   - "Giải thích bài" → "Explain current lesson's grammar in Vietnamese"
   - "5 câu luyện" → "Give me 5 practice sentences for current topic"
   - "Chat tự do" → Normal chat (no special prompt)

3. **Test**: Click each button, verify AI response is relevant

---

### 🟡 MEDIUM PRIORITY (Quality of Life)

#### B5: Unified Level-Up Eligibility Service ⏱️ ~2 hours
**Why**: Avoid two different logic paths for "can user level up"

**Tasks:**
1. Create `app/services/level_progress_service.py`:
   ```python
   class LevelProgressService:
       async def check_eligibility(self, user_id: UUID, db: AsyncSession) -> Dict:
           # Single source of truth for level-up rules
           # Check: topic completion %, average quiz score, test history
           return {
               "eligible": True/False,
               "current_level": "A1",
               "next_level": "A2",
               "requirements": {
                   "topics_completed": "3/4",
                   "quiz_avg": "85%",
                   "ready": True
               }
           }
   ```

2. Create API endpoint `GET /api/learning/level-up-eligibility`:
   ```python
   @router.get("/level-up-eligibility")
   async def get_level_up_eligibility(...):
       service = LevelProgressService()
       result = await service.check_eligibility(user_id, db)
       return result
   ```

3. Update Dashboard (`streamlit_app.py` - `page_dashboard()`):
   ```python
   eligibility = api_get_level_up_eligibility()
   if eligibility.get("eligible"):
       st.success("🎓 Bạn đủ điều kiện thi lên level!")
       if st.button("🚀 Thi lên level"):
           st.session_state.page = "level_up_test"
           st.rerun()
   ```

4. **Test**: Complete topics → check dashboard shows level-up button

---

#### C3: Auto-Activate Next Context ⏱️ ~30 min
**Why**: After completing lesson or quiz, user shouldn't need to manually activate next lesson

**Tasks:**
1. In `app/services/topic_service.py` - After `complete_lesson()`:
   ```python
   async def complete_lesson(self, topic_id, lesson_order, user_id, db):
       # Mark lesson complete
       # ...
       
       # AUTO-ACTIVATE NEXT LESSON
       next_lesson_order = lesson_order + 1
       next_lesson = await db.execute(select(Lesson).where(
           Lesson.topic_id == topic_id,
           Lesson.lesson_order == next_lesson_order
       ))
       if next_lesson.scalar_one_or_none():
           await self.activate_context(
               user_id=user_id,
               topic_id=topic_id,
               lesson_order=next_lesson_order,
               db=db
           )
   ```

2. In `app/services/topic_service.py` - After `submit_quiz()`:
   ```python
   async def submit_quiz(self, ...):
       # Calculate score
       # ...
       
       if passed:
           # AUTO-ACTIVATE NEXT TOPIC (if available)
           next_topic = await self._get_next_topic(current_level, db)
           if next_topic:
               await self.activate_context(
                   user_id=user_id,
                   topic_id=next_topic.id,
                   db=db
               )
   ```

3. **Test**: Complete lesson → chat → verify AI knows about next lesson

---

### 🟢 LOW PRIORITY (Polish)

#### C2: Chat Session History Sidebar ⏱️ ~1 hour
**Why**: Nice to have - see previous chat sessions grouped by topic

**Tasks:**
1. In `streamlit_app.py` - Add sidebar section in `page_chat()`:
   ```python
   with st.sidebar:
       st.markdown("### 💬 Lịch sử chat")
       sessions = api_chat_get_sessions(limit=20)
       
       # Group by topic
       by_topic = {}
       for s in sessions:
           topic_id = s.get("topic_id", "general")
           by_topic.setdefault(topic_id, []).append(s)
       
       for topic_id, topic_sessions in by_topic.items():
           st.markdown(f"**📚 {topic_sessions[0].get('topic_name', 'General')}**")
           for s in topic_sessions[:5]:  # Show last 5
               if st.button(f"📅 {s['created_at']}", key=f"session_{s['id']}"):
                   # Load session
                   st.session_state.chat_session_id = s["session_id"]
                   messages = api_chat_get_history(s["session_id"])
                   st.session_state.messages = messages
                   st.rerun()
   ```

2. **Test**: Have multiple chat sessions → verify sidebar shows them

---

#### C4: Unify AIContextService Usage ⏱️ ~1 hour
**Why**: Avoid duplicate context-building logic

**Tasks:**
1. Review `app/services/ai_context_service.py` - Does it exist?
2. If YES: Update `learning_service._build_learning_context_dict()` to use it
3. If NO: Create it and consolidate context logic
4. **Test**: Verify context is identical before/after refactor

---

## 📊 ESTIMATED TIME TO 100%

| Task | Priority | Time | Status |
|------|----------|------|--------|
| B3 - ChatResponse metadata | 🔴 High | 30 min | ⏳ TODO |
| B4 - Profile level update | 🔴 High | 45 min | ⏳ TODO |
| C1 - Preset buttons | 🔴 High | 20 min | ⏳ TODO |
| **HIGH PRIORITY TOTAL** | | **~1.5 hrs** | |
| B5 - Level-up service | 🟡 Medium | 2 hrs | ⏳ TODO |
| C3 - Auto-activate | 🟡 Medium | 30 min | ⏳ TODO |
| **MEDIUM PRIORITY TOTAL** | | **~2.5 hrs** | |
| C2 - Session sidebar | 🟢 Low | 1 hr | ⏳ TODO |
| C4 - Unify AIContext | 🟢 Low | 1 hr | ⏳ TODO |
| **LOW PRIORITY TOTAL** | | **~2 hrs** | |

**Total to 100%**: ~6 hours of focused work

---

## 🎯 RECOMMENDED APPROACH

### Session 4 (1.5 hrs): Core Fixes
- B3: Metadata ✅
- B4: Profile updates ✅
- C1: Preset buttons ✅

**Result**: System is **feature-complete** (95%)

---

### Session 5 (2.5 hrs): Quality Improvements
- B5: Level-up service ✅
- C3: Auto-activate ✅

**Result**: User experience is **smooth** (98%)

---

### Session 6 (Optional, 2 hrs): Polish
- C2: Session history ✅
- C4: Code cleanup ✅

**Result**: System is **production-ready** (100%)

---

## 🧪 FINAL TESTING CHECKLIST

Once all tasks complete, run this full test:

### End-to-End Flow:
1. ✅ Register new user → placement test → verify level saved
2. ✅ Dashboard shows correct level + topics
3. ✅ Click topic → "Học tiếp" → verify context activated
4. ✅ Chat with AI → verify AI knows current lesson
5. ✅ Click "Giải thích bài" preset → verify works
6. ✅ Complete lesson → verify next lesson auto-activated
7. ✅ Take quiz → fail some questions → click "Ôn với AI"
8. ✅ Verify quiz context persists in conversation
9. ✅ Continue chatting → verify profile learns (check DB weak_skills)
10. ✅ Complete all topics → verify level-up button appears
11. ✅ Take level-up test → verify level updated
12. ✅ Check metadata in API responses

### Database Checks:
```sql
-- Profile level updated?
SELECT current_level FROM user_profiles WHERE user_id = '...';

-- Conversations saved?
SELECT COUNT(*) FROM conversations WHERE user_id = '...';

-- Weak skills learning?
SELECT weak_skills FROM user_profiles WHERE user_id = '...';

-- Progress tracked?
SELECT * FROM user_topic_progress WHERE user_id = '...';
```

---

**Ready to continue? Start with Session 4 tasks (B3, B4, C1)** 🚀
