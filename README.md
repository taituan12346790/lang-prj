# 🎓 AI-Powered English Learning Platform

Hệ thống học tiếng Anh thông minh sử dụng Multi-Agent AI và LangGraph, cung cấp trải nghiệm học tập cá nhân hóa toàn diện: học từ vựng theo chủ đề, luyện ngữ pháp, viết luận, và trò chuyện với AI Tutor.

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
Backend (FastAPI)
├── Multi-Agent AI (LangGraph)
│   ├── Grammar Agent
│   ├── Exercise Agent
│   └── Translator Agent
├── PostgreSQL Database
└── RESTful API

Frontend (Streamlit)
├── Learning Dashboard
├── AI Chat Interface
├── Writing Practice
└── Analytics Dashboard

AI/LLM
├── Groq API (Llama 3.1)
├── LangChain/LangGraph
└── Multi-Agent Orchestration
```

## 🚀 Cài Đặt & Chạy

### Yêu Cầu Hệ Thống
- Python 3.10+
- PostgreSQL 14+
- Git

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

### Bước 3: Cấu Hình Database PostgreSQL

**Option 1: PostgreSQL Local**
```bash
# Tạo database
createdb lang_learning_db

# Hoặc dùng psql
psql -U postgres
CREATE DATABASE lang_learning_db;
```

**Option 2: Neon.tech (Cloud PostgreSQL - Khuyến nghị)**
1. Đăng ký tại https://neon.tech (miễn phí)
2. Tạo project mới
3. Copy connection string
4. Paste vào `.env` file

```bash
# Chạy migrations
alembic upgrade head

# Seed dữ liệu mẫu (25 topics + lessons)
python -c "from app.data.topics_data import TOPICS; print(f'Loaded {len(TOPICS)} topics')"
```

### Bước 4: Cấu Hình Environment Variables

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Cập nhật các giá trị sau:

```env
# Database (Neon.tech hoặc local PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/lang_learning_db

# Groq API (https://console.groq.com - Free tier: 30 requests/min)
GROQ_API_KEY=gsk_your_api_key_here

# JWT Secret (generate random string)
SECRET_KEY=your-secret-key-minimum-32-characters

# Google OAuth (Optional - để enable Google login)
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret

# URLs
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8501
```

**Lấy Groq API Key:**
1. Truy cập https://console.groq.com/
2. Đăng ký/Đăng nhập
3. Tạo API key mới
4. Free tier: 30 requests/phút (đủ cho development)

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

## 🔧 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM cho database
- **Alembic** - Database migrations
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation

### AI/ML
- **LangGraph** - Multi-agent orchestration framework
- **LangChain** - LLM integration framework
- **Groq** - Fast LLM API (Llama 3.1 70B)
- **OpenAI-compatible API** - Flexible LLM integration

### Frontend
- **Streamlit** - Interactive web UI
- **Plotly** - Data visualization
- **Pandas** - Data analysis

### Authentication
- **JWT** - Stateless authentication
- **Google OAuth 2.0** - Social login
- **Passlib + bcrypt** - Secure password hashing

## 🌐 Deployment

### Render.com (Recommended - Free tier available)

**1. Backend Deployment:**
- Create new Web Service
- Connect GitHub repository
- Environment: Python 3.10
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**2. Database:**
- Create PostgreSQL instance on Render (hoặc dùng Neon.tech)
- Copy `Internal Database URL`
- Add to backend environment variables

**3. Frontend Deployment:**
- Create new Web Service
- Connect GitHub repository  
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
- Environment Variable: `BACKEND_URL=<your-backend-url>`

**4. Environment Variables trên Render:**
```
DATABASE_URL=<from-render-postgres>
GROQ_API_KEY=<your-groq-key>
SECRET_KEY=<random-32-chars>
FRONTEND_URL=<your-frontend-url>
BACKEND_URL=<your-backend-url>
```

### Docker (Alternative)

```bash
# Build và run với Docker Compose
docker-compose up -d

# Chạy migrations
docker-compose exec backend alembic upgrade head
```

### Heroku

```bash
# Login và tạo app
heroku login
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku master

# Chạy migrations
heroku run alembic upgrade head
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

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/TinhNangMoi`)
3. Commit changes (`git commit -m 'Thêm tính năng XYZ'`)
4. Push to branch (`git push origin feature/TinhNangMoi`)
5. Tạo Pull Request

## 📄 License

Dự án này được phát triển cho mục đích học tập và nghiên cứu.

## 👥 Author

**Nguyễn Tài Tuấn**
- GitHub: [@taituan12346790](https://github.com/taituan12346790)
- Email: tuan.nt204690@sis.hust.edu.vn
- University: Hanoi University of Science and Technology (HUST)

## 🙏 Acknowledgments

- **LangChain & LangGraph** - Multi-agent AI framework
- **Groq** - Ultra-fast LLM inference
- **Streamlit** - Rapid UI development
- **HUST** - Academic support and guidance

---

## 📞 Support & Contact

Nếu bạn gặp vấn đề hoặc có câu hỏi:
- 🐛 [Tạo Issue trên GitHub](https://github.com/taituan12346790/lang-prj/issues)
- 📧 Email: tuan.nt204690@sis.hust.edu.vn

---

⭐ **Nếu project hữu ích, hãy cho một star trên GitHub!** ⭐
