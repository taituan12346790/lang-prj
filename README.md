# 🎓 AI English Learning Platform

Hệ thống học tiếng Anh với Multi-Agent AI (LangGraph + Groq Llama 3.1)

## Tính năng

- 🤖 Multi-Agent AI: Grammar, Exercise, Translator agents
- 📚 25+ chủ đề học tập với quiz tương tác
- ✍️ Luyện viết với phản hồi AI tự động
- 💬 Chat với AI Tutor thông minh
- 📊 Theo dõi tiến độ học tập

## Cài đặt

### Yêu cầu
- Python 3.10+
- PostgreSQL hoặc Neon.tech (cloud)

### Các bước

1. Clone repo:
```bash
git clone https://github.com/taituan12346790/lang-prj.git
cd lang-prj
```

2. Cài dependencies:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Tạo file `.env`:
```env
DATABASE_URL=postgresql://user:password@host/db
GROQ_API_KEY=your_groq_key  # Lấy tại https://console.groq.com
SECRET_KEY=your_secret_key
```

4. Chạy migrations:
```bash
alembic upgrade head
```

5. Chạy ứng dụng:
```bash
# Backend
uvicorn app.main:app --reload

# Frontend (terminal mới)
streamlit run streamlit_app.py
```

Backend: http://localhost:8000  
Frontend: http://localhost:8501

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, PostgreSQL, Alembic  
**AI/ML:** LangGraph, LangChain, Groq (Llama 3.1)  
**Frontend:** Streamlit, Plotly  
**Auth:** JWT, Google OAuth 2.0

## Contact

GitHub: [@taituan12346790](https://github.com/taituan12346790)
