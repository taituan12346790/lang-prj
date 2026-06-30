# 🎓 Hệ Thống Học Tiếng Anh Thông Minh với Multi-Agent AI

Hệ thống học tiếng Anh tích hợp AI Multi-Agent, sử dụng LangGraph để cung cấp trải nghiệm học tập cá nhân hóa với các tính năng: học từ vựng theo chủ đề, luyện ngữ pháp, viết luận, và trò chuyện với AI Tutor thông minh.

## 🌟 Tính Năng Chính

### 1. **Multi-Agent AI System**
- **Grammar Agent**: Phân tích và giải thích ngữ pháp chi tiết
- **Exercise Agent**: Tạo bài tập tùy chỉnh theo trình độ
- **Translator Agent**: Dịch và giải thích ngữ cảnh
- **AI Tutor**: Trò chuyện thông minh, hỗ trợ học tập cá nhân hóa

### 2. **Học Theo Chủ Đề (Learning Path)**
- 25+ chủ đề đa dạng từ cơ bản đến nâng cao
- Mỗi chủ đề có 5 bài học với quiz tương tác
- Hệ thống theo dõi tiến độ chi tiết

### 3. **Luyện Viết (Writing Practice)**
- Các chủ đề viết luận đa dạng
- AI phân tích và chấm điểm tự động
- Góp ý chi tiết về ngữ pháp, từ vựng, cấu trúc

### 4. **AI Chat & Learning Activities**
- Trò chuyện tự nhiên với AI Tutor
- Tích hợp bài tập trong cuộc hội thoại
- Ghi nhớ ngữ cảnh và tiến độ học tập

### 5. **Analytics & Progress Tracking**
- Dashboard theo dõi tiến độ
- Thống kê chi tiết điểm số, thời gian học
- Phân tích điểm mạnh/yếu

## 🏗️ Kiến Trúc Hệ Thống

```
├── Backend (FastAPI)
│   ├── Multi-Agent AI (LangGraph)
│   ├── PostgreSQL Database
│   └── RESTful API
│
├── Frontend (Streamlit)
│   ├── Learning Dashboard
│   ├── AI Chat Interface
│   └── Analytics Dashboard
│
└── AI Integration
    ├── Groq (Llama 3.1)
    └── LangChain/LangGraph
```

## 🚀 Cài Đặt & Chạy

### Yêu Cầu Hệ Thống
- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ (optional - cho Next.js frontend)

### Bước 1: Clone Repository

```bash
git clone https://github.com/taituan12346790/lang-prj.git
cd lang-prj
```

### Bước 2: Cài Đặt Python Environment

```bash
# Tạo virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 3: Cấu Hình Database

```bash
# Tạo database PostgreSQL
createdb lang_learning_db

# Chạy migrations
alembic upgrade head

# Seed dữ liệu mẫu
python seed_database.py
```

### Bước 4: Cấu Hình Environment Variables

Tạo file `.env` từ `.env.example`:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/lang_learning_db

# API Keys
GROQ_API_KEY=your_groq_api_key_here

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret

# JWT Secret
SECRET_KEY=your_secret_key_here

# Backend URL
BACKEND_URL=http://localhost:8000
```

### Bước 5: Chạy Backend

```bash
# Development mode
uvicorn app.main:app --reload --port 8000

# hoặc
python -m uvicorn app.main:app --reload
```

Backend sẽ chạy tại: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Bước 6: Chạy Frontend (Streamlit)

Mở terminal mới:

```bash
# Activate virtual environment
venv\Scripts\activate

# Chạy Streamlit
streamlit run streamlit_app.py
```

Frontend sẽ chạy tại: `http://localhost:8501`

## 📦 Cấu Trúc Thư Mục

```
lang-prj/
├── app/                          # Backend FastAPI
│   ├── agents/                   # Multi-Agent AI
│   │   ├── grammar_agent.py
│   │   ├── exercise_agent.py
│   │   └── translator_agent.py
│   ├── core/                     # Core logic
│   │   ├── pipeline.py           # LangGraph pipeline
│   │   ├── router.py             # Agent routing
│   │   └── intent_classifier.py
│   ├── models/                   # SQLAlchemy models
│   ├── routers/                  # API endpoints
│   ├── services/                 # Business logic
│   └── schemas/                  # Pydantic schemas
│
├── alembic/                      # Database migrations
│   └── versions/
│
├── streamlit_app.py              # Frontend Streamlit
├── requirements.txt              # Python dependencies
├── alembic.ini                   # Alembic config
└── .env                          # Environment variables
```

