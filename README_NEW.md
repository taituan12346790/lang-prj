# 🎓 AI Language Tutor - Hệ Thống Học Tiếng Anh Thông Minh

> **Lộ trình học có cấu trúc từ A1 → C2 theo chuẩn CEFR**  
> 190 chủ đề • 760 bài học • Quiz tự động • AI Tutor 24/7

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)

---

## 📋 Giới Thiệu

**AI Language Tutor** là hệ thống học tiếng Anh hoàn chỉnh với:

✅ **Lộ trình học có cấu trúc** - 190 chủ đề từ A1 → C2  
✅ **4 bài học / chủ đề** - Grammar → Vocabulary → Practice → Quiz  
✅ **Quiz tự động chấm** - 10 câu hỏi, điểm tức thì  
✅ **Level-Up Test** - Khi hoàn thành ≥75% chủ đề  
✅ **AI Tutor Chat** - Hỗ trợ 24/7, luyện hội thoại  
✅ **Dashboard trực quan** - Theo dõi tiến độ, điểm số  

---

## 🚀 Khởi Động Nhanh

### 1. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình Database

```bash
# Tạo database PostgreSQL
createdb ai_language_tutor

# Chạy migrations
alembic upgrade head
```

### 3. Chạy Backend

```bash
python -m uvicorn app.main:app --reload
```

✅ Backend: `http://127.0.0.1:8000`  
📄 API Docs: `http://127.0.0.1:8000/docs`

### 4. Chạy Frontend

```bash
streamlit run streamlit_app.py
```

✅ Frontend: `http://localhost:8501`

---

## 📚 Tài Liệu

| Tài Liệu | Mô Tả |
|----------|-------|
| **[HUONG_DAN_SU_DUNG.md](HUONG_DAN_SU_DUNG.md)** | 📖 Hướng dẫn sử dụng cho người dùng cuối |
| **[LEARNING_PATH_SYSTEM.md](LEARNING_PATH_SYSTEM.md)** | 🏗️ Kiến trúc hệ thống chi tiết |
| **[SUMMARY_COMPLETION.md](SUMMARY_COMPLETION.md)** | ✅ Tóm tắt những gì đã hoàn thành |
| **[can_bo_sung.txt](can_bo_sung.txt)** | 📝 Yêu cầu ban đầu |
| **[y_tuong_moi.txt](y_tuong_moi.txt)** | 💡 Ý tưởng và thiết kế hệ thống |

---

## 🎯 Tính Năng Chính

### 🗺️ Lộ Trình Học Có Cấu Trúc

```
A1 (20 chủ đề) → A2 (25 chủ đề) → B1 (30 chủ đề)
     ↓              ↓                  ↓
B2 (35 chủ đề) → C1 (40 chủ đề) → C2 (40 chủ đề)
```

**Tổng cộng: 190 chủ đề = ~100 giờ học**

### 📖 4 Bài Học / Chủ Đề

```
1️⃣ Grammar      → Giải thích ngữ pháp + ví dụ
2️⃣ Vocabulary   → Danh sách từ + phát âm
3️⃣ Practice     → Bài tập thực hành
4️⃣ Quiz         → 10 câu hỏi kiểm tra
```

### 📊 Dashboard Trực Quan

```
┌─────────────────────────────────────┐
│ 📊 Tiến độ Level A1: 25%           │
│ ████████░░░░░░░░ (5/20 chủ đề)     │
│                                     │
│ ✅ Hoàn thành: 5                    │
│ 🔵 Đang học: 1                      │
│ ⬜ Chưa học: 14                     │
│ 📝 Điểm TB: 82%                     │
└─────────────────────────────────────┘
```

### 🏆 Level-Up Test

**Điều kiện:**
- ✅ Hoàn thành ≥75% chủ đề
- ✅ Điểm quiz trung bình ≥70%

**Kết quả:**
- Pass (≥75%) → Nâng lên level tiếp theo
- Fail → Ôn tập và thử lại

### 💬 AI Tutor Chat

- Hỏi về ngữ pháp
- Luyện hội thoại
- Ôn tập kiến thức
- Luôn có sẵn 24/7

---

## 🏗️ Kiến Trúc

### Backend (FastAPI)

```
app/
├── api/           # API routes
├── core/          # Config, database, security
├── data/          # Topics data (190 chủ đề)
├── llm/           # LLM integration
├── memory/        # Memory management
├── models/        # Database models
├── rag/           # RAG system
├── routers/       # API endpoints
├── schemas/       # Pydantic schemas
├── services/      # Business logic
├── tools/         # AI tools
└── main.py        # FastAPI app
```

