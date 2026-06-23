# 🚀 Quick Start Guide - AI Language Tutor

## ✅ System Status: FULLY OPERATIONAL

All code compiles, all imports work, all routes registered. Ready to run!

---

## 🏃 Get Started in 30 Seconds

### 1. Start Backend (Terminal 1)
```bash
cd d:\lang_prj
python -m uvicorn app.main:app --reload
```

Expected output:
```
Uvicorn running on http://127.0.0.1:8000
```

### 2. Start Frontend (Terminal 2)
```bash
cd d:\lang_prj
streamlit run streamlit_app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### 3. Access the App
Open your browser to: **http://localhost:8501**

---

## 👤 Test Account

### Create New Account:
1. Click "Đăng ký" (Register)
2. Enter any email (e.g., test@example.com)
3. Create a password (min 8 characters)
4. Choose native language: Vietnamese
5. Choose target language: English
6. Click "✅ Đăng ký"
7. You'll be directed to placement test

### Or Test with Placement Test:
After registration, you'll take a quick placement test to determine your level (A1-C2)

---

## 📚 How to Use the App

### Step 1: Dashboard
- See your current level
- View available topics
- Check your learning statistics

### Step 2: Choose Topic
- Browse topics available for your level
- Click on a topic to see lessons
- View progress bar for the topic

### Step 3: Select Lesson
- View lesson content
- Learn grammar/vocabulary
- See examples and explanations

### Step 4: Practice Exercises
- Answer practice questions
- **NEW:** If you answer wrong, AI will:
  - Analyze the error automatically
  - Show you the error type
  - Display error frequency (how many times you made this error)
  - Provide personalized Vietnamese explanation
  - Suggest what to do next

### Step 5: Take Quiz
- Test your knowledge on the topic
- Get detailed feedback
- See your accuracy

### Step 6: Chat with AI
- Chat freely with the AI tutor
- Practice conversation skills
- Chat history saved automatically
- Get personalized explanations

### Step 7: Analytics
- View your learning progress
- See which skills are weak
- Check study timeline
- Track accuracy by topic

---

## 🎓 The AI Error Correction System

### How It Works:

**Scenario:** You're practicing and answer a question incorrectly

```
Question:
  "Yesterday, I ___ to the market."
  a) go
  b) went
  c) am going

Your answer: go
Correct: went
```

**What Happens:**

1. ✅ System detects your error is TENSE_MISMATCH
2. ✅ System checks if you made this error before
3. ✅ System checks your error history
4. ✅ AI generates personalized feedback in Vietnamese

**First Time Error:**
```
ℹ️ Lần đầu thôi, đừng lo! 😊
Bạn vừa nhầm về thì của động từ (verb tense).
Động từ 'go' phải ở thì quá khứ: 'went'

Gợi ý: Đọc lại phần "Past Tense" trong bài học.
```

**Third Time Error:**
```
⚠️ Bạn đã sai 3 lần rồi!
Hãy ôn lại lý thuyết về Verb Tenses:
- I went (quá khứ đơn)
- I am going (hiện tại tiếp diễn)
- I will go (tương lai đơn)