## 🔑 API Endpoints Chính

### Authentication
- `POST /api/auth/register` - Đăng ký tài khoản
- `POST /api/auth/login` - Đăng nhập
- `POST /api/auth/google` - Đăng nhập Google OAuth

### Learning Path
- `GET /api/learning-path/topics` - Danh sách chủ đề
- `GET /api/learning-path/topics/{topic_id}` - Chi tiết chủ đề
- `POST /api/learning-path/lessons/{lesson_id}/complete` - Hoàn thành bài học

### AI Chat
- `POST /api/chat/send` - Gửi tin nhắn đến AI
- `GET /api/chat/history` - Lịch sử chat
- `POST /api/chat/clear` - Xóa lịch sử

### Quiz
- `POST /api/quiz/generate` - Tạo quiz từ bài học
- `POST /api/quiz/submit` - Nộp bài quiz
- `GET /api/quiz/results` - Xem kết quả

### Writing
- `POST /api/writing/submit` - Nộp bài viết
- `POST /api/writing/evaluate` - Đánh giá bài viết
- `GET /api/writing/history` - Lịch sử bài viết

### Analytics
- `GET /api/analytics/progress` - Tiến độ học tập
- `GET /api/analytics/quiz-stats` - Thống kê quiz
- `GET /api/analytics/writing-stats` - Thống kê writing

## 🧪 Testing

```bash
# Chạy tests
pytest

# Test với coverage
pytest --cov=app tests/

# Test API endpoint cụ thể
python test_api.py
```

## 📊 Database Schema

Hệ thống sử dụng PostgreSQL với các bảng chính:

- `users` - Thông tin người dùng
- `topics` - Chủ đề học tập
- `lessons` - Bài học
- `quiz_results` - Kết quả quiz
- `conversations` - Lịch sử chat
- `user_writings` - Bài viết của người dùng
- `learning_sessions` - Phiên học
- `chat_learning_activities` - Hoạt động học trong chat

## 🔧 Công Nghệ Sử Dụng

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **PostgreSQL** - Database
- **Pydantic** - Data validation

### AI/ML
- **LangGraph** - Multi-agent orchestration
- **LangChain** - LLM framework
- **Groq** - LLM API (Llama 3.1)

### Frontend
- **Streamlit** - Web UI framework
- **Plotly** - Interactive charts
- **Pandas** - Data manipulation

### Authentication
- **JWT** - Token-based auth
- **Google OAuth 2.0** - Social login
- **Passlib** - Password hashing

## 🌐 Deployment

### Render.com (Recommended)

1. **Backend Deployment**:
   - Connect GitHub repository
   - Environment: Python 3.10
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Database**:
   - Create PostgreSQL instance on Render
   - Update `DATABASE_URL` in environment variables

3. **Frontend Deployment**:
   - Create new Streamlit deployment
   - Connect same GitHub repository
   - Update `BACKEND_URL` to point to backend service

### Docker (Alternative)

```bash
# Build and run với Docker Compose
docker-compose up -d

# Chạy migrations
docker-compose exec backend alembic upgrade head

# Seed database
docker-compose exec backend python seed_database.py
```

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `GROQ_API_KEY` | Groq API key cho LLM | ✅ |
| `SECRET_KEY` | JWT secret key | ✅ |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | ⚠️ |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | ⚠️ |
| `BACKEND_URL` | Backend API URL | ✅ |

⚠️ = Optional nhưng khuyến nghị cho production

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Author

**Nguyễn Tài Tuấn**
- GitHub: [@taituan12346790](https://github.com/taituan12346790)
- Email: tuan.nt204690@sis.hust.edu.vn

## 🙏 Acknowledgments

- LangChain & LangGraph for multi-agent framework
- Groq for fast LLM inference
- HUST for academic support

## 📞 Support

Nếu bạn gặp vấn đề hoặc có câu hỏi:
- Mở [GitHub Issue](https://github.com/taituan12346790/lang-prj/issues)
- Email: tuan.nt204690@sis.hust.edu.vn

---

**⭐ Nếu project này hữu ích, hãy star trên GitHub!**
