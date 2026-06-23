# Next Steps & Roadmap 🗺️

## Current Status: Phase 3 Complete ✅

**Agent Control**: 55-65% (target achieved!)  
**Phase 0-3**: All implemented  
**Phase 4-5**: Optional (can be done later)

---

## Immediate Next Steps (Required)

### 1. End-to-End Testing 🧪
**Priority**: HIGH  
**Time**: 1-2 hours  
**Owner**: User

**Tasks**:
- [ ] Login to Streamlit (http://localhost:8501)
- [ ] Test Scenario 1: Regular chat with action buttons
- [ ] Test Scenario 2: Practice action (offer_practice)
- [ ] Test Scenario 3: Complete lesson action
- [ ] Test Scenario 4: Start quiz action
- [ ] Test Scenario 5: Quiz review mode
- [ ] Test Scenario 6: Level-up eligibility
- [ ] Document any bugs found

**Reference**: See `PHASE_3_TEST_GUIDE.md`

---

### 2. Bug Fixes (If Any) 🐛
**Priority**: HIGH  
**Time**: Varies based on issues  
**Owner**: Developer

**Common Issues to Watch**:
- Action buttons not appearing → Check metadata capture
- Buttons not responding → Check browser console
- Wrong actions suggested → Check learning_context
- Redirect failures → Check page state management

**Debugging**:
- Backend logs: `Get-Content backend.log -Wait -Tail 50`
- Frontend debug: Add `st.write("metadata:", metadata)`
- API test: `python test_phase3_api.py`

---

## Optional Enhancements (Phase 4-5)

### Phase 4: Level-Up Eligibility in Analytics 📊
**Priority**: MEDIUM  
**Time**: 2-3 hours  
**Goal**: Add eligibility check to analytics_context automatically

**Current State**:
- `/api/learning/level-up-eligibility` endpoint exists (B5)
- `LevelProgressService` has unified eligibility check
- Analytics dashboard shows basic metrics

**What's Missing**:
- Analytics dashboard doesn't include eligibility status
- Agent doesn't automatically know when user is eligible

**Implementation**:
1. Add eligibility check to `api_analytics_dashboard()`
2. Include in analytics_context string for prompts
3. Orchestrator already suggests level-up action if eligible
4. Test: Complete 2 topics → Check if action appears

**Files to Modify**:
- `app/routers/analytics.py` (add eligibility to dashboard response)
- `streamlit_app.py` (include eligibility in analytics_context)

---

### Phase 5: UI Unification 🎨
**Priority**: LOW  
**Time**: 8-10 hours  
**Goal**: Merge lesson/quiz/chat into one unified page

**Current Problem**:
- User navigates between separate pages
- Context switches lose conversation flow
- Multiple page transitions = friction

**Proposed Solution**:
```
┌─────────────────────────────────────┐
│  AI Language Tutor                  │
├─────────────────────────────────────┤
│  [Dashboard] [Learning] [Analytics] │  ← Tabs
├─────────────────────────────────────┤
│                                     │
│  Learning Tab:                      │
│  ┌───────────────────────────────┐ │
│  │ 📚 Current: Numbers & Age     │ │
│  │ Progress: 2/4 lessons         │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 💬 Chat with AI Tutor         │ │
│  │                               │ │
│  │ User: xin chào                │ │
│  │ AI: [response]                │ │
│  │                               │ │
│  │ 💡 Actions:                   │ │
│  │ [Practice] [Quiz] [Complete]  │ │
│  └───────────────────────────────┘ │
│                                     │
│  When user clicks [Quiz]:          │
│  ┌───────────────────────────────┐ │
│  │ 🎯 Quiz: Numbers & Age        │ │
│  │                               │ │
│  │ Question 1/10: [...]          │ │
│  │ [ ] A [ ] B [ ] C [ ] D       │ │
│  │                               │ │
│  │ [Previous] [Next] [Submit]    │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

**Benefits**:
- No page transitions
- Persistent chat history
- Smoother UX
- All features in one place

**Challenges**:
- Complex state management
- Need to rewrite page layouts
- Risk of breaking existing features

**Recommendation**: Do this AFTER Phase 4 and user testing

**Files to Modify**:
- `streamlit_app.py` (major refactor)
- Merge `page_chat()`, `page_lesson()`, `page_quiz()` into `page_learning()`

---

## Future Ideas (Beyond Phase 5)

### 1. Adaptive Difficulty 🎚️
**Concept**: Agent adjusts content difficulty based on performance
- If user gets 90%+ → Suggest harder material
- If user struggles → Simplify explanations

**Implementation**:
- Track accuracy per lesson/topic
- Add difficulty_level to lesson content
- Agent chooses content based on user skill

---

### 2. Spaced Repetition Automation 🔄
**Concept**: Agent automatically schedules reviews
- Track last review date per topic
- Calculate optimal review interval (1d, 3d, 7d, 14d...)
- Suggest review when due

**Implementation**:
- Add `last_reviewed_at` to user_topic_progress
- Orchestrator checks for due reviews
- Already has `REVIEW_WEAK_SKILL` action type

---

### 3. Voice Input/Output 🎤
**Concept**: Practice speaking with AI
- User speaks → Speech-to-text → Agent
- Agent responds → Text-to-speech → User hears

**Implementation**:
- Frontend: Use Web Speech API or Whisper
- Backend: Add TTS service (Google TTS, Azure TTS)
- Store audio recordings for review

---

### 4. Multi-modal Learning 📸
**Concept**: Learn with images, videos, audio
- Agent shows images to teach vocabulary
- User uploads images to describe
- Videos for listening practice

**Implementation**:
- Add media_url to lesson content
- Frontend displays images/videos
- Agent generates questions about media

---

### 5. Peer Learning 👥
**Concept**: Match users for practice conversations
- Find users at similar level
- Pair for chat practice
- Agent moderates conversation

**Implementation**:
- Add matchmaking service
- WebSocket for real-time chat
- Agent provides feedback after session

---

### 6. Gamification 🎮
**Concept**: Add game elements for engagement
- Points, badges, leaderboards
- Daily challenges, streaks
- Unlock rewards (new topics, features)

**Implementation**:
- Add points system to database
- Track achievements
- Display progress visually

---

## Technical Debt & Refactoring

### Code Quality:
- [ ] Add type hints to all functions
- [ ] Add docstrings to all classes/methods
- [ ] Split large files (streamlit_app.py is 2500+ lines)
- [ ] Extract common utilities

### Testing:
- [ ] Add unit tests for orchestrator
- [ ] Add integration tests for execute-action
- [ ] Add E2E tests for critical flows
- [ ] Set up CI/CD pipeline

### Performance:
- [ ] Cache frequently used data (topics, lessons)
- [ ] Optimize database queries (add indexes)
- [ ] Profile slow endpoints
- [ ] Add request logging/monitoring

### Security:
- [ ] Audit authentication/authorization
- [ ] Add rate limiting
- [ ] Sanitize user inputs
- [ ] Add CSRF protection

---

## Recommended Prioritization

### Week 1 (Current):
1. ✅ Complete Phase 0-3 implementation
2. ⏳ End-to-end testing
3. ⏳ Fix critical bugs

### Week 2:
1. Phase 4: Analytics + eligibility
2. User feedback collection
3. Minor UX improvements

### Week 3:
1. Spaced repetition automation (high value, low effort)
2. Performance optimization
3. Code refactoring

### Week 4:
1. Phase 5: UI unification (if needed)
2. Add unit tests
3. Documentation updates

### Month 2+:
1. Voice input/output
2. Multi-modal learning
3. Gamification
4. Peer learning (if demand exists)

---

## Success Metrics to Track

### User Engagement:
- Daily active users (DAU)
- Average session duration
- Messages per session
- Return rate (7-day, 30-day)

### Learning Outcomes:
- Lesson completion rate
- Quiz pass rate (>80%)
- Topic completion rate
- Level-up rate

### Agent Performance:
- Action button click rate
- Action completion rate
- User satisfaction (survey)
- Error rate

### System Health:
- API response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- Uptime percentage
- Database query performance

---

## Resources Needed

### For Phase 4-5:
- Developer time: 10-15 hours
- Testing time: 5 hours
- No additional infrastructure

### For Voice/Multi-modal:
- TTS/STT API subscription ($10-50/month)
- Media storage (S3/Cloud Storage)
- Additional bandwidth

### For Peer Learning:
- WebSocket infrastructure
- Real-time messaging service
- Moderation tools

---

## Decision Points

### Should we do Phase 4 or Phase 5 first?
**Recommendation**: Phase 4 first
- **Why**: Lower risk, faster to implement
- **Impact**: Improves agent intelligence
- **Phase 5**: Bigger refactor, can wait for user feedback

### Should we prioritize new features or code quality?
**Recommendation**: Balance both
- **Week 1-2**: New features (Phase 4)
- **Week 3**: Code quality (tests, refactoring)
- **Week 4**: New features (if needed) or stabilization

### Should we add voice/multi-modal now?
**Recommendation**: Wait until after Phase 5
- **Why**: Core features should stabilize first
- **Risk**: Adding too many features too fast
- **Better**: Get user feedback first

---

## Contact & Support

### Documentation:
- `cursor_goi_y.txt` - Full analysis and recommendations
- `PHASE_3_COMPLETION.md` - Phase 3 implementation details
- `PHASE_3_TEST_GUIDE.md` - Testing instructions
- `SESSION_4_COMPLETE.md` - Session summary

### Key Files:
- Orchestrator: `app/core/learning_orchestrator.py`
- Execute action: `app/routers/learning_path.py`
- Action rendering: `streamlit_app.py` (lines 2090-2150)

### Debugging:
- Backend logs: `backend.log`
- Test script: `python test_phase3_api.py`
- Frontend debug: `st.write("metadata:", metadata)`

---

## Conclusion

**Current Achievement**: Phase 0-3 complete, Agent control at 55-65% ✅

**Next Milestone**: Phase 4 + user testing + code quality improvements

**Long-term Vision**: Adaptive, voice-enabled, multi-modal AI tutor with peer learning

**Timeline**: 4-8 weeks for core features, 3-6 months for advanced features

---

**Created**: June 5, 2026  
**Status**: Roadmap draft  
**Owner**: Product/Development team