→ Làm 5 bài tập để luyện tập
```

**Fifth+ Time Error:**
```
🔴 Bạn đã sai 5 lần với lỗi này!
Hãy quay lại học bài cơ bản về Verb Tenses trước.
Sau đó làm các bài tập từ mức A1.
```

---

## 🔧 System Architecture

### Backend (FastAPI)
- **Port:** 8000
- **Health check:** GET `/health`
- **Main routes:** `/api/learning`, `/api/chat`, `/api/quiz`, `/api/analytics`
- **Error analysis:** POST `/api/learning/analyze-error`

### Frontend (Streamlit)
- **Port:** 8501
- **Pages:** auth, dashboard, topics, lessons, quiz, chat, analytics
- **Automatic error detection:** When user answers wrong

### Database (SQLite)
- **Location:** Determined by `.env` file
- **Migrations:** Auto-applied on startup
- **Key tables:** users, lessons, quizzes, error_logs, conversations

---

## 💡 Key Features

### ✅ Complete Learning Path
- Lessons organized by CEFR level (A1 → C2)
- Structured progression
- Quiz system with scoring

### ✅ AI-Powered Error Detection
- Automatic error classification
- Hybrid approach (rules + LLM)
- 5+ error types detected
- Personalized correction

### ✅ Error Tracking & Analytics
- Frequency counting (how many times you made each error)
- Error history stored in database
- Weak skills identification
- Progress visualization

### ✅ Chat AI with History
- Free-form conversation with AI
- Chat history persisted to database
- Context-aware responses
- Retrievable anytime

### ✅ Personalized Learning
- Adaptive feedback based on error count
- Recommendations based on weak skills
- Custom learning path
- Progress tracking

---

## 🧪 Verify Everything Works

### Check Backend:
```bash
python -c "import app.main; print('✅ Backend OK')"
```

Expected output: `✅ Backend OK`

### Check Frontend:
```bash
python -m py_compile streamlit_app.py
```

Expected: No output = success ✅

### Run Tests:
```bash
python test_error_detection.py
```

Expected: All tests pass ✅

---

## 📊 Sample Data

When you first run the app, it will load:
- **Topics:** Grammar, Vocabulary, Listening, Speaking
- **Lessons:** ~20-50 per topic depending on level
- **Practice exercises:** ~5-10 per lesson
- **Quiz questions:** ~10-15 per topic

---

## 🆘 Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /PID <PID> /F
```

### Frontend won't connect to backend?
1. Check backend is running on port 8000
2. Check `.env` file has correct `API_BASE_URL`
3. Default: `API_BASE_URL=http://127.0.0.1:8000`

### Database error?
```bash
# Check tables exist
python check_tables.py

# Run migrations
python -m alembic upgrade head
```

### Chat not saving?
1. Check `/api/chat/save-message` endpoint is working
2. Verify database is connected
3. Check `conversations` table exists

---

## 📝 Important Notes

### Environment Variables (`.env` file):
```
API_BASE_URL=http://127.0.0.1:8000
DATABASE_URL=sqlite:///./app.db
OPENAI_API_KEY=your_key_here
ENVIRONMENT=development
```

### First Time Setup:
1. Backend starts → Creates tables if needed
2. Frontend connects → Can now login/register
3. User registers → Profile created with A1 level
4. User takes placement → Level updated
5. Ready to start learning!

### Security:
- Passwords hashed with bcrypt
- JWT tokens for authentication
- Sessions expire after 24 hours
- Sensitive data not logged

---

## 🎯 Next Steps

1. **Start the system** → Follow "Get Started" section above
2. **Register a test account** → Create account, take placement test
3. **Select a topic** → Choose one that matches your level
4. **Try a lesson** → Read content and practice
5. **Answer wrong on purpose** → See the error correction in action!
6. **Chat with AI** → Practice free conversation
7. **Check analytics** → See your progress tracked

---

## 📞 Useful Commands

```bash
# Start backend
python -m uvicorn app.main:app --reload

# Start frontend
streamlit run streamlit_app.py

# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:8501

# View database tables
python check_tables.py

# Run migrations
python -m alembic upgrade head

# Check logs
tail -f app.log (on Linux/Mac)
Get-Content app.log -Tail 50 (on Windows)
```

---

## 🎉 Ready?

Everything is working! Start the backend and frontend, then:

1. ✅ Backend: `python -m uvicorn app.main:app --reload`
2. ✅ Frontend: `streamlit run streamlit_app.py`
3. ✅ Open browser: `http://localhost:8501`
4. ✅ Register and start learning!

**Status: FULLY OPERATIONAL** 🚀

The AI tutor with error detection and personalized correction is ready to help users learn languages effectively!