### Frontend (Streamlit)

```
streamlit_app.py   # Single-file frontend
├── Auth Page      # Đăng nhập/đăng ký
├── Placement Test # Xác định trình độ
├── Dashboard      # Tổng quan tiến độ
├── Topics List    # Danh sách chủ đề
├── Topic Detail   # 4 bài học
├── Lesson View    # Nội dung bài học
├── Quiz          # Kiểm tra
├── Quiz Result    # Kết quả
├── Chat          # AI Tutor
└── Level-Up Test  # Nâng cấp
```

### Database Schema

```
topics                  # 190 chủ đề
├── id
├── level (A1-C2)
├── order
├── name / name_vi
└── ...

lessons                 # 760 bài học
├── id
├── topic_id
├── order (1-4)
├── lesson_type
└── content (JSONB)

user_topic_progress    # Tiến độ
├── user_id
├── topic_id
├── status
├── lesson_completed
├── quiz_score
└── ...
```

---

## 📊 Thống Kê

| Metric | Giá Trị |
|--------|---------|
| **Topics** | 190 |
| **Lessons** | 760 |
| **Quiz Questions** | ~1,900 |
| **Levels** | 6 (A1-C2) |
| **Backend LOC** | ~3,000 |
| **Frontend LOC** | ~1,350 |
| **Database Tables** | 12 |
| **API Endpoints** | 25+ |

---

## 🎬 Demo Workflow

### 1. Đăng ký & Placement Test
```
Đăng ký → Placement Test (20 câu) → Xác định level: A1
```

### 2. Dashboard
```
Dashboard hiển thị:
- Level hiện tại: A1
- Tiến độ: 0/20 (0%)
- Chủ đề tiếp theo: "Greetings"
→ [🚀 Bắt đầu học]
```

### 3. Học Chủ Đề
```
Topic: Greetings
├─ 1️⃣ Grammar     [Bắt đầu]
├─ 2️⃣ Vocabulary  🔒
├─ 3️⃣ Practice    🔒
└─ 4️⃣ Quiz        🔒

→ Học tuần tự → Quiz pass → ✅ Hoàn thành
```

### 4. Tiến độ & Level-Up
```
Sau 15/20 chủ đề + điểm TB 82%:
→ 🏆 Level-Up Test sẵn sàng
→ Pass → Nâng lên A2
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Python async web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM (async)
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Authentication
- **Loguru** - Logging

### Frontend
- **Streamlit** - Rapid UI development
- **httpx** - HTTP client
- **Custom CSS** - Styling

### AI & NLP
- **LangChain** - Agentic framework
- **OpenAI GPT** - Chat tutor
- **RAG** - Retrieval from grammar books

---

## 📝 API Endpoints

### Learning Path
```
GET  /api/learning/dashboard
GET  /api/learning/topics/{level}
GET  /api/learning/topic/{topic_id}
GET  /api/learning/lesson/{lesson_id}
POST /api/learning/topic/{topic_id}/lesson/{order}/complete
```

### Quiz
```
GET  /api/quiz/topic/{topic_id}/questions
POST /api/quiz/topic/{topic_id}/submit
```

### Test
```
GET  /api/test/placement/questions
POST /api/test/placement
GET  /api/test/level/{level}/questions
POST /api/test/level-up
```

### Auth
```
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/google
```

---

## 🔐 Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/ai_language_tutor

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# OpenAI
OPENAI_API_KEY=sk-...

# Google OAuth (optional)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# API Base URL
API_BASE_URL=http://127.0.0.1:8000
```

---

## 🚀 Deployment

### Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f
```

### Manual

```bash
# Backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
streamlit run streamlit_app.py --server.port 8501
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👥 Team

**AI Language Tutor Development Team**

---

## 📧 Contact

For questions or support:
- Email: support@ailanguagetutor.com
- Issues: [GitHub Issues](https://github.com/your-repo/issues)

---

## 🎉 Acknowledgments

- **CEFR Framework** - Common European Framework of Reference for Languages
- **OpenAI** - GPT models
- **FastAPI Community** - Excellent documentation
- **Streamlit** - Rapid prototyping

---

**⭐ If you find this project useful, please consider giving it a star!**

---

**Version:** 1.0  
**Last Updated:** 2026-06-03  
**Status:** ✅ Production Ready
