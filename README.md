# 🎓 AI Language Tutor - Vietnamese AI Learning Platform

AI-powered language learning platform with personalized tutoring, adaptive exercises, and context-aware feedback.

## 🌟 Features

- 🤖 **AI Tutor** - Multi-agent system with specialized agents
- 📚 **20 A1 Topics** - Complete beginner English curriculum
- ✍️ **Writing Assessment** - Automated essay evaluation with detailed feedback
- 📊 **Analytics Dashboard** - Track progress and learning patterns
- 🎯 **Adaptive Learning** - Personalized content based on CEFR levels
- 💬 **Interactive Chat** - Real-time conversation with AI tutor

## 🏗️ Architecture

### Backend (FastAPI)
- Multi-agent orchestration with LangGraph
- Context-aware AI responses
- PostgreSQL database with SQLAlchemy
- JWT authentication + Google OAuth

### Frontend (Streamlit)
- Interactive learning interface
- Real-time chat with AI
- Progress tracking and analytics

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database (Neon.tech recommended)
- Groq API key

### Local Development

1. **Clone repository**
```bash
git clone <your-repo-url>
cd lang_prj
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Run migrations**
```bash
alembic upgrade head
```

5. **Start backend**
```bash
uvicorn app.main:app --reload
```

6. **Start frontend** (new terminal)
```bash
streamlit run streamlit_app.py
```

## 🌐 Deployment

### Render (Backend) + Streamlit Cloud (Frontend)

See detailed guide: `DEPLOY_CHECKLIST_RENDER.md`

**Quick steps:**
1. Setup Neon.tech database (free forever)
2. Deploy backend to Render
3. Deploy frontend to Streamlit Cloud
4. Run database migrations

## 📦 Project Structure

```
lang_prj/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Core functionality (agents, pipeline)
│   ├── data/         # Topics data
│   ├── llm/          # LLM client & prompts
│   ├── memory/       # Memory management
│   ├── models/       # Database models
│   ├── routers/      # API routers
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── tools/        # AI tools
├── alembic/          # Database migrations
├── streamlit_app.py  # Frontend application
├── requirements.txt  # Backend dependencies
└── requirements-frontend.txt  # Frontend dependencies
```

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM
- LangChain - LLM framework
- LangGraph - Agent orchestration
- Groq API - LLM provider

**Frontend:**
- Streamlit - Interactive web apps

**Database:**
- PostgreSQL - Production database
- Alembic - Migrations

## 📝 Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host/dbname

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM
GROQ_API_KEY=your-groq-api-key

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
```

## 🤝 Contributing

This is an academic project for thesis purposes.

## 📄 License

Private - Academic Project

## 👨‍💻 Author

Vietnamese Language Learning Thesis Project
