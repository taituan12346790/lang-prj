# 🏗️ AI Language Tutor - System Overview

## 🎨 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                      USER (Web Browser)                            │
│                    http://localhost:8501                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   FRONTEND (Streamlit App)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Pages:                                                       │  │
│  │  • Auth (Login/Register)                                    │  │
│  │  • Dashboard (Overview + Stats)                             │  │
│  │  • Topics (Browse by level A1-C2)                          │  │
│  │  • Lessons (Content + Examples)                            │  │
│  │  • Practice (✨ Error Detection Here)                       │  │
│  │  • Quiz (Assessment)                                        │  │
│  │  • Chat (Free conversation)                                │  │
│  │  • Analytics (Progress tracking)                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ API Functions:                                               │  │
│  │  • api_login() / api_register()                             │  │
│  │  • api_topics() / api_lesson()                              │  │
│  │  • api_quiz_questions() / api_submit_quiz()                │  │
│  │  • api_chat() / api_chat_save_message()                    │  │
│  │  • ✨ api_analyze_error() ← NEW!                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────┬──────────────────────────────┘
                                       │
                        HTTP POST/GET (httpx)
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI Server)                          │
│                     Port: 8000                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Auth Router  │  │ Learning     │  │ Chat Router  │            │
│  │              │  │ Path Router  │  │              │            │
│  │ /api/auth/*  │  │ /api/learning│  │ /api/chat/*  │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │        🎯 LEARNING PATH ROUTER (8 routes)                  │  │
│  │                                                              │  │
│  │  GET  /api/learning/dashboard        → Dashboard          │  │
│  │  GET  /api/learning/topics/{level}   → Topics list        │  │
│  │  GET  /api/learning/topic/{id}       → Topic details      │  │
│  │  GET  /api/learning/lesson/{id}      → Lesson content     │  │
│  │  POST /api/learning/.../complete     → Mark done          │  │
│  │  GET  /api/learning/eligibility      → Level-up check     │  │
│  │  ✨ POST /api/learning/analyze-error ← ERROR ANALYSIS!    │  │
│  │                                                              │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │         ✨ ERROR ANALYSIS PIPELINE                          │  │
│  │                                                               │  │
│  │  Request Input:                                             │  │
│  │    {                                                         │  │
│  │      "question": "_____ am a student",                      │  │
│  │      "user_answer": "She",                                  │  │
│  │      "correct_answer": "I",                                 │  │
│  │      "skill_tag": "pronouns_agreement",                     │  │
│  │      "lesson_id": "...",                                    │  │
│  │      "topic_id": "..."                                      │  │
│  │    }                                                         │  │
│  │                                                               │  │
│  │  Processing:                                                │  │
│  │    1. ErrorAnalyzer.classify()                              │  │
│  │       → Rule-based quick check                              │  │
│  │       → Error type: SUBJECT_VERB_AGREEMENT                  │  │
│  │                                                               │  │
│  │    2. ErrorAnalyzer.generate_explanation()                  │  │
│  │       → LLM generates Vietnamese explanation                │  │
│  │                                                               │  │
│  │    3. ErrorService.track_error()                            │  │
│  │       → Query: Check frequency in database                  │  │
│  │       → Save: Log error to user_error_logs                  │  │
│  │       → Increment: frequency counter                        │  │
│  │                                                               │  │
│  │    4. ErrorService.generate_suggestion()                    │  │
│  │       → If freq == 1: "Lần đầu, không sao..."              │  │
│  │       → If freq == 3: "Ôn lại lý thuyết + bài tập"        │  │
│  │       → If freq >= 5: "Quay lại cơ bản"                    │  │
│  │                                                               │  │
│  │  Response Output:                                           │  │
│  │    {                                                         │  │
│  │      "error_type": "SUBJECT_VERB_AGREEMENT",               │  │
│  │      "frequency": 3,                                        │  │
│  │      "severity": "medium",                                  │  │
│  │      "explanation": "...(Vietnamese)...",                   │  │
│  │      "suggestion": "...(personalized)...",                  │  │
│  │      "recommendation": {                                    │  │
│  │        "action": "practice",                                │  │
│  │        "items": [...]                                       │  │
│  │      }                                                       │  │
│  │    }                                                         │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              SERVICE LAYER                                   │  │
│  │                                                               │  │
│  │  • LearningService    → Learning logic                      │  │
│  │  • ErrorService       → Error tracking (✨ NEW)             │  │
│  │  • QuizService        → Quiz evaluation                     │  │
│  │  • AnalyticsService   → Stats & weak skills                │  │
│  │  • MemoryService      → Chat history management            │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              CORE LOGIC                                      │  │
│  │                                                               │  │
│  │  • ErrorAnalyzer       (✨ NEW - Hybrid classification)     │  │
│  │  • IntentClassifier                                          │  │
│  │  • LanguageParser                                           │  │
│  │  • PracticeGenerator                                        │  │
│  │  • LearningStrategy                                         │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                           SQLAlchemy ORM
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATABASE (SQLite)                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Users & Auth:                                                      │
│  ├─ users (id, email, password_hash)                              │
│  └─ user_profiles (user_id, level, native_lang, target_lang)     │
│                                                                      │
│  Learning Content:                                                  │
│  ├─ topics (id, name, level, description)                         │
│  ├─ lessons (id, topic_id, content)                               │
│  ├─ exercises (id, lesson_id, question, answer, explanation)     │
│  └─ quizzes (id, topic_id, questions, answers)                   │
│                                                                      │
│  Learning Progress:                                                 │
│  ├─ user_topic_progress (user_id, topic_id, accuracy, completed) │
│  ├─ exercise_results (id, user_id, exercise_id, is_correct)     │
│  └─ quiz_results (id, user_id, quiz_id, score)                   │
│                                                                      │
│  ✨ ERROR TRACKING (NEW):                                          │
│  └─ user_error_logs (user_id, error_type, frequency, severity,   │
│     skill_tag, created_at, updated_at)                            │
│     Indexes: (user_id, error_type), (user_id, skill_tag)         │
│                                                                      │
│  Chat Persistence:                                                  │
│  ├─ conversations (id, session_id, user_id, messages[])          │
│  └─ chat_messages (id, session_id, role, content, timestamp)     │
│                                                                      │
│  Analytics:                                                         │
│  └─ analytics_cache (user_id, weak_skills[], accuracy_by_topic)  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow: User Answers Wrong

```
USER INTERACTION:
   User sees practice question
   ├─ Question: "Yesterday I ___ to school"
   ├─ Options: a) go, b) went, c) am going
   └─ Selects: "a) go" ❌

FRONTEND DETECTS ERROR:
   Checks: user_choice ("go") != correct_answer ("went")
   ├─ Error detected: TRUE
   └─ Calls: api_analyze_error(...)

API CALL (HTTP POST):
   POST /api/learning/analyze-error
   Body: {
     "question": "Yesterday I ___ to school",
     "user_answer": "go",
     "correct_answer": "went",
     "skill_tag": "past_tense",
     "lesson_id": "abc123",
     "topic_id": "topic456"
   }

BACKEND PROCESSING:
   1. ErrorAnalyzer.classify(question, user_answer, correct_answer)
      ├─ Quick pattern match → TENSE_MISMATCH
      └─ LLM generates explanation in Vietnamese
   
   2. ErrorService.track_error(user_id, error_type, skill_tag)
      ├─ Query DB: SELECT * FROM user_error_logs WHERE...
      ├─ Check frequency: count = 2 (user made this error 2 times before)
      ├─ New frequency: 3 (this is 3rd time)
      ├─ Insert: new entry into user_error_logs
      └─ Increment counter: frequency = 3
   
   3. ErrorService.generate_suggestion(frequency=3)
      ├─ Since frequency == 3:
      ├─ Return: "Ôn lại lý thuyết + 5 bài tập"
      └─ Include: Example sentences + practice link

RESPONSE (HTTP JSON):
   {
     "error_type": "TENSE_MISMATCH",
     "frequency": 3,
     "severity": "medium",
     "explanation": "Động từ ở thì quá khứ đơn...",
     "suggestion": "Lần thứ 3 bạn sai! Ôn lại...",
     "recommendation": {
       "action": "practice",
       "items": ["exercise1", "exercise2", ...]
     }
   }

FRONTEND DISPLAYS ERROR:
   Error panel appears with:
   ├─ ⚠️ Badge (because frequency = 3)
   ├─ Explanation in Vietnamese
   ├─ Suggestion: "Ôn lại lý thuyết + 5 bài tập"
   ├─ Button: "Ôn lập" (Review)
   └─ Button: "Làm bài tập" (Practice)

USER SEES:
   Clear error feedback + personalized suggestion
   Can immediately access practice materials
   Progress tracked in database for next time
```

---

## 🧠 Error Classification System

```
HYBRID APPROACH:

┌─────────────────────────────────────┐
│   User Input                        │
│   {question, user_answer, correct}  │
└────────────────┬────────────────────┘
                 │
       ┌─────────┴─────────┐
       │                   │
       ▼                   ▼
┌──────────────┐   ┌──────────────┐
│ RULE-BASED   │   │ LLM-BASED    │
│ CLASSIFIER   │   │ CLASSIFIER   │
│              │   │              │
│ Fast (<100ms)│   │ Detailed     │
│              │   │ (1-2s)       │
│ Patterns:    │   │              │
│ • Tenses     │   │ Context-     │
│ • Agreement  │   │ aware        │
│ • Word order │   │ explanation  │
│ • Subject    │   │              │
│ • Spelling   │   │              │
└──────┬───────┘   └──────┬───────┘
       │                  │
       └──────────┬───────┘
                  │
                  ▼
       ┌─────────────────────┐
       │ COMBINE & VALIDATE  │
       │                     │
       │ error_type = rule   │
       │ explanation = llm   │
       │ confidence = both   │
       └────────────┬────────┘
                    │
                    ▼
       ┌─────────────────────┐
       │ RETURN RESULT       │
       │                     │
       │ {error_type,        │
       │  explanation,       │
       │  confidence}        │
       └─────────────────────┘

ERROR TYPES DETECTED:
  1. TENSE_MISMATCH          (past vs present)
  2. SUBJECT_VERB_AGREEMENT   (I am vs She am)
  3. WORD_ORDER              (wrong sentence structure)
  4. VOCABULARY_CHOICE       (wrong word for meaning)
  5. GRAMMATICAL_ERROR       (missing articles, etc.)
```

---

## 📈 Frequency-Based Personalization

```
ADAPTIVE FEEDBACK SYSTEM:

Error occurs
     │
     ▼
Check frequency in database
     │
     ├─────────────────┬───────────────┬───────────────┬─────────────────┐
     │                 │               │               │                 │
     ▼                 ▼               ▼               ▼                 ▼
   1st time         2nd time        3rd time        4th time          5th+
     │                 │               │               │                 │
     ▼                 ▼               ▼               ▼                 ▼
┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│ ENCOURAGE  │  │ EDUCATE    │  │ INTERVENE  │  │ INTENSIVE  │  │ RESET      │
├────────────┤  ├────────────┤  ├────────────┤  ├────────────┤  ├────────────┤
│ Badge: ℹ️  │  │ Badge: ⚠️  │  │ Badge: ⚠️  │  │ Badge: 🔴  │  │ Badge: 🔴  │
│            │  │            │  │            │  │            │  │            │
│ "Lần đầu   │  │ "Ôn lại    │  │ "Bạn đã    │  │ "Bạn đã    │  │ "Lỗi này   │
│ thôi, kh  │  │ lý thuyết"  │  │ sai 3      │  │ sai 4      │  │ rất phổ    │
│ óng lo!"   │  │            │  │ lần!"      │  │ lần!"      │  │ biến!"     │
│            │  │ + examples │  │            │  │            │  │            │
│ Action:    │  │ + practice │  │ Action:    │  │ Action:    │  │ Action:    │
│ Continue   │  │            │  │ Review     │  │ Review +   │  │ Go back    │
│ normally   │  │ Action:    │  │ theory +   │  │ Intensive  │  │ to basics  │
│            │  │ Do 3 more  │  │ 5 new      │  │ exercises  │  │ (A1)       │
│            │  │ exercises  │  │ exercises  │  │            │  │            │
│            │  │            │  │            │  │            │  │            │
└────────────┘  └────────────┘  └────────────┘  └────────────┘  └────────────┘
```

---

## 🔄 Chat Persistence Flow

```
USER OPENS CHAT:
   ├─ Session ID created (or retrieved if existing)
   └─ Chat history loaded from DB

USER TYPES MESSAGE:
   ├─ Message sent to AI
   └─ AI generates response

BOTH SAVED TO DATABASE:
   ├─ INSERT into conversations:
   │  {session_id, user_id, role="user", message, timestamp}
   ├─ INSERT into conversations:
   │  {session_id, user_id, role="assistant", response, timestamp}
   └─ Database now has full history

USER COMES BACK LATER:
   ├─ Same session ID used
   ├─ OLD messages retrieved from DB
   ├─ Chat history displayed (so AI remembers context)
   └─ Conversation continues naturally

MULTI-TURN CONVERSATION:
   Turn 1: User: "What is past tense?"
           AI: "Past tense is used for..."
           (both saved to DB)
   
   Turn 2: User: "Give me an example"
           AI retrieves last exchange from DB
           AI generates response with context
           Response saved to DB
   
   Turn 3: User: "How is it different from..."
           AI has full conversation history
           AI provides informed response
```

---

## ⚙️ Tech Stack

### Frontend
- **Framework:** Streamlit (Python)
- **HTTP Client:** httpx
- **State Management:** st.session_state
- **UI:** Custom CSS + Streamlit components

### Backend
- **Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **Migrations:** Alembic
- **AI/LLM:** OpenAI API (GPT-4)
- **Async:** asyncio

### Database
- **Default:** SQLite
- **Configurable:** PostgreSQL, MySQL, etc.
- **Tables:** 12+ (users, lessons, exercises, errors, chat, analytics)
- **Indexes:** 5+ for performance

### DevOps
- **Server:** Uvicorn (async)
- **Python Version:** 3.9+
- **Dependencies:** See requirements.txt
- **Environment:** .env file

---

## 🎯 User Journey Map

```
┌──────────────┐
│   START      │
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│ 1. REGISTER / LOGIN      │
│                          │
│ New user:                │
│ - Create account         │
│ - Take placement test    │
│ - Level determined       │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 2. DASHBOARD             │
│                          │
│ - View profile           │
│ - See available topics   │
│ - Check progress stats   │
└──────┬───────────────────┘
       │
       ▼ (Select Topic)
┌──────────────────────────┐
│ 3. TOPIC VIEW            │
│                          │
│ - See lessons in topic   │
│ - View progress          │
│ - Start lesson           │
└──────┬───────────────────┘
       │
       ▼ (Open Lesson)
┌──────────────────────────┐
│ 4. LESSON CONTENT        │
│                          │
│ - Read theory            │
│ - See examples           │
│ - Learn concepts         │
└──────┬───────────────────┘
       │
       ▼ (Practice)
┌──────────────────────────────────┐
│ 5. PRACTICE EXERCISES (✨ KEY!)  │
│                                  │
│ Answer Q1:                       │
│ ├─ Correct? → Next              │
│ └─ Wrong? → ✨ ERROR PANEL       │
│             • Type: TENSE        │
│             • Freq: 2nd error    │
│             • Suggestion: "Review"
│             • Action: Practice   │
│                                  │
│ Answer Q2... Q3... (repeat)      │
└──────┬───────────────────────────┘
       │
       ▼ (When ready)
┌──────────────────────────┐
│ 6. QUIZ ASSESSMENT       │
│                          │
│ - 10-15 questions        │
│ - Timed or untimed       │
│ - Immediate scoring      │
│ - Detailed feedback      │
└──────┬───────────────────┘
       │
       ├─ Score < 70%? → Review lesson
       │
       └─ Score ≥ 70%? → Topic complete!
                         Check eligibility
                         for Level Up
                         ▼
┌──────────────────────────┐
│ 7. PROGRESS TRACKING     │
│                          │
│ - View analytics         │
│ - See weak skills        │
│ - Check accuracy trends  │
│ - Plan next steps        │
└──────┬───────────────────┘
       │
       ├─ More practice? → Back to step 3
       │
       ├─ Chat & practice? → Chat AI
       │
       └─ Next level ready? → Level-up test
                              ▼
┌──────────────────────────┐
│ 8. LEVEL-UP TEST         │
│                          │
│ - Grammar test           │
│ - Score threshold        │
│ - New level assigned     │
│ - New topics unlock      │
└──────┬───────────────────┘
       │
       └──────────────────→ Back to step 3
                          (New topics available!)
```

---

## ✨ Summary

This system provides:
1. ✅ Complete structured learning path (A1 → C2)
2. ✅ **Intelligent error detection & correction** (Hybrid AI)
3. ✅ **Frequency-based adaptive feedback** (Smart personalization)
4. ✅ Persistent chat with history
5. ✅ Real-time progress analytics
6. ✅ AI-powered learning recommendations
7. ✅ Production-ready architecture

**The key innovation:** Automatic error analysis with personalized correction that improves with each attempt!

