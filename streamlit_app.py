"""
AI Language Tutor – Learning Path Edition
==========================================
Backend : python -m uvicorn app.main:app --reload
Frontend: streamlit run streamlit_app.py
"""
from __future__ import annotations

import html
import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import httpx
import streamlit as st

# Hide Streamlit default footer and menu
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Setup logger
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════
DEFAULT_API_BASE = os.getenv("API_BASE_URL", "https://ai-language-tutor-api-brqu.onrender.com")
CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
LEVEL_COLORS = {
    "A1": "#6ee7b7", "A2": "#34d399",
    "B1": "#60a5fa", "B2": "#3b82f6",
    "C1": "#c084fc", "C2": "#a855f7",
}
LESSON_ICONS = {
    "grammar": "",
    "vocabulary": "",
    "practice": "",
    "writing": "",
    "quiz": "",
    # Vietnamese aliases
    "ngữ pháp": "",
    "từ vựng": "",
    "thực hành": "",
    "viết": "",
    "kiểm tra": "",
}

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════
def _init() -> None:
    defaults = {
        "access_token": None,
        "user": None,
        "profile": None,
        "api_base": DEFAULT_API_BASE,
        "page": "auth",          # auth / placement / dashboard / topic / lesson / quiz / quiz_result / chat / levelup
        "messages": [],
        "current_session_id": None,
        # learning path state
        "current_topic": None,   # full topic dict
        "current_lesson": None,  # full lesson dict
        "quiz_questions": None,
        "quiz_answers": {},
        "quiz_result": None,
        "topic_list": None,      # cached topic list
        "dashboard": None,       # cached dashboard data
        # test state
        "placement_questions": [],
        "levelup_questions": [],
        "test_answers": {},
        # UI state
        "confirm_logout": False,
        "show_debug_info": False,  # Set to True to show debug info in sidebar
        "is_logging_out": False,  # Flag to prevent profile fetch during logout
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ═══════════════════════════════════════════════════════════════
# HTTP HELPERS
# ═══════════════════════════════════════════════════════════════
def _headers() -> dict:
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    tok = st.session_state.get("access_token")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def _url(path: str) -> str:
    return f"{st.session_state.api_base.rstrip('/')}{path}"


def _err(r: httpx.Response) -> str:
    try:
        d = r.json()
        return d.get("error") or d.get("detail") or r.text
    except Exception:
        return r.text or f"HTTP {r.status_code}"


def _get(path: str, **kw) -> tuple[bool, Any, str]:
    try:
        with httpx.Client(timeout=20) as c:
            r = c.get(_url(path), headers=_headers(), **kw)
        if r.status_code == 200:
            return True, r.json(), ""
        if r.status_code == 401:
            _logout()
        return False, None, _err(r)
    except Exception as e:
        return False, None, str(e)


def _post(path: str, body: dict, timeout: int = 30) -> tuple[bool, Any, str]:
    try:
        with httpx.Client(timeout=timeout) as c:
            r = c.post(_url(path), json=body, headers=_headers())
        if r.status_code in (200, 201):
            return True, r.json(), ""
        if r.status_code == 401:
            _logout()
        return False, None, _err(r)
    except Exception as e:
        return False, None, str(e)


# ═══════════════════════════════════════════════════════════════
# AUTH API
# ═══════════════════════════════════════════════════════════════
def api_login(email: str, pw: str) -> tuple[bool, str]:
    ok, data, err = _post("/api/auth/login", {"email": email.strip().lower(), "password": pw})
    if ok:
        st.session_state.access_token = data["access_token"]
        st.session_state.user = data.get("user", {})
        _fetch_profile()
        return True, f"Chào mừng, {data.get('user', {}).get('full_name', '')}!"
    return False, err


def api_register(email, pw, name, native, target) -> tuple[bool, str]:
    ok, _, err = _post("/api/auth/register", {
        "email": email.strip().lower(), "password": pw,
        "full_name": name.strip(), "native_language": native, "target_language": target,
    })
    return ok, err


def _fetch_profile() -> None:
    """Fetch user profile and populate session state"""
    # Skip fetch if logging out
    if st.session_state.get("is_logging_out"):
        return
    
    ok, data, err = _get("/api/profile/")
    if ok and data:
        st.session_state.profile = data
        # Also set user object from profile data
        st.session_state.user = {
            "full_name": data.get("full_name", "User"),
            "email": data.get("email", ""),
            "id": data.get("user_id")
        }
        # Debug
        print(f"Profile loaded: {data.get('email')}, user_id={data.get('user_id')}")
    else:
        st.session_state.profile = None
        st.session_state.user = None
        print(f"Failed to fetch profile: {err}")


def _logout():
    """Clear all session state and return to auth page"""
    # Clear all major session keys
    keys_to_clear = [
        "access_token", "user", "profile", "messages", "current_session_id",
        "current_topic", "current_lesson", "quiz_questions", "quiz_answers",
        "quiz_result", "topic_list", "dashboard", "confirm_logout", 
        "is_logging_out", "analytics_context", "analytics_data"
    ]
    for k in keys_to_clear:
        if k in st.session_state:
            st.session_state[k] = None
    
    st.session_state.page = "auth"
    st.session_state.just_logged_out = True  # Prevent auto re-login
    
    # CRITICAL: Clear Google OAuth token from URL to prevent auto re-login
    st.query_params.clear()
    
    st.rerun()  # Force immediate redirect


def current_level() -> str:
    p = st.session_state.get("profile") or {}
    return p.get("current_level", "A1")


# ═══════════════════════════════════════════════════════════════
# LEARNING PATH API
# ═══════════════════════════════════════════════════════════════
def api_dashboard() -> Optional[dict]:
    ok, data, err = _get("/api/learning/dashboard")
    if ok:
        st.session_state.dashboard = data
        return data
    st.error(f"Không tải được dashboard: {err}")
    return None


def api_topics(level: str) -> list:
    ok, data, err = _get(f"/api/learning/topics/{level}")
    if ok:
        st.session_state.topic_list = data
        return data
    st.error(f"Lỗi tải danh sách chủ đề: {err}")
    return []


def api_topic_detail(topic_id: str) -> Optional[dict]:
    ok, data, _ = _get(f"/api/learning/topic/{topic_id}")
    return data if ok else None


def api_get_learning_context() -> Optional[dict]:
    """Get user's current learning context (active topic/lesson) from backend"""
    ok, data, _ = _get("/api/learning/context")
    return data if ok else None


def api_activate_context(topic_id: str, lesson_order: int = None, mode: str = "topic") -> bool:
    """Activate learning context in backend"""
    payload = {"topic_id": topic_id}
    if lesson_order:
        payload["lesson_order"] = lesson_order
    if mode:
        payload["mode"] = mode
    
    ok, data, err = _post("/api/learning/activate-context", payload)
    if ok:
        return True
    else:
        st.warning(f"Could not activate context: {err}")
        return False


def api_execute_action(action_type: str, params: dict = None) -> Optional[dict]:
    """Phase 3: Execute an action suggested by Agent"""
    payload = {
        "action_type": action_type,
        "params": params or {}
    }
    ok, data, err = _post("/api/learning/execute-action", payload)
    if ok:
        return data
    else:
        st.error(f"Không thực hiện được: {err}")
        return None


def api_lesson(lesson_id: str) -> Optional[dict]:
    ok, data, _ = _get(f"/api/learning/lesson/{lesson_id}")
    return data if ok else None


def api_submit_writing(lesson_id: str, topic_id: str, prompt: str, user_text: str, word_count: int) -> tuple[bool, Optional[dict], Optional[str]]:
    """Submit writing for AI review"""
    payload = {
        "lesson_id": lesson_id,
        "topic_id": topic_id,
        "prompt": prompt,
        "user_text": user_text,
        "word_count": word_count
    }
    ok, data, err = _post("/api/writing/submit", payload)
    return ok, data, err


def api_writing_history(lesson_id: str = None, limit: int = 10) -> list:
    """Get writing history"""
    params = {"limit": limit}
    if lesson_id:
        params["lesson_id"] = lesson_id
    ok, data, _ = _get("/api/writing/history", params=params)
    return data if ok else []


def api_get_pending_exercise(session_id: str) -> Optional[dict]:
    """Get pending exercise for current session"""
    ok, data, _ = _get(f"/api/ai-exercise/pending?session_id={session_id}")
    return data if ok else None


def api_complete_lesson(topic_id: str, lesson_order: int) -> bool:
    ok, _, err = _post(
        f"/api/learning/topic/{topic_id}/lesson/{lesson_order}/complete", {}
    )
    if not ok:
        st.warning(f"Không lưu tiến độ: {err}")
    return ok


def api_quiz_questions(topic_id: str) -> Optional[dict]:
    ok, data, err = _get(f"/api/quiz/topic/{topic_id}/questions")
    return data if ok else None


def api_submit_quiz(topic_id: str, answers: dict) -> Optional[dict]:
    ok, data, err = _post(f"/api/quiz/topic/{topic_id}/submit", {"answers": answers})
    if not ok:
        st.error(f"Lỗi nộp quiz: {err}")
    return data if ok else None


def api_get_placement_q() -> list:
    ok, data, _ = _get("/api/test/placement/questions")
    return data.get("questions", []) if ok else []


def api_submit_placement(answers: dict) -> Optional[dict]:
    ok, data, err = _post("/api/test/placement", {"answers": answers})
    return data if ok else None


def api_level_questions(level: str) -> list:
    ok, data, _ = _get(f"/api/test/level/{level}/questions")
    return data.get("questions", []) if ok else []


def api_submit_levelup(level: str, answers: dict) -> Optional[dict]:
    ok, data, err = _post("/api/test/level-up", {
        "test_type": "grammar", "current_level": level,
        "num_questions": len(answers), "answers": answers,
    })
    return data if ok else None


def api_chat(
    msg: str, 
    session_id: Optional[str] = None,
    quiz_wrong_answers: Optional[list] = None,
    quiz_topic_id: Optional[str] = None
) -> tuple[bool, str, dict]:
    """A4/A5: Send chat with session_id for conversation tracking + A3: Quiz review"""
    payload = {
        "user_input": msg, 
        "explain_in": "vi", 
        "temperature": 0.7
    }
    if session_id:
        payload["session_id"] = session_id
    if quiz_wrong_answers:
        payload["quiz_wrong_answers"] = quiz_wrong_answers
    if quiz_topic_id:
        payload["quiz_topic_id"] = quiz_topic_id
    
    ok, data, err = _post("/api/chat/", payload, timeout=120)
    if ok:
        return True, data.get("response", ""), data.get("metadata", {})
    return False, err, {}


def api_chat_save_message(
    session_id: str,
    role: str,
    message: str,
    model_used: str = "gpt-4",
    tokens: int = 0
) -> Optional[dict]:
    """Save chat message to database"""
    ok, data, err = _post("/api/chat/save-message", {
        "session_id": session_id,
        "role": role,
        "message": message,
        "model_used": model_used,
        "tokens": tokens
    })
    if ok:
        return data
    return None


def api_chat_get_history(session_id: str, limit: int = 100) -> Optional[list]:
    """Get chat history from database"""
    ok, data, err = _get(f"/api/chat/history/{session_id}?limit={limit}")
    if ok:
        return data.get("messages", []) if data else []
    return []


def api_chat_get_sessions(limit: int = 50) -> Optional[list]:
    """Get all chat sessions"""
    ok, data, err = _get(f"/api/chat/sessions?limit={limit}")
    if ok:
        return data.get("sessions", []) if data else []
    return []


def api_chat_analyze_error(
    question: str,
    user_answer: str,
    correct_answer: str,
    skill_tag: str = None,
    lesson_id: str = None,
    topic_id: str = None
) -> Optional[dict]:
    """Call error analysis API"""
    ok, data, err = _post("/api/learning/analyze-error", {
        "question": question,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "skill_tag": skill_tag,
        "lesson_id": lesson_id,
        "topic_id": topic_id
    }, timeout=30)
    if ok:
        return data
    st.error(f"Lỗi phân tích: {err}")
    return None


# Alias for backward compatibility
api_analyze_error = api_chat_analyze_error


# ═══════════════════════════════════════════════════════════════
# ANALYTICS API
# ═══════════════════════════════════════════════════════════════
def api_analytics_dashboard() -> Optional[dict]:
    """Lấy analytics tổng quan"""
    ok, data, err = _get("/api/analytics/dashboard")
    if not ok:
        st.error(f"Không tải được analytics: {err}")
        return None
    return data


def api_analytics_skills() -> Optional[dict]:
    """Lấy phân tích theo skill"""
    ok, data, err = _get("/api/analytics/skills")
    return data if ok else None


def api_analytics_reviews() -> list:
    """Lấy topics cần ôn tập"""
    ok, data, err = _get("/api/analytics/reviews")
    return data if ok else []


def api_analytics_timeline(days: int = 30) -> list:
    """Lấy timeline học tập"""
    ok, data, err = _get(f"/api/analytics/timeline?days={days}")
    return data if ok else []


def api_chat_activities(days: int = 30, activity_type: Optional[str] = None) -> Optional[dict]:
    """Lấy hoạt động học từ AI Tutor chat"""
    params = f"days={days}"
    if activity_type:
        params += f"&activity_type={activity_type}"
    ok, data, err = _get(f"/api/analytics/chat-activities?{params}")
    return data if ok else None


# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════
def _inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp span:not(.material-icons):not([data-testid="stIconMaterial"]),
.stApp div:not([data-testid="stIconMaterial"]) {
    font-family: 'Inter', sans-serif;
}
/* Keep Material Icons readable in expanders/buttons (avoid "arr" garbled text) */
.material-icons,
[data-testid="stIconMaterial"] {
    font-family: 'Material Icons' !important;
    font-style: normal !important;
    font-weight: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
}
[data-testid="stExpander"] summary [data-testid="stIconMaterial"] {
    font-size: 1.25rem !important;
    margin-right: 0.35rem !important;
}

/* Main background */
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); padding-top: 0px !important; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; max-width: 1200px; }

/* Show sidebar - P2: Enable chat history sidebar */
[data-testid="stSidebar"] { 
    background: rgba(15,12,41,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="collapsedControl"] { display: none !important; }

/* Hide sidebar on auth page - clean look for login/register */
body[data-page="auth"] [data-testid="stSidebar"],
body[data-page="auth"] [data-testid="collapsedControl"] {
    display: none !important;
}

/* Profile popover trigger: hide only Material chevron, keep username visible */
[data-testid="stPopover"] button .material-icons,
[data-testid="stPopover"] button [data-testid="stIconMaterial"] {
    display: none !important;
}

/* ═══════════════════════════════════════════════════════════ */
/* TOP NAVIGATION BAR */
/* ═══════════════════════════════════════════════════════════ */
.top-nav {
    background: rgba(15, 12, 41, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    margin: -1rem -1rem 1rem -1rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.nav-logo {
    font-size: 1.3rem;
    font-weight: 700;
    color: #6ee7b7;
    display: flex;
    align-items: center;
    gap: 8px;
}

.nav-user {
    display: flex;
    align-items: center;
    gap: 12px;
}

.nav-user-badge {
    padding: 6px 14px;
    background: rgba(110, 231, 183, 0.15);
    border: 1px solid rgba(110, 231, 183, 0.3);
    border-radius: 20px;
    color: #6ee7b7;
    font-size: 0.85rem;
    font-weight: 600;
}

/* Breadcrumb */
.breadcrumb {
    padding: 0.75rem 0;
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.5);
    margin-bottom: 1rem;
}

.breadcrumb a {
    color: rgba(255, 255, 255, 0.6);
    text-decoration: none;
    transition: color 0.2s;
}

.breadcrumb a:hover {
    color: rgba(255, 255, 255, 0.9);
}

.breadcrumb span {
    margin: 0 8px;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .top-nav {
        padding: 0 1rem;
    }
    .nav-logo {
        font-size: 1.1rem;
    }
    .nav-links {
        gap: 0.25rem;
    }
    .nav-link {
        padding: 6px 10px;
        font-size: 0.85rem;
    }
}

/* Card component */
.lp-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
    transition: transform .2s, box-shadow .2s;
    color: rgba(255,255,255,0.92);
}
.lp-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

/* Topic card states */
.topic-completed { border-left: 4px solid #34d399 !important; }
.topic-inprogress { border-left: 4px solid #60a5fa !important; }
.topic-locked     { border-left: 4px solid rgba(255,255,255,0.2) !important; opacity: 0.6; }

/* Progress bar */
.prog-bar-bg {
    background: rgba(255,255,255,0.1);
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
    margin: 8px 0;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6ee7b7, #3b82f6);
    transition: width 0.5s ease;
}

/* Level badge */
.level-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 1px;
}

/* Quiz option buttons */
.quiz-option {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
    text-align: left !important;
    padding: 10px 16px !important;
    margin: 4px 0 !important;
    width: 100% !important;
    cursor: pointer;
    transition: all .15s;
}
.quiz-option:hover {
    background: rgba(99,102,241,0.3) !important;
    border-color: #6366f1 !important;
}
.quiz-correct { background: rgba(52,211,153,0.25) !important; border-color: #34d399 !important; }
.quiz-wrong   { background: rgba(248,113,113,0.25) !important; border-color: #f87171 !important; }

/* Stat box */
.stat-box {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-number { font-size: 2rem; font-weight: 700; color: #6ee7b7; }
.stat-label  { font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-top: 2px; }

/* Lesson step */
.lesson-step {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    border-radius: 12px;
    margin: 6px 0;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.92);
    cursor: pointer;
    transition: all .2s;
}
.lesson-step:hover { background: rgba(255,255,255,0.1); transform: translateX(4px); }
.lesson-step.done  { border-color: #34d399; background: rgba(52,211,153,0.08); }
.lesson-step.active { border-color: #60a5fa; background: rgba(96,165,250,0.12); }

/* White text on dark main area — avoid bare `div` (breaks expander/info blocks) */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5,
.main p, .main label,
[data-testid="stMarkdownContainer"] p {
    color: rgba(255,255,255,0.92) !important;
}
.stMarkdown p { color: rgba(255,255,255,0.85) !important; }

/* Input fields - DARKER TEXT FOR BETTER READABILITY */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(255,255,255,0.95) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;  /* Dark text for inputs */
    font-weight: 500 !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: rgba(0,0,0,0.4) !important;  /* Dark placeholder */
}
.stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.3) !important;
    background: rgba(255,255,255,1) !important;
}

/* Input labels - keep white for dark background */
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: rgba(255,255,255,0.95) !important;
    font-weight: 500 !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all .2s !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
}
.stButton button[kind="secondary"] {
    background: rgba(255,255,255,0.1) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] .stButton button {
    width: 100% !important;
    text-align: left !important;
    padding: 10px 16px !important;
    margin: 4px 0 !important;
}
[data-testid="stSidebar"] h3 {
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
    font-size: 1.1rem !important;
}

/* Radio - DARK TEXT FOR QUIZ ANSWERS - ULTRA STRONG OVERRIDE */
.stRadio label { color: rgba(255,255,255,0.95) !important; font-weight: 500 !important; }
.stRadio [data-testid="stWidgetLabel"] { color: white !important; font-weight: 600 !important; }

/* Main radio button container with white background and dark text */
.stRadio div[role="radiogroup"] > label {
    background: rgba(255,255,255,0.95) !important;
    color: #1a1a1a !important;
    padding: 10px 16px !important;
    border-radius: 8px !important;
    margin: 6px 0 !important;
    font-weight: 500 !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
}

/* Force dark text on ALL nested elements */
.stRadio div[role="radiogroup"] > label * {
    color: #1a1a1a !important;  /* Apply to ALL children */
}
.stRadio div[role="radiogroup"] > label > div {
    color: #1a1a1a !important;
}
.stRadio div[role="radiogroup"] > label span {
    color: #1a1a1a !important;
}
.stRadio div[role="radiogroup"] > label p {
    color: #1a1a1a !important;
}

/* Also override for radio input text */
.stRadio div[role="radiogroup"] label[data-baseweb="radio"] {
    background: rgba(255,255,255,0.95) !important;
}
.stRadio div[role="radiogroup"] label[data-baseweb="radio"] > div:last-child {
    color: #1a1a1a !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.1) !important; }

/* Chat messages — light text on dark bubble (incl. tables from AI markdown) */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h4,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ol,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ul,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code {
    color: rgba(255,255,255,0.92) !important;
}
[data-testid="stChatMessage"] table {
    background: rgba(255,255,255,0.06) !important;
    border-collapse: collapse !important;
    width: 100% !important;
    margin: 0.5rem 0 !important;
}
[data-testid="stChatMessage"] th,
[data-testid="stChatMessage"] td {
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: rgba(255,255,255,0.9) !important;
    padding: 8px 12px !important;
    background: rgba(255,255,255,0.04) !important;
}
[data-testid="stChatMessage"] th {
    background: rgba(99,102,241,0.35) !important;
    font-weight: 600 !important;
}
[data-testid="stChatMessage"] tr:nth-child(even) td {
    background: rgba(255,255,255,0.07) !important;
}
[data-testid="stChatMessageContent"] {
    color: rgba(255,255,255,0.92) !important;
}
[data-testid="stChatMessageContent"] *:not(button):not(button *) {
    color: rgba(255,255,255,0.9) !important;
}

/* Chat input bar at bottom */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stChatInput"] {
    background: rgba(15, 12, 41, 0.98) !important;
    border-top: 1px solid rgba(255,255,255,0.1) !important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
    background: #ffffff !important;
    color: #1a1a1a !important;
    border: 1px solid rgba(0,0,0,0.15) !important;
    border-radius: 12px !important;
    -webkit-text-fill-color: #1a1a1a !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(0,0,0,0.4) !important;
    -webkit-text-fill-color: rgba(0,0,0,0.4) !important;
}

/* Select box - closed state: dark text on white field */
.stSelectbox [data-baseweb="select"],
.stSelectbox [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] div,
.stSelectbox select {
    background: rgba(255,255,255,0.95) !important;
    color: #1a1a1a !important;
    font-weight: 500 !important;
}
.stSelectbox [data-baseweb="select"] * {
    color: #1a1a1a !important;
}

/* Select box dropdown menu (portal outside widget - registration language pickers) */
div[data-baseweb="popover"] [data-baseweb="menu"],
div[data-baseweb="popover"] [role="listbox"],
div[data-baseweb="popover"] ul {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.12) !important;
    border-radius: 8px !important;
}
div[data-baseweb="popover"] [data-baseweb="menu"] li,
div[data-baseweb="popover"] [role="listbox"] li,
div[data-baseweb="popover"] [role="option"],
div[data-baseweb="popover"] ul li {
    background: #ffffff !important;
    color: #1a1a1a !important;
    font-weight: 500 !important;
}
div[data-baseweb="popover"] [data-baseweb="menu"] li *,
div[data-baseweb="popover"] [role="listbox"] li *,
div[data-baseweb="popover"] [role="option"] *,
div[data-baseweb="popover"] ul li * {
    color: #1a1a1a !important;
}
div[data-baseweb="popover"] [data-baseweb="menu"] li:hover,
div[data-baseweb="popover"] [role="listbox"] li:hover,
div[data-baseweb="popover"] ul li:hover {
    background: #eef2ff !important;
    color: #1a1a1a !important;
}
div[data-baseweb="popover"] [data-baseweb="menu"] li[aria-selected="true"],
div[data-baseweb="popover"] ul li[aria-selected="true"] {
    background: #e0e7ff !important;
    color: #1a1a1a !important;
}

/* Alerts: dark/colored backgrounds so white text stays readable */
div[data-testid="stAlertContainer"] {
    background: rgba(30, 27, 75, 0.92) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
}
div[data-testid="stAlertContainer"] * {
    color: rgba(255,255,255,0.95) !important;
}
div[data-testid="stAlertContainer"][kind="warning"] {
    background: rgba(120, 80, 10, 0.55) !important;
    border-color: rgba(251, 191, 36, 0.45) !important;
}
div[data-testid="stAlertContainer"][kind="info"] {
    background: rgba(30, 58, 138, 0.55) !important;
    border-color: rgba(96, 165, 250, 0.45) !important;
}
div[data-testid="stAlertContainer"][kind="success"] {
    background: rgba(6, 78, 59, 0.55) !important;
    border-color: rgba(52, 211, 153, 0.45) !important;
}
div[data-testid="stAlertContainer"][kind="error"] {
    background: rgba(127, 29, 29, 0.55) !important;
    border-color: rgba(248, 113, 113, 0.45) !important;
}

/* Disabled buttons: muted style, not white-on-white */
.stButton button:disabled,
.stButton button[disabled] {
    background: rgba(255,255,255,0.12) !important;
    color: rgba(255,255,255,0.45) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    box-shadow: none !important;
    transform: none !important;
    cursor: not-allowed !important;
}

/* Expander (AI Tutor context panel + quiz details) */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: rgba(255,255,255,0.95) !important;
    background: rgba(99, 102, 241, 0.2) !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.75rem !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span:not([data-testid="stIconMaterial"]) {
    color: rgba(255,255,255,0.95) !important;
}
[data-testid="stExpanderDetails"] {
    background: rgba(15, 12, 41, 0.5) !important;
    border-top: 1px solid rgba(255,255,255,0.08) !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"],
[data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] p,
[data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] strong {
    color: rgba(255,255,255,0.9) !important;
}
[data-testid="stExpanderDetails"] .stButton button {
    background: rgba(99, 102, 241, 0.35) !important;
    color: rgba(255,255,255,0.95) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
/* Quiz / hint blocks inside expander */
.lp-quiz-item {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 0;
}
.lp-quiz-item.correct { border-left: 4px solid #34d399; }
.lp-quiz-item.wrong { border-left: 4px solid #f87171; }
.lp-hint {
    background: rgba(30, 58, 138, 0.45);
    border: 1px solid rgba(96, 165, 250, 0.35);
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    margin-top: 0.5rem;
    color: #dbeafe;
    font-size: 0.88rem;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.75rem !important;
}
[data-testid="stMetricLabel"] {
    color: rgba(255,255,255,0.65) !important;
}
[data-testid="stMetricValue"] {
    color: rgba(255,255,255,0.95) !important;
}
[data-testid="stExpanderDetails"] [data-testid="stMetric"] {
    background: rgba(99, 102, 241, 0.15) !important;
    border-color: rgba(255,255,255,0.1) !important;
}

/* Profile popover trigger button (top-right user menu) */
[data-testid="stPopover"] > button,
[data-testid="stPopover"] > button[kind="secondary"],
[data-testid="stPopover"] [data-baseweb="button"] {
    background: rgba(30, 27, 75, 0.92) !important;
    background-color: rgba(30, 27, 75, 0.92) !important;
    color: #6ee7b7 !important;
    border: 1px solid rgba(110, 231, 183, 0.45) !important;
    border-radius: 20px !important;
    font-weight: 600 !important;
    padding: 0.45rem 1rem !important;
    min-height: 2.4rem !important;
}
[data-testid="stPopover"] > button:hover,
[data-testid="stPopover"] [data-baseweb="button"]:hover {
    background: rgba(99, 102, 241, 0.45) !important;
    border-color: rgba(110, 231, 183, 0.65) !important;
}
[data-testid="stPopover"] button,
[data-testid="stPopover"] button *:not([data-testid="stIconMaterial"]) {
    color: #6ee7b7 !important;
}
[data-testid="stPopover"] button [data-testid="stMarkdownContainer"],
[data-testid="stPopover"] button [data-testid="stMarkdownContainer"] p {
    color: #6ee7b7 !important;
    font-weight: 600 !important;
}

/* Profile popover panel: white background + black text */
[data-testid="stPopoverBody"],
[data-testid="stPopover"] [data-baseweb="popover"] {
    background: rgba(255,255,255,0.98) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    padding: 0.75rem 1rem !important;
    min-width: 200px !important;
}
[data-testid="stPopoverBody"] *:not(button):not(button *) {
    color: #1a1a1a !important;
}
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"],
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] p,
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stPopoverBody"] [data-testid="stCaptionContainer"],
[data-testid="stPopoverBody"] [data-testid="stCaptionContainer"] *,
[data-testid="stPopoverBody"] [data-testid="stWidgetLabel"],
[data-testid="stPopoverBody"] label,
[data-testid="stPopoverBody"] span,
[data-testid="stPopoverBody"] p,
[data-testid="stPopoverBody"] div {
    color: #1a1a1a !important;
}
[data-testid="stPopoverBody"] hr {
    border-color: rgba(0,0,0,0.12) !important;
}
/* Logout button inside popover: purple gradient, white label (readable) */
[data-testid="stPopoverBody"] .stButton button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #ffffff !important;
}
[data-testid="stPopoverBody"] .stButton button * {
    color: #ffffff !important;
}

/* Inline notice blocks (practice hint, etc.) */
.lp-notice {
    background: rgba(251, 191, 36, 0.18);
    border: 1px solid rgba(251, 191, 36, 0.45);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.75rem;
    color: #fef3c7;
    font-size: 0.92rem;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# NAVIGATION BAR & BREADCRUMB
# ═══════════════════════════════════════════════════════════════
def _render_nav_bar():
    """Render top navigation bar with user menu in header"""
    current_page = st.session_state.get("page", "dashboard")
    user = st.session_state.get("user", {})
    profile = st.session_state.get("profile", {})
    
    user_name = user.get("full_name", "User")
    current_level = profile.get("current_level", "A1")
    
    # Top bar with logo and user info side by side
    col_logo, col_user = st.columns([3, 1])
    
    with col_logo:
        st.markdown("""
        <div style="padding: 1rem 0;">
            <span style="font-size: 1.3rem; font-weight: 700; color: #6ee7b7;">
                AI Language Tutor
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_user:
        # User menu with popover - use custom label to avoid expand_more text
        user_display = f"👤 {user_name}"
        with st.popover(user_display, use_container_width=True):
            st.markdown(f"**{user_name}**")
            st.caption(f"Level: {current_level}")
            st.divider()
            if st.button("Đăng xuất", use_container_width=True, key="logout_in_popover"):
                _logout()  # Use centralized logout function
    
    st.markdown('<div style="height: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;"></div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Dashboard", use_container_width=True, type="primary" if current_page == "dashboard" else "secondary", key="nav_dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("Chủ đề học", use_container_width=True, type="primary" if current_page in ["topics", "topic", "lesson", "quiz"] else "secondary", key="nav_topics"):
            st.session_state.page = "topics"
            st.rerun()
    
    with col3:
        if st.button("AI Tutor", use_container_width=True, type="primary" if current_page == "chat" else "secondary", key="nav_chat"):
            st.session_state.page = "chat"
            st.rerun()
    
    with col4:
        # P1: Add analytics button
        if st.button("Thống kê", use_container_width=True, type="primary" if current_page == "analytics" else "secondary", key="nav_analytics"):
            st.session_state.page = "analytics"
            st.rerun()


def _render_breadcrumb():
    """Render breadcrumb navigation"""
    current_page = st.session_state.get("page", "dashboard")
    
    breadcrumbs = []
    
    # Build breadcrumb trail
    if current_page == "dashboard":
        breadcrumbs = [("", "Dashboard")]
    elif current_page == "topics":
        breadcrumbs = [("", "Dashboard"), ("", "Chủ đề")]
    elif current_page == "topic":
        topic = st.session_state.get("current_topic") or {}
        topic_name = topic.get("name_vi", "Chủ đề")
        breadcrumbs = [("", "Dashboard"), ("", "Chủ đề"), ("", topic_name)]
    elif current_page == "lesson":
        topic = st.session_state.get("current_topic") or {}
        lesson = st.session_state.get("current_lesson") or {}
        topic_name = topic.get("name_vi", "Chủ đề")
        lesson_title = lesson.get("title_vi", "Bài học")
        breadcrumbs = [("", "Dashboard"), ("", "Chủ đề"), ("", topic_name), ("", lesson_title)]
    elif current_page == "quiz":
        topic = st.session_state.get("current_topic") or {}
        topic_name = topic.get("name_vi", "Chủ đề")
        breadcrumbs = [("", "Dashboard"), ("", "Chủ đề"), ("", topic_name), ("", "Quiz")]
    elif current_page == "chat":
        breadcrumbs = [("", "Dashboard"), ("", "Chat AI")]
    elif current_page == "analytics":
        breadcrumbs = [("", "Dashboard"), ("", "Thống kê")]
    else:
        breadcrumbs = [("", "Dashboard")]
    
    # Render breadcrumb
    breadcrumb_html = '<div class="breadcrumb">'
    for i, (icon, label) in enumerate(breadcrumbs):
        if i > 0:
            breadcrumb_html += ' <span>›</span> '
        breadcrumb_html += f'{icon} {label}'
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# UI COMPONENTS
# ═══════════════════════════════════════════════════════════════
def _render_page_header():
    """Render nav bar and breadcrumb for all pages"""
    _render_nav_bar()
    _render_breadcrumb()


def _show_sidebar_user_info():
    """Render nav bar and breadcrumb - replaces old sidebar"""
    # Load user/token/profile first
    user = st.session_state.get("user")
    token = st.session_state.get("access_token")
    profile = st.session_state.get("profile")
    
    # Render header
    _render_page_header()
    
    # OLD sidebar code kept for backwards compatibility (but hidden by CSS)
    
    # ALWAYS show sidebar - even if user is missing
    with st.sidebar:
        # Debug info - ONLY show if debugging is needed (hidden by default)
        show_debug = st.session_state.get("show_debug_info", False)
        if show_debug:
            st.caption(f"page={st.session_state.get('page', '?')}")
            st.caption(f"token={'Yes' if token else 'No'}")
            st.caption(f"user={'Yes' if user else 'No'}")
            st.caption(f"profile={'Yes' if profile else 'No'}")
        
        if not user:
            # User is missing - try to recover or show warning
            st.warning("Session expired. Please login again.")
            if show_debug:
                st.info(f"Debug: token={bool(token)}, user={bool(user)}, profile={bool(profile)}")
            
            if st.button("Quay về đăng nhập", use_container_width=True, key="sidebar_back_to_login"):
                st.session_state.page = "auth"
                st.rerun()
            
            if st.button("🔧 Try Reload Profile", use_container_width=True, key="sidebar_reload_profile"):
                _fetch_profile()
                st.rerun()
            return
        
        st.markdown("### 👤 Tài khoản")
        
        st.markdown(f"**{user.get('full_name', 'User')}**")
        st.markdown(f"📧 {user.get('email', '')}")
        
        level = profile.get("current_level", "A1") if profile else "A1"
        lcolor = LEVEL_COLORS.get(level, "#6ee7b7")
        st.markdown(f"Level: {_badge(level, lcolor)}", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### Điều hướng")
        if st.button("Dashboard", use_container_width=True, key="sidebar_nav_dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("Chủ đề học", use_container_width=True, key="sidebar_nav_topics"):
            st.session_state.page = "topics"
            st.rerun()
        if st.button("Chat AI", use_container_width=True, key="sidebar_nav_chat"):
            st.session_state.page = "chat"
            st.rerun()
        
        st.markdown("---")
        
        # Logout with confirmation
        if not st.session_state.get("confirm_logout"):
            # Show logout button normally
            if st.button("Đăng xuất", use_container_width=True, type="secondary", key="sidebar_logout_btn"):
                st.session_state.confirm_logout = True
                st.rerun()
        else:
            # Show confirmation dialog
            st.warning("Bạn có chắc muốn đăng xuất?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Có, đăng xuất ngay", use_container_width=True, type="primary", key="sidebar_logout_yes"):
                    st.session_state.confirm_logout = False
                    _logout()  # Use the centralized logout function
            with col2:
                if st.button("Hủy", use_container_width=True, key="sidebar_logout_no"):
                    st.session_state.confirm_logout = False
                    st.rerun()


def _progress_html(pct: float, color: str = "#6ee7b7") -> str:
    return f"""
    <div class="prog-bar-bg">
        <div class="prog-bar-fill" style="width:{min(pct,100):.1f}%; background:linear-gradient(90deg,{color},#3b82f6);"></div>
    </div>
    """


def _badge(text: str, color: str) -> str:
    return f'<span class="level-badge" style="background:{color}22; color:{color}; border:1px solid {color}55">{text}</span>'


def _stat(number, label: str):
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{number}</div>
        <div class="stat-label">{label}</div>
    </div>""", unsafe_allow_html=True)


def _card_open() -> str:
    return '<div class="lp-card">'


def _card_close() -> str:
    return '</div>'


# ═══════════════════════════════════════════════════════════════
# PAGE: AUTH
# ═══════════════════════════════════════════════════════════════
def page_auth():
    # Sidebar is hidden on auth page (no need to show backend status to users)
    
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1.5rem">
        <h1 style="font-size:2.2rem; font-weight:800; margin:0;">AI Language Tutor</h1>
        <p style="color:rgba(255,255,255,0.5); margin-top:6px;">Lộ trình học ngoại ngữ thông minh theo chuẩn CEFR</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="lp-card">', unsafe_allow_html=True)
        st.markdown("### 🔑 Đăng nhập / Đăng ký")
        mode = st.radio("Chọn chế độ", ["Đăng nhập", "Đăng ký"], horizontal=True, label_visibility="collapsed")

        if mode == "Đăng nhập":
            email = st.text_input("Email", placeholder="you@example.com", key="l_email")
            pw = st.text_input("Mật khẩu", type="password", key="l_pw")
            if st.button("Đăng nhập", use_container_width=True):
                if email and pw:
                    with st.spinner("Đang xác thực..."):
                        ok, msg = api_login(email, pw)
                    if ok:
                        st.session_state.page = "dashboard"
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Vui lòng điền email và mật khẩu")

        else:
            reg_email = st.text_input("Email", key="r_email")
            reg_name = st.text_input("Họ tên", key="r_name")
            reg_pw = st.text_input("Mật khẩu (≥8 ký tự)", type="password", key="r_pw")
            reg_pw2 = st.text_input("Xác nhận mật khẩu", type="password", key="r_pw2")
            
            c1, c2 = st.columns(2)
            with c1:
                # Only Vietnamese as native language
                native_display = st.selectbox("Tiếng mẹ đẻ", ["Tiếng Việt"], key="r_nat")
                native = "vi"
            with c2:
                # Only English as target language
                target_display = st.selectbox("Học tiếng", ["Tiếng Anh"], key="r_tgt")
                target = "en"

            if st.button("Đăng ký", use_container_width=True):
                if not (reg_email and reg_name and reg_pw):
                    st.warning("Vui lòng điền đầy đủ thông tin")
                elif len(reg_pw) < 8:
                    st.warning("Mật khẩu phải có ít nhất 8 ký tự")
                elif reg_pw != reg_pw2:
                    st.warning("Mật khẩu không khớp")
                else:
                    with st.spinner("Đang tạo tài khoản..."):
                        ok, err = api_register(reg_email, reg_pw, reg_name, native, target)
                    if ok:
                        ok2, msg2 = api_login(reg_email, reg_pw)
                        if ok2:
                            st.session_state.page = "placement"
                            st.rerun()
                        else:
                            st.error(f"Đăng ký OK nhưng đăng nhập thất bại: {msg2}")
                    else:
                        st.error(err)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="lp-card">', unsafe_allow_html=True)
        st.markdown("### Google Sign In")
        google_url = f"{st.session_state.api_base}/api/auth/google"
        st.markdown(
            f'<a href="{google_url}" target="_blank">'
            f'<button style="width:100%;padding:12px;background:#4285F4;color:white;'
            f'border:none;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;">'
            f'Đăng nhập bằng Google</button></a>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)



# ═══════════════════════════════════════════════════════════════
# PAGE: ONBOARDING (for OAuth users)
# ═══════════════════════════════════════════════════════════════
def page_onboarding():
    """Onboarding page for OAuth users to set language preferences"""
    st.title("Chào mừng bạn đến với AI Language Tutor!")
    
    st.markdown("### Thiết lập ngôn ngữ học tập")
    
    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox(
                "🌍 Ngôn ngữ mẹ đẻ",
                options=["vi"],
                format_func=lambda x: "🇻🇳 Tiếng Việt",
                disabled=True,
                key="native_lang"
            )
        
        with col2:
            st.selectbox(
                "Ngôn ngữ bạn muốn học",
                options=["en"],
                format_func=lambda x: "English",
                disabled=True,
                key="target_lang"
            )
        
        st.markdown("---")
        
        submitted = st.form_submit_button("Bắt đầu học", use_container_width=True, type="primary")
        
        if submitted:
            # Call onboarding API
            url = f"{DEFAULT_API_BASE}/api/profile/onboarding"
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            
            payload = {
                "native_language": "vi",
                "target_language": "en"
            }
            
            with st.spinner("Đang lưu thông tin..."):
                try:
                    response = httpx.post(url, json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        st.success("Hoàn thành! Đang chuyển đến bài kiểm tra xếp loại...")
                        _fetch_profile()  # Refresh profile
                        st.session_state.page = "placement"
                        st.query_params.clear()  # Clear URL params
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Lỗi: {response.json().get('detail', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"Không thể kết nối server: {e}")


# ═══════════════════════════════════════════════════════════════
# PAGE: PLACEMENT TEST
# ═══════════════════════════════════════════════════════════════
def page_placement():
    # Show sidebar during placement test
    _show_sidebar_user_info()
    
    st.markdown("## Bài Kiểm Tra Xếp Loại")
    st.markdown("Trả lời các câu hỏi để xác định trình độ ngoại ngữ của bạn (CEFR A1→C2).")

    questions = st.session_state.get("placement_questions") or []
    if not questions:
        if st.button("📥 Tải câu hỏi", type="primary"):
            with st.spinner("Đang tải..."):
                questions = api_get_placement_q()
            st.session_state.placement_questions = questions
            st.rerun()
        return

    total = len(questions)
    answered = len(st.session_state.test_answers)
    pct = answered / total if total else 0
    st.markdown(f"Đã trả lời: **{answered}/{total}**")
    st.markdown(_progress_html(pct * 100), unsafe_allow_html=True)
    st.divider()

    with st.form("placement_form"):
        answers = {}
        for i, q in enumerate(questions, 1):
            qid = q["question_id"]
            opts = q.get("options", [])
            st.markdown(f"**Câu {i}:** {q['question']}")
            if opts:
                choice = st.radio("Chọn câu trả lời", opts, key=f"pl_{qid}", label_visibility="collapsed")
                answers[qid] = choice
            else:
                answers[qid] = st.text_input("Câu trả lời", key=f"pl_{qid}")
            st.markdown("---")

        submitted = st.form_submit_button("📤 Nộp bài", type="primary", use_container_width=True)

    if submitted:
        with st.spinner("Đang chấm điểm..."):
            result = api_submit_placement(answers)
        if result:
            level = result.get("estimated_level") or result.get("level", "A1")
            score = result.get("score", 0)
            st.success(f"Hoàn thành! Trình độ của bạn: **{level}** (Điểm: {score}%)")
            _fetch_profile()
            st.session_state.placement_questions = []
            st.session_state.test_answers = {}
            st.session_state.dashboard = None
            st.session_state.page = "dashboard"
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════════
def page_dashboard():
    # Render nav bar and breadcrumb
    _render_nav_bar()
    _render_breadcrumb()
    
    with st.spinner("Đang tải dashboard..."):
        data = api_dashboard()
    if not data:
        return

    level = data.get("current_level", "A1")
    lp = data.get("level_progress", {})
    pct = lp.get("completion_percentage", 0)
    total = lp.get("total_topics", 0)
    done = lp.get("completed_topics", 0)
    inprog = lp.get("in_progress_topics", 0)
    avg_score = lp.get("average_quiz_score")
    
    # B5: Check level-up eligibility from unified service
    eligibility = None
    try:
        ok, elig_data, _ = _get("/api/learning/level-up-eligibility")
        if ok:
            eligibility = elig_data
    except:
        pass
    
    can_lu = eligibility.get("eligible", False) if eligibility else False

    # Header
    lcolor = LEVEL_COLORS.get(level, "#6ee7b7")
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
        <div style="display:flex; align-items:center; gap:14px;">
            <div>
                <h2 style="margin:0; font-size:1.8rem;">Bảng Điều Khiển Học Tập</h2>
                <p style="margin:0; color:rgba(255,255,255,0.5);">Xin chào, {(st.session_state.user or {}).get('full_name','Học viên')}!</p>
            </div>
        </div>
        {_badge(f'Trình độ {level}', lcolor)}
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    st.markdown(f"#### Tiến độ Level {level}: {pct:.0f}%  ({done}/{total} chủ đề)")
    st.markdown(_progress_html(pct, lcolor), unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    with c1: _stat(done, "Hoàn thành")
    with c2: _stat(inprog, "Đang học")
    with c3: _stat(total - done - inprog, "Chưa bắt đầu")
    with c4: _stat(f"{avg_score:.0f}%" if avg_score else "—", "Điểm TB Quiz")

    st.markdown("")

    # B5: Level-up banner with detailed requirements
    if can_lu and eligibility:
        req = eligibility.get("requirements", {})
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#6366f133,#8b5cf633);
                    border:1px solid #6366f1; border-radius:14px; padding:1.2rem 1.5rem; margin:1rem 0;">
            <h3 style="margin:0; color:#c4b5fd;">{eligibility.get('message', 'Bạn đủ điều kiện Level-Up!')}</h3>
            <p style="margin:8px 0 0; color:rgba(255,255,255,0.7); font-size:0.9rem;">
                Hoàn thành: {req.get('topics_completed', '?')} ({req.get('topics_completed_percent', 0):.0f}%)<br>
                Điểm quiz TB: {req.get('quiz_avg_score', 0):.0f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Làm bài kiểm tra nâng cấp", type="primary"):
            with st.spinner("Đang tải bài kiểm tra..."):
                qs = api_level_questions(level)
            st.session_state.levelup_questions = qs
            st.session_state.test_answers = {}
            st.session_state.page = "levelup"
            st.rerun()
    elif eligibility:
        # Show progress toward eligibility
        req = eligibility.get("requirements", {})
        st.info(f"{eligibility.get('message', 'Tiếp tục học để mở Level-Up Test')}\n\n"
                f"Tiến độ: {req.get('topics_completed', '?')} ({req.get('topics_completed_percent', 0):.0f}%) | "
                f"Quiz: {req.get('quiz_avg_score', 0):.0f}%")
    else:
        # Fallback
        need = round(total * 0.75) - done
        if need > 0:
            st.info(f"Cần hoàn thành thêm {need} chủ đề để mở Level-Up Test.")

    st.divider()

    # Current & next topic
    curr = data.get("current_topic")
    nxt = data.get("next_topic")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Đang học dở")
        if curr:
            st.markdown(f"""
            <div class="lp-card topic-inprogress">
                <div style="font-size:1.1rem; font-weight:600; color:#ffffff;">{curr['name']}</div>
                <div style="color:rgba(255,255,255,0.8); font-size:0.85rem;">{curr['name_vi']}</div>
                <div style="margin:8px 0; color:rgba(255,255,255,0.85);">
                    Bài hoàn thành: {curr['progress']['lesson_completed']}/5
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(_progress_html(curr['progress']['lesson_completed'] * 20, '#60a5fa'), unsafe_allow_html=True)
            
            col_continue, col_chat = st.columns(2)
            with col_continue:
                if st.button(f"Tiếp tục học", key="btn_curr", use_container_width=True):
                    with st.spinner("Đang tải chủ đề..."):
                        detail = api_topic_detail(curr["id"])
                    
                    if not detail:
                        st.error("⚠️ Không thể tải chủ đề. Vui lòng thử lại sau.")
                        st.stop()
                    
                    st.session_state.current_topic = detail
                    
                    # Activate topic + first incomplete lesson
                    lesson_order = curr.get("progress", {}).get("lesson_completed", 0) + 1
                    api_activate_context(curr["id"], lesson_order=min(lesson_order, 5), mode="lesson")
                    
                    st.session_state.page = "topic"
                    st.rerun()
            
            with col_chat:
                # P1.4: Add "Học với AI" button
                if st.button("Học với AI", key="btn_chat_curr", use_container_width=True):
                    # Activate context
                    lesson_order = curr.get("progress", {}).get("lesson_completed", 0) + 1
                    api_activate_context(curr["id"], lesson_order=min(lesson_order, 5), mode="chat")
                    
                    # Go to chat
                    st.session_state.page = "chat"
                    st.rerun()
        else:
            st.info("Chưa có chủ đề đang học")

    with col_b:
        st.markdown("#### Chủ đề tiếp theo")
        if nxt:
            st.markdown(f"""
            <div class="lp-card">
                <div style="font-size:1.1rem; font-weight:600; color:#ffffff;">{nxt['name']}</div>
                <div style="color:rgba(255,255,255,0.8); font-size:0.85rem;">{nxt['name_vi']}</div>
                <div style="color:rgba(255,255,255,0.65); font-size:0.82rem; margin-top:6px;">
                    ⏱ ~{nxt.get('estimated_minutes',30)} phút
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Bắt đầu học", key="btn_next", type="primary"):
                detail = api_topic_detail(nxt["id"])
                st.session_state.current_topic = detail
                st.session_state.page = "topic"
                st.rerun()
        else:
            st.success("Bạn đã học hết tất cả chủ đề!")

    # All topics button
    st.markdown("")
    if st.button("Xem toàn bộ chủ đề", use_container_width=True):
        st.session_state.topic_list = None
        st.session_state.page = "topics"
        st.rerun()
    
    # Review previous levels section
    level_order = ["A1", "A2", "B1", "B2", "C1", "C2"]
    current_level_index = level_order.index(level)
    
    if current_level_index > 0:  # Has previous levels
        st.divider()
        st.markdown("#### Ôn lại bài cũ")
        st.markdown("Truy cập lại các bài học ở level thấp hơn để củng cố kiến thức")
        
        # Show buttons for previous levels
        previous_levels = level_order[:current_level_index]
        cols = st.columns(len(previous_levels))
        
        for idx, prev_level in enumerate(previous_levels):
            with cols[idx]:
                level_color = LEVEL_COLORS.get(prev_level, "#6ee7b7")
                if st.button(f"Level {prev_level}", key=f"review_{prev_level}", use_container_width=True):
                    # Load topics for that level
                    st.session_state.topic_list = None
                    st.session_state.review_level = prev_level  # Store which level to show
                    st.session_state.page = "topics"
                    st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: TOPICS LIST
# ═══════════════════════════════════════════════════════════════
def page_topics():
    # Show sidebar with user info and logout
    _show_sidebar_user_info()
    
    current_user_level = current_level()
    
    # Allow user to select level (current and all previous levels)
    level_order = ["A1", "A2", "B1", "B2", "C1", "C2"]
    current_level_index = level_order.index(current_user_level)
    available_levels = level_order[:current_level_index + 1]  # Current + previous levels
    
    # Check if user is coming from dashboard with a specific review level
    review_level = st.session_state.get("review_level")
    if review_level and review_level in available_levels:
        default_index = available_levels.index(review_level)
        st.session_state.review_level = None  # Clear after using
    else:
        default_index = len(available_levels) - 1  # Default to current level
    
    st.markdown(f"## Chủ đề học tập")
    
    # Level selector with labels
    col1, col2 = st.columns([3, 1])
    with col1:
        # Add labels to show current vs review
        level_options = []
        for lvl in available_levels:
            if lvl == current_user_level:
                level_options.append(f"{lvl} (Level hiện tại)")
            else:
                level_options.append(f"{lvl} (Ôn lại)")
        
        selected_display = st.selectbox(
            "Chọn Level:",
            options=level_options,
            index=default_index,
            key="selected_level_topics"
        )
        # Extract actual level from display text
        selected_level = selected_display.split(" ")[0]
    with col2:
        if st.button("← Dashboard", key="back_dash_topics"):
            st.session_state.page = "dashboard"
            st.rerun()
    
    # Show info message if reviewing old level
    if selected_level != current_user_level:
        st.info(f"Bạn đang ôn lại level {selected_level}. Level hiện tại của bạn là {current_user_level}.")

    with st.spinner("Đang tải chủ đề..."):
        topics = api_topics(selected_level)

    if not topics:
        st.warning("Chưa có chủ đề nào. Vui lòng kiểm tra kết nối backend.")
        return

    done = sum(1 for t in topics if t["progress"]["status"] == "completed")
    st.markdown(f"Hoàn thành: **{done}/{len(topics)}** chủ đề")
    st.markdown(_progress_html(done / len(topics) * 100 if topics else 0), unsafe_allow_html=True)
    st.markdown("")

    for t in topics:
        prog = t.get("progress", {})
        status = prog.get("status", "not_started")
        score = prog.get("quiz_score")
        l_done = prog.get("lesson_completed", 0)

        if status == "completed":
            icon, css_class = "", "topic-completed"
            score_txt = f" • Quiz: {score:.0f}%" if score is not None else ""
        elif status == "in_progress":
            icon, css_class = "", "topic-inprogress"
            score_txt = f" • Bài {l_done}/5"
        else:
            icon, css_class = "⬜", ""
            score_txt = ""

        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="lp-card {css_class}" style="cursor:pointer;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:1.4rem;">{icon}</span>
                    <div>
                        <div style="font-weight:600;">{t['order']}. {t['name']}</div>
                        <div style="color:rgba(255,255,255,0.5); font-size:0.82rem;">{t['name_vi']}{score_txt}</div>
                        <div style="color:rgba(255,255,255,0.35); font-size:0.78rem;">
                            ⏱ ~{t.get('estimated_minutes',30)} phút
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            label = "Tiếp tục" if status == "in_progress" else ("Xem lại" if status == "completed" else "Học")
            if st.button(label, key=f"tp_{t['id']}"):
                detail = api_topic_detail(t["id"])
                st.session_state.current_topic = detail
                
                # Activate this topic + current lesson
                lesson_order = t.get("progress", {}).get("lesson_completed", 0) + 1
                api_activate_context(t["id"], lesson_order=min(lesson_order, 5), mode="lesson")
                
                st.session_state.page = "topic"
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: TOPIC DETAIL
# ═══════════════════════════════════════════════════════════════
def page_topic():
    # Show sidebar with user info and logout
    _show_sidebar_user_info()
    
    topic = st.session_state.get("current_topic")
    if not topic:
        st.session_state.page = "dashboard"
        st.rerun()

    prog = topic.get("progress", {})
    l_done = prog.get("lesson_completed", 0)
    lessons = topic.get("lessons", [])
    status = prog.get("status", "not_started")

    # Header
    lcolor = LEVEL_COLORS.get(topic.get("level","A1"), "#6ee7b7")
    if st.button("← Về trang chủ"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown(f"""
    <div class="lp-card" style="margin-top:0.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div style="font-size:1.5rem; font-weight:700; color:#ffffff;">{topic['name']}</div>
                <div style="color:rgba(255,255,255,0.75);">{topic['name_vi']}</div>
                <div style="margin-top:8px; color:rgba(255,255,255,0.6); font-size:0.85rem;">
                    {'  •  '.join(topic.get('grammar_focus',[])[:3])}
                </div>
            </div>
            <div>{_badge(topic.get('level','A1'), lcolor)}</div>
        </div>
        <div style="margin-top:12px; color:rgba(255,255,255,0.85);">
            Tiến độ: {l_done}/5 bài
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(_progress_html(l_done * 20, lcolor), unsafe_allow_html=True)

    st.markdown("### Các bài học")

    for i, lesson in enumerate(lessons):
        l_order = lesson["order"]
        l_type = lesson["lesson_type"]
        icon = LESSON_ICONS.get(l_type, "📄")
        done = l_done >= l_order
        active = l_order == l_done + 1
        locked = l_order > l_done + 1

        if done:
            state_icon, state_txt, css = "", "Hoàn thành", "done"
        elif active:
            state_icon, state_txt, css = "", "Đang học", "active"
        else:
            state_icon, state_txt, css = "", "Chưa mở", ""

        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
            <div class="lesson-step {css}">
                <span style="font-size:1.5rem;">{icon}</span>
                <div style="flex:1;">
                    <div style="font-weight:600; color:#ffffff;">{icon} {lesson['title']}</div>
                    <div style="font-size:0.8rem; color:rgba(255,255,255,0.7);">{lesson.get('title_vi','')}</div>
                </div>
                <span style="font-size:0.8rem; color:rgba(255,255,255,0.4);">{state_icon} {state_txt}</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if not locked:
                btn_label = "Xem lại" if done else "Bắt đầu"
                if st.button(btn_label, key=f"les_{lesson['id']}"):
                    with st.spinner("Đang tải bài học..."):
                        full = api_lesson(lesson["id"])
                    st.session_state.current_lesson = full
                    
                    # Activate context with lesson
                    api_activate_context(topic["id"], lesson_order=l_order, mode="lesson")
                    
                    if l_type in ("quiz", "kiểm tra"):
                        with st.spinner("Đang tải quiz..."):
                            qdata = api_quiz_questions(topic["id"])
                        st.session_state.quiz_questions = qdata
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_result = None
                        st.session_state.page = "quiz"
                    else:
                        st.session_state.page = "lesson"
                    st.rerun()
            else:
                st.markdown('<div style="padding:8px; color:rgba(255,255,255,0.3); font-size:0.8rem;"></div>', unsafe_allow_html=True)

    # Chat button
    st.divider()
    if st.button("Luyện tập với AI Tutor", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: LESSON VIEW
# ═══════════════════════════════════════════════════════════════
def page_lesson():
    # Show sidebar with user info and logout
    _show_sidebar_user_info()
    
    lesson = st.session_state.get("current_lesson")
    topic = st.session_state.get("current_topic")
    if not lesson:
        st.session_state.page = "topic"
        st.rerun()

    l_type = lesson.get("lesson_type", "")
    content = lesson.get("content", {})
    icon = LESSON_ICONS.get(l_type, "📄")

    if st.button("← Quay lại chủ đề"):
        st.session_state.page = "topic"
        st.rerun()

    st.markdown(f"## {icon} {lesson['title']}")
    if lesson.get("title_vi"):
        st.markdown(f"*{lesson['title_vi']}*")
    st.divider()

    # ── Grammar lesson ──────────────────────────────────────────
    if l_type in ("grammar", "ngữ pháp"):
        st.markdown("### 📚 Giải thích")
        # Prioritize Vietnamese explanation
        explanation_vi = content.get('explanation_vi', '')
        explanation_en = content.get('explanation', '')
        
        if explanation_vi:
            st.markdown(f"""<div class="lp-card">
                <p style="font-size:1.05rem; line-height:1.6;">{explanation_vi}</p>
                <hr style="border-color:rgba(255,255,255,0.1); margin: 12px 0;">
                <p style="color:rgba(255,255,255,0.5); font-size:0.9rem; font-style:italic;">{explanation_en}</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="lp-card">
                <p>{explanation_en}</p>
            </div>""", unsafe_allow_html=True)

        # Prioritize Vietnamese key_points
        key_points_vi = content.get("key_points_vi", [])
        key_points_en = content.get("key_points", [])
        
        if key_points_vi:
            st.markdown("### 🔑 Điểm chính")
            for pt in key_points_vi:
                st.markdown(f"• **{pt}**")
        elif key_points_en:
            st.markdown("### 🔑 Điểm chính")
            for pt in key_points_en:
                st.markdown(f"• **{pt}**")

        if content.get("examples"):
            st.markdown("### 💡 Ví dụ")
            for ex in content["examples"]:
                st.markdown(f"""<div class="lp-card" style="margin:6px 0; padding:12px 16px;">
                    <div style="font-size:1rem; font-weight:600;">{ex['en']}</div>
                    <div style="color:rgba(255,255,255,0.6); margin-top:4px;">{ex['vi']}</div>
                </div>""", unsafe_allow_html=True)

        # Prioritize Vietnamese notes
        notes_vi = content.get("notes_vi", "")
        notes_en = content.get("notes", "")
        
        if notes_vi:
            st.info(f"**💡 Lưu ý:** {notes_vi}")
        elif notes_en:
            st.info(f"**💡 Lưu ý:** {notes_en}")

    # ── Vocabulary lesson ───────────────────────────────────────
    elif l_type in ("vocabulary", "từ vựng"):
        words = content.get("words", [])
        st.markdown(f"### Danh sách từ vựng ({len(words)} từ)")
        for w in words:
            st.markdown(f"""<div class="lp-card" style="margin:6px 0; padding:12px 18px;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <span style="font-size:1.15rem; font-weight:700; color:#6ee7b7;">{w['word']}</span>
                        <span style="color:rgba(255,255,255,0.4); font-size:0.85rem; margin-left:10px;">{w.get('pronunciation','')}</span>
                    </div>
                    <div style="color:#fbbf24; font-weight:600;">{w['meaning']}</div>
                </div>
                <div style="color:rgba(255,255,255,0.55); font-size:0.87rem; margin-top:6px; font-style:italic;">
                    {w.get('example','')}
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Practice lesson ─────────────────────────────────────────
    elif l_type in ("practice", "thực hành"):
        exercises = content.get("exercises", [])
        st.markdown(f"### Bài tập ({len(exercises)} câu)")

        if "practice_answers" not in st.session_state:
            st.session_state.practice_answers = {}
        if "practice_checked" not in st.session_state:
            st.session_state.practice_checked = {}
        if "error_analysis" not in st.session_state:
            st.session_state.error_analysis = {}

        for i, ex in enumerate(exercises):
            qkey = f"prac_{lesson['id']}_{i}"
            st.markdown(f"""<div class="lp-card">
                <div style="font-weight:600; margin-bottom:10px;">Câu {i+1}: {ex['question']}</div>
            """, unsafe_allow_html=True)

            opts = ex.get("options", [])
            if opts:
                choice = st.radio("Chọn đáp án:", opts, key=qkey, label_visibility="collapsed")
                if st.button("Kiểm tra", key=f"chk_{qkey}"):
                    is_right = choice == ex["answer"]
                    st.session_state.practice_checked[qkey] = (choice, is_right, ex["answer"], ex.get("explanation",""))
                    
                    # ✨ NEW: If wrong, analyze error
                    if not is_right:
                        with st.spinner("AI đang phân tích lỗi..."):
                            analysis = api_analyze_error(
                                question=ex['question'],
                                user_answer=choice,
                                correct_answer=ex['answer'],
                                skill_tag=ex.get('skill', 'general'),
                                lesson_id=lesson['id'],
                                topic_id=topic['id'] if topic else None
                            )
                            if analysis:
                                st.session_state.error_analysis[qkey] = analysis
                    
                    st.rerun()

            checked = st.session_state.practice_checked.get(qkey)
            if checked:
                usr, ok, ans, expl = checked
                if ok:
                    st.success(f"Đúng! {expl}")
                else:
                    st.error(f"Sai. Đáp án đúng: **{ans}**\n\n{expl}")
                    
                    # ✨ NEW: Show error analysis panel
                    error_analysis = st.session_state.error_analysis.get(qkey)
                    if error_analysis:
                        st.markdown("---")
                        st.markdown("### AI Phân Tích Lỗi")
                        
                        error = error_analysis.get("error", {})
                        freq = error_analysis.get("frequency", 0)
                        suggestion = error_analysis.get("suggestion", "")
                        rec_type = error_analysis.get("recommendation_type", "EXPLAIN")
                        
                        # Error type badge
                        error_type = error.get("error_type", "GENERAL_ERROR").replace("_", " ")
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"**Loại lỗi:** {error_type}")
                        with col_b:
                            if freq == 1:
                                st.info(f"Lần {freq}")
                            elif freq <= 3:
                                st.warning(f"Lần {freq}")
                            else:
                                st.error(f"Lần {freq}")
                        
                        # AI Suggestion
                        st.markdown("**Gợi ý từ AI:**")
                        st.markdown(f"> {suggestion}")
                        
                        # Action buttons
                        next_action = error_analysis.get("next_action", {})
                        if rec_type in ["INTENSIVE_PRACTICE", "BACK_TO_BASICS"]:
                            st.markdown("---")
                            st.warning(f"**Cảnh báo**: Bạn đã sai lỗi này **{freq} lần**. Đây là dấu hiệu cần ôn lại kiến thức!")
                            st.markdown("")
                            
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                if st.button("Học với AI Tutor ngay", key=f"ai_tutor_{qkey}", type="primary", use_container_width=True):
                                    # Prepare context for AI
                                    error_context = {
                                        "error_type": error.get("error_type", ""),
                                        "skill_tag": error.get("skill_tag", ""),
                                        "frequency": freq,
                                        "question": ex['question'],
                                        "user_answer": usr,
                                        "correct_answer": ans,
                                        "explanation": error.get("explanation", "")
                                    }
                                    
                                    # Save to session state
                                    st.session_state.ai_tutor_mode = True
                                    st.session_state.error_context = error_context
                                    
                                    # Prepare initial AI message
                                    error_type_vn = {
                                        "TENSE_MISMATCH": "thì trong tiếng Anh",
                                        "SUBJECT_VERB_AGREEMENT": "sự hòa hợp chủ ngữ - động từ",
                                        "WORD_ORDER": "trật tự từ",
                                        "VOCABULARY_CHOICE": "lựa chọn từ vựng",
                                        "GENERAL_ERROR": "ngữ pháp"
                                    }.get(error.get("error_type", ""), "ngữ pháp")
                                    
                                    initial_prompt = f"""Tôi cần giúp đỡ khẩn cấp! Tôi đã sai lỗi về **{error_type_vn}** tới {freq} lần rồi.

Câu hỏi vừa sai: {ex['question']}
Câu trả lời của tôi: {usr}
Đáp án đúng: {ans}

Bạn có thể:
1. Giải thích chi tiết lý thuyết về {error_type_vn} (bằng tiếng Việt)
2. Cho tôi 3-5 ví dụ minh họa rõ ràng
3. Đưa ra 5 bài tập tương tự để tôi luyện tập
4. Chấm bài và giải thích khi tôi trả lời

Hãy giúp tôi khắc phục lỗi này nhé!"""
                                    
                                    # Initialize chat with this context
                                    st.session_state.messages = [
                                        {"role": "user", "content": initial_prompt}
                                    ]
                                    
                                    # Switch to chat page
                                    st.session_state.page = "chat"
                                    st.rerun()
                            
                            with col2:
                                if st.button("Xem lại bài", key=f"review_{qkey}", use_container_width=True):
                                    st.info("Cuộn lên trên để xem lại nội dung bài học nhé!")
                        elif rec_type == "EXPLAIN_WITH_EXAMPLES":
                            # For 2-3 times, offer optional AI help
                            st.markdown("---")
                            if st.button("Cần AI giải thích thêm?", key=f"ai_help_{qkey}", use_container_width=True):
                                # Same logic as above
                                error_context = {
                                    "error_type": error.get("error_type", ""),
                                    "skill_tag": error.get("skill_tag", ""),
                                    "frequency": freq,
                                    "question": ex['question'],
                                    "user_answer": usr,
                                    "correct_answer": ans,
                                    "explanation": error.get("explanation", "")
                                }
                                st.session_state.ai_tutor_mode = True
                                st.session_state.error_context = error_context
                                
                                error_type_vn = {
                                    "TENSE_MISMATCH": "thì trong tiếng Anh",
                                    "SUBJECT_VERB_AGREEMENT": "sự hòa hợp chủ ngữ - động từ",
                                    "WORD_ORDER": "trật tự từ",
                                    "VOCABULARY_CHOICE": "lựa chọn từ vựng",
                                    "GENERAL_ERROR": "ngữ pháp"
                                }.get(error.get("error_type", ""), "ngữ pháp")
                                
                                initial_prompt = f"""Tôi cần giải thích thêm về lỗi {error_type_vn}.

Câu hỏi: {ex['question']}
Tôi trả lời: {usr}
Đáp án đúng: {ans}

Bạn có thể giải thích rõ hơn và cho tôi vài ví dụ + bài tập để luyện không?"""
                                
                                st.session_state.messages = [{"role": "user", "content": initial_prompt}]
                                st.session_state.page = "chat"
                                st.rerun()
                        else:
                            # For 1st time, just show the explanation
                            pass
                        
                        st.markdown("---")
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("")

    # ── Writing lesson (NEW) ────────────────────────────────────
    elif l_type in ("writing", "viết"):
        st.markdown("### Viết đoạn văn ngắn")
        
        # Get writing prompt
        prompt = content.get("prompt", "")
        prompt_vi = content.get("prompt_vi", "")
        tips = content.get("tips", [])
        example = content.get("example", {})
        min_words = content.get("min_words", 50)
        
        # Show prompt
        st.markdown(f"""<div class="lp-card">
            <div style="font-weight:600; font-size:1.1rem; margin-bottom:8px;">Đề bài:</div>
            <p style="color:#6ee7b7;">{prompt}</p>
            <p style="color:rgba(255,255,255,0.6); font-style:italic;">{prompt_vi}</p>
        </div>""", unsafe_allow_html=True)
        
        # Show tips
        if tips:
            with st.expander("Gợi ý viết"):
                for tip in tips:
                    st.markdown(f"• {tip}")
        
        # Show example if available
        if example:
            with st.expander("Xem ví dụ mẫu"):
                st.markdown(f"**{example.get('title', 'Example')}**")
                st.markdown(example.get('text', ''))
                if example.get('translation'):
                    st.caption(f"*{example.get('translation')}*")
        
        # Writing area - word limits by level
        topic_level = topic.get("level", "A1") if topic else "A1"
        if topic_level == "A1":
            MIN_WORDS, MAX_WORDS = 10, 50
        else:
            MIN_WORDS, MAX_WORDS = 20, 100
        
        st.markdown(f"**Viết bài của bạn** (từ {MIN_WORDS} đến {MAX_WORDS} từ):")
        writing_key = f"writing_{lesson['id']}"
        user_writing = st.text_area(
            "Your writing:",
            height=200,
            key=writing_key,
            label_visibility="collapsed",
            placeholder="Start writing here..."
        )
        
        # Word count
        word_count = len(user_writing.split()) if user_writing else 0
        col_count, col_btn = st.columns([3, 1])
        with col_count:
            if word_count < MIN_WORDS:
                st.caption(f"Số từ: {word_count} (Cần tối thiểu {MIN_WORDS} từ)")
            elif word_count > MAX_WORDS:
                st.caption(f"Số từ: {word_count} (Vượt quá {MAX_WORDS} từ, hãy rút gọn)")
            else:
                st.caption(f"Số từ: {word_count} ✓")
        
        # Submit for AI review
        with col_btn:
            can_submit = MIN_WORDS <= word_count <= MAX_WORDS
            if st.button("Gửi AI chấm bài", disabled=not can_submit, use_container_width=True):
                with st.spinner("AI đang đọc và chấm bài..."):
                    # Submit to backend API
                    ok, feedback_data, err = api_submit_writing(
                        lesson_id=lesson["id"],
                        topic_id=topic["id"] if topic else None,
                        prompt=prompt,
                        user_text=user_writing,
                        word_count=word_count
                    )
                    
                    if ok:
                        st.session_state.writing_feedback = feedback_data
                        st.session_state.writing_attempt = feedback_data.get("attempt_number", 1)
                        st.rerun()
                    else:
                        st.error(f"Lỗi: {err}")
        
        # Show AI feedback if available
        if st.session_state.get("writing_feedback"):
            feedback = st.session_state.writing_feedback
            attempt = st.session_state.get("writing_attempt", 1)
            
            st.markdown("---")
            st.markdown(f"### 📝 Kết quả chấm bài (Lần {attempt})")
            
            # Score cards
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Ngữ pháp", f"{feedback['score_grammar']:.1f}/25")
            with col2:
                st.metric("Từ vựng", f"{feedback['score_vocabulary']:.1f}/25")
            with col3:
                st.metric("Nội dung", f"{feedback['score_content']:.1f}/25")
            with col4:
                st.metric("Cấu trúc", f"{feedback['score_structure']:.1f}/25")
            with col5:
                score_total = feedback['score_total']
                score_color = "#10b981" if score_total >= 80 else "#f59e0b" if score_total >= 60 else "#ef4444"
                st.markdown(f"<div style='text-align:center;'><div style='font-size:0.8rem;color:rgba(255,255,255,0.6);'>Tổng điểm</div><div style='font-size:1.8rem;font-weight:700;color:{score_color};'>{score_total:.0f}</div><div style='font-size:0.8rem;color:rgba(255,255,255,0.6);'>/100</div></div>", unsafe_allow_html=True)
            
            st.markdown("")
            
            # General feedback
            st.markdown("**💬 Nhận xét chung:**")
            st.info(feedback['feedback'])
            
            # Detailed feedback with better visibility
            detailed = feedback.get('detailed_feedback')
            if detailed:
                if detailed.get('corrections'):
                    st.markdown("**🔧 Cần sửa:**")
                    for corr in detailed['corrections']:
                        st.markdown(f"<div style='color: rgba(255, 255, 255, 0.95); padding: 4px 0;'>• {corr}</div>", unsafe_allow_html=True)
                
                if detailed.get('suggestions'):
                    st.markdown("**💡 Gợi ý cải thiện:**")
                    for sug in detailed['suggestions']:
                        st.markdown(f"<div style='color: rgba(255, 255, 255, 0.95); padding: 4px 0;'>• {sug}</div>", unsafe_allow_html=True)
            
            st.markdown("")
            
            # Action buttons
            col_retry, col_history = st.columns(2)
            with col_retry:
                if st.button("✍️ Viết lại bài khác", use_container_width=True):
                    st.session_state.writing_feedback = None
                    st.session_state.writing_attempt = None
                    st.rerun()
            
            with col_history:
                if st.button("📚 Xem lịch sử", use_container_width=True):
                    st.session_state.show_writing_history = True
                    st.rerun()
        
        # Show writing history if requested
        if st.session_state.get("show_writing_history"):
            st.markdown("---")
            st.markdown("### 📚 Lịch sử bài viết")
            
            history = api_writing_history(lesson_id=lesson["id"], limit=5)
            
            if history:
                for item in history:
                    # Create expander title with key info
                    score_display = f"{item.get('score_total', 0):.0f}/100" if item.get('score_total') else "Chưa chấm"
                    expander_title = f"Lần {item['attempt_number']} - {item['submitted_at'][:10]} - Điểm: {score_display}"
                    
                    with st.expander(expander_title, expanded=False):
                        # Show metadata
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(f"📝 Số từ: {item['word_count']}")
                        with col2:
                            if item.get('reviewed_at'):
                                st.caption(f"✅ Đã chấm: {item['reviewed_at'][:10]}")
                        
                        # Show prompt
                        st.markdown("**Đề bài:**")
                        st.info(item.get('prompt', 'N/A'))
                        
                        # Show user's writing
                        st.markdown("**Bài viết của bạn:**")
                        st.write(item.get('user_text', 'N/A'))
                        
                        # Show scores if available
                        if item.get('score_total'):
                            st.markdown("**Điểm chi tiết:**")
                            score_cols = st.columns(4)
                            with score_cols[0]:
                                st.metric("Ngữ pháp", f"{item.get('score_grammar', 0):.0f}/25")
                            with score_cols[1]:
                                st.metric("Từ vựng", f"{item.get('score_vocabulary', 0):.0f}/25")
                            with score_cols[2]:
                                st.metric("Nội dung", f"{item.get('score_content', 0):.0f}/25")
                            with score_cols[3]:
                                st.metric("Cấu trúc", f"{item.get('score_structure', 0):.0f}/25")
                            
                            # Progress bar for total score
                            st.progress(item['score_total'] / 100)
                            
                            # Show feedback
                            if item.get('feedback'):
                                st.markdown("**Nhận xét:**")
                                st.success(item['feedback'])
                            
                            # Show detailed feedback if available
                            if item.get('detailed_feedback'):
                                detailed = item['detailed_feedback']
                                
                                if detailed.get('corrections'):
                                    st.markdown("**Sửa lỗi:**")
                                    for correction in detailed['corrections']:
                                        st.warning(f"• {correction}")
                                
                                if detailed.get('suggestions'):
                                    st.markdown("**Gợi ý cải thiện:**")
                                    for suggestion in detailed['suggestions']:
                                        st.info(f"• {suggestion}")
            else:
                st.info("Chưa có bài viết nào")
            
            if st.button("Đóng lịch sử"):
                st.session_state.show_writing_history = False
                st.rerun()
    
    # End of practice section

    # Mark lesson complete and go back
    st.divider()
    
    # Calculate practice completion stats
    # Fix: exercises and session state might not be defined if lesson type is not "practice"
    exercises = content.get("exercises", []) if l_type in ("practice", "thực hành") else []
    total_exercises = len(exercises)
    checked_count = len(st.session_state.get("practice_checked", {}))
    correct_count = sum(1 for (_, is_correct, _, _) in st.session_state.get("practice_checked", {}).values() if is_correct)
    
    # Show progress
    if total_exercises > 0:
        st.markdown(f"**Tiến độ:** {checked_count}/{total_exercises} câu đã làm | {correct_count}/{total_exercises} câu đúng")
        
        # Calculate accuracy
        if checked_count > 0:
            accuracy = (correct_count / checked_count) * 100
            if accuracy == 100 and checked_count == total_exercises:
                st.success(f"Hoàn hảo! Bạn đã làm đúng tất cả {correct_count} câu!")
            else:
                st.warning(f"Độ chính xác: {accuracy:.0f}% - Cần đúng 100% mới hoàn thành bài")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Quay lại", use_container_width=True):
            st.session_state.page = "topic"
            st.rerun()
    with col2:
        # Completion logic:
        # - Practice lesson: Need 100% correct
        # - Writing lesson: Need to submit and get AI feedback
        # - Other lessons (grammar, vocabulary): Can complete immediately
        if l_type in ("practice", "thực hành"):
            can_complete = (total_exercises > 0 and 
                           checked_count == total_exercises and 
                           correct_count == total_exercises)
        elif l_type in ("writing", "viết"):
            # Writing lesson: can complete if user has submitted and got feedback
            can_complete = st.session_state.get("writing_feedback") is not None
        else:
            # Grammar/vocabulary lessons can be completed without exercises
            can_complete = True
        
        if can_complete:
            if st.button("Hoàn thành bài này", type="primary", use_container_width=True):
                if topic:
                    api_complete_lesson(topic["id"], lesson["order"])
                    # Refresh topic
                    detail = api_topic_detail(topic["id"])
                    st.session_state.current_topic = detail
                # clear practice state
                st.session_state.practice_answers = {}
                st.session_state.practice_checked = {}
                st.session_state.error_analysis = {}
                st.session_state.page = "topic"
                st.rerun()
        else:
            # Show appropriate warning message based on lesson type
            if l_type in ("writing", "viết"):
                st.markdown(
                    '<div class="lp-notice">Bạn cần gửi bài viết và nhận phản hồi từ AI để hoàn thành!</div>',
                    unsafe_allow_html=True,
                )
            else:
                # For practice lessons
                st.markdown(
                    '<div class="lp-notice">Phải làm đúng 100% bài tập practice mới có thể hoàn thành!</div>',
                    unsafe_allow_html=True,
                )
            st.button(
                "Hoàn thành bài này",
                type="primary",
                use_container_width=True,
                disabled=True,
            )


# ═══════════════════════════════════════════════════════════════
# PAGE: QUIZ
# ═══════════════════════════════════════════════════════════════
def page_quiz():
    # Show sidebar with user info and logout
    _show_sidebar_user_info()
    
    topic = st.session_state.get("current_topic")
    qdata = st.session_state.get("quiz_questions")
    result = st.session_state.get("quiz_result")

    # Show results if already submitted
    if result:
        page_quiz_result()
        return

    if not qdata or not topic:
        st.session_state.page = "topic"
        st.rerun()

    questions = qdata.get("questions", [])
    answers = st.session_state.get("quiz_answers", {})

    if st.button("← Quay lại chủ đề"):
        st.session_state.page = "topic"
        st.rerun()

    st.markdown(f"## Quiz: {qdata.get('topic_name','')}")
    st.markdown(f"*{topic.get('name_vi','')}*")

    answered = len([a for a in answers.values() if a])
    total = len(questions)
    st.markdown(f"Đã trả lời: **{answered}/{total}**")
    st.markdown(_progress_html(answered / total * 100 if total else 0, "#fbbf24"), unsafe_allow_html=True)
    st.markdown("""<div class="lp-card" style="background:rgba(251,191,36,0.08); border-color:#fbbf24;">
        ⚡ Điểm ≥ 70% = hoàn thành chủ đề • Được làm lại nếu không đạt
    </div>""", unsafe_allow_html=True)
    st.markdown("")

    with st.form("quiz_form"):
        for i, q in enumerate(questions, 1):
            qid = q["id"]
            st.markdown(f"""<div class="lp-card">
                <div style="font-weight:600; font-size:1rem;">Câu {i}/{total}: {q['question']}</div>
            </div>""", unsafe_allow_html=True)
            choice = st.radio("Chọn đáp án", q["options"], key=f"q_{qid}", label_visibility="collapsed")
            answers[qid] = choice
            st.markdown("")

        submitted = st.form_submit_button(
            "📤 Nộp bài quiz", type="primary", use_container_width=True
        )

    if submitted:
        if len(answers) < total:
            st.warning("Vui lòng trả lời tất cả câu hỏi!")
        else:
            with st.spinner("Đang chấm điểm..."):
                res = api_submit_quiz(topic["id"], answers)
            if res:
                st.session_state.quiz_result = res
                st.session_state.quiz_answers = {}
                # Refresh topic progress
                detail = api_topic_detail(topic["id"])
                st.session_state.current_topic = detail
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: QUIZ RESULT
# ═══════════════════════════════════════════════════════════════
def page_quiz_result():
    # Show sidebar ONLY if not already shown by parent page_quiz()
    # Check if we're being called directly (page == "quiz_result") or from page_quiz()
    if st.session_state.get("page") == "quiz_result":
        _show_sidebar_user_info()
    
    result = st.session_state.get("quiz_result")
    topic = st.session_state.get("current_topic")
    if not result:
        st.session_state.page = "dashboard"
        st.rerun()

    # Handle both old format (quiz_response) and new format (quiz_response + weak_skills)
    quiz_response = result.get("quiz_response") if "quiz_response" in result else result
    
    score = quiz_response.get("score", 0)
    passed = quiz_response.get("passed", False)
    correct = quiz_response.get("correct_count", 0)
    total = quiz_response.get("total_count", 0)
    feedback = quiz_response.get("feedback", "")
    completed = quiz_response.get("topic_completed", False)
    results = quiz_response.get("results", [])
    
    # New: Extract weak_skills for AI review
    weak_skills = result.get("weak_skills", [])
    ai_review_enabled = result.get("ai_review_enabled", False)
    ai_review_prompt = result.get("ai_review_prompt", "")

    # Score circle
    color = "#34d399" if passed else "#f87171"
    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem 0;">
        <div style="font-size:4rem; font-weight:800; color:{color};">{score:.0f}%</div>
        <div style="font-size:1.4rem; font-weight:600; color:{'#34d399' if passed else '#f87171'};">
            {'ĐẠT!' if passed else 'CHƯA ĐẠT'}
        </div>
        <div style="color:rgba(255,255,255,0.5); margin-top:6px;">{feedback}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(_progress_html(score, "#34d399" if passed else "#f87171"), unsafe_allow_html=True)
    st.markdown(f"**{correct}/{total}** câu đúng")

    if completed:
        st.success("Chủ đề này đã được đánh dấu hoàn thành!")

    # Detail toggle
    with st.expander("Xem chi tiết từng câu", expanded=not passed):
        for r in results:
            ok = r["is_correct"]
            explanation = (r.get("explanation") or "").strip()
            icon = "" if ok else ""
            st.markdown(f"**{icon} {r['question']}**")
            st.caption(f"Bạn chọn: **{r['your_answer']}**")
            if not ok:
                st.caption(f"Đáp án đúng: **{r['correct_answer']}**")
            if explanation:
                st.markdown(
                    f'<div class="lp-hint">{html.escape(explanation)}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("---")
            
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Làm lại quiz", use_container_width=True):
            st.session_state.quiz_result = None
            st.session_state.quiz_answers = {}
            if topic:
                qdata = api_quiz_questions(topic["id"])
                st.session_state.quiz_questions = qdata
            st.session_state.page = "quiz"
            st.rerun()
    with c2:
        if not passed and ai_review_enabled:
            if st.button("Ôn bài với AI", use_container_width=True, type="secondary"):
                # A3: Build quiz_wrong_answers from results
                quiz_wrong_answers = []
                for r in results:
                    if not r.get("is_correct"):
                        quiz_wrong_answers.append({
                            "question": r.get("question", ""),
                            "user_answer": r.get("your_answer", ""),
                            "correct_answer": r.get("correct_answer", ""),
                            "skill_tag": r.get("skill_tag", "unknown"),
                            "explanation": r.get("explanation", "")
                        })
                
                # Set session state for chat to use
                st.session_state.quiz_review_mode = True
                st.session_state.quiz_wrong_answers = quiz_wrong_answers
                st.session_state.quiz_topic_id = topic.get("id") if topic else None
                st.session_state.messages = [
                    {"role": "user", "content": f"Tôi vừa làm quiz và sai {len(quiz_wrong_answers)} câu. Giúp tôi ôn lại các lỗi này."}
                ]
                st.session_state.page = "chat"
                st.rerun()
        else:
            if st.button("← Về chủ đề", use_container_width=True, key="quiz_result_back_to_topic_1"):
                st.session_state.quiz_result = None
                st.session_state.page = "topic"
                st.rerun()
    with c3:
        if st.button("← Về chủ đề" if passed or not ai_review_enabled else "Dashboard", use_container_width=True, key="quiz_result_back_to_topic_2"):
            st.session_state.quiz_result = None
            if passed or not ai_review_enabled:
                st.session_state.page = "topic"
            else:
                st.session_state.dashboard = None
                st.session_state.page = "dashboard"
            st.rerun()
    with c4:
        if st.button("Về Dashboard", type="primary", use_container_width=True):
            st.session_state.quiz_result = None
            st.session_state.dashboard = None
            st.session_state.page = "dashboard"
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: FREE CHAT
# ═══════════════════════════════════════════════════════════════
def page_chat():
    # Show sidebar with user info and logout
    _show_sidebar_user_info()
    
    # C2: Session history in sidebar
    with st.sidebar:
        st.divider()
        st.markdown("### Lịch sử chat")
        
        try:
            sessions = api_chat_get_sessions(limit=10)
            
            if sessions:
                # Group by topic
                by_topic = {}
                for s in sessions:
                    topic_name = s.get("topic_name", "Tổng quát")
                    by_topic.setdefault(topic_name, []).append(s)
                
                for topic_name, topic_sessions in by_topic.items():
                    with st.expander(f"{topic_name}", expanded=False):
                        for s in topic_sessions[:3]:  # Show last 3
                            session_id = s.get("session_id")
                            created = s.get("created_at", "")
                            msg_count = s.get("message_count", 0)
                            
                            # Format date
                            try:
                                from datetime import datetime
                                dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                                date_str = dt.strftime("%d/%m %H:%M")
                            except:
                                date_str = created[:16] if created else ""
                            
                            if st.button(f"📅 {date_str} ({msg_count} tin)", 
                                       key=f"session_{session_id}",
                                       use_container_width=True):
                                # Load session
                                st.session_state.chat_session_id = session_id
                                messages = api_chat_get_history(session_id)
                                if messages:
                                    # Convert to proper format
                                    formatted = []
                                    for m in messages:
                                        formatted.append({
                                            "role": m.get("role", "user"),
                                            "content": m.get("message", m.get("content", ""))
                                        })
                                    st.session_state.messages = formatted
                                st.rerun()
            else:
                st.caption("Chưa có lịch sử chat")
        except Exception as e:
            st.caption("Không tải được lịch sử")
    
    # Initialize session tracking
    if "chat_session_id" not in st.session_state:
        import uuid
        st.session_state.chat_session_id = str(uuid.uuid4())
    
    session_id = st.session_state.chat_session_id
    
    # A3: Check if entering from quiz review
    quiz_review_mode = st.session_state.get("quiz_review_mode", False)
    quiz_wrong_answers = st.session_state.get("quiz_wrong_answers", [])
    quiz_topic_id = st.session_state.get("quiz_topic_id")
    
    # Helper function to call API with quiz context
    def call_chat_api(msg):
        return api_chat(
            msg,
            session_id=session_id,
            quiz_wrong_answers=quiz_wrong_answers if quiz_review_mode else None,
            quiz_topic_id=quiz_topic_id if quiz_review_mode else None
        )
    
    # Clear quiz review mode after first use
    if quiz_review_mode and len(st.session_state.get("messages", [])) > 1:
        st.session_state.quiz_review_mode = False
        st.session_state.quiz_wrong_answers = []
        st.session_state.quiz_topic_id = None
    
    # AUTO-ACTIVATE CONTEXT: Load active topic on page entry
    if "chat_context_activated" not in st.session_state:
        try:
            # Get current user's active topic from backend
            profile_response = api_get_learning_context()
            logger.info(f"🔍 AUTO-ACTIVATE: profile_response = {profile_response}")
            
            if profile_response and profile_response.get("active_topic_id"):
                # Activate context in backend
                activate_response = api_activate_context(
                    profile_response["active_topic_id"],
                    profile_response.get("active_lesson_order")
                )
                if activate_response:
                    st.session_state.chat_context_activated = True
                    logger.info(f"✅ AUTO-ACTIVATE: Context activated for topic {profile_response['active_topic_id']}")
            else:
                # AUTO-RESOLVE: No active topic → use dashboard current/next topic
                logger.info("🔄 AUTO-RESOLVE: No active topic, trying dashboard current/next topic")
                dashboard_data = api_dashboard()
                
                if dashboard_data:
                    target_topic = dashboard_data.get("current_topic") or dashboard_data.get("next_topic")
                    
                    if target_topic:
                        topic_id = target_topic.get("id")
                        progress = target_topic.get("progress") or {}
                        lesson_order = progress.get("lesson_completed", 0) + 1
                        
                        activate_response = api_activate_context(topic_id, lesson_order)
                        if activate_response:
                            st.session_state.chat_context_activated = True
                            logger.info(f"✅ AUTO-RESOLVE: Context activated for topic {topic_id} lesson {lesson_order}")
                        else:
                            logger.warning("AUTO-RESOLVE: Failed to activate auto-resolved topic")
                            st.session_state.chat_context_activated = False
                    else:
                        logger.warning("⚠️ AUTO-RESOLVE: No topics available")
                        st.session_state.chat_context_activated = False
                else:
                    logger.warning("⚠️ AUTO-RESOLVE: Could not load dashboard")
                    st.session_state.chat_context_activated = False
        except Exception as e:
            logger.error(f"❌ AUTO-ACTIVATE: Failed to auto-activate context: {e}")
            st.session_state.chat_context_activated = False
    
    if st.button("← Quay lại"):
        prev = st.session_state.get("current_topic")
        st.session_state.page = "topic" if prev else "dashboard"
        # Clear AI tutor mode when leaving
        if "ai_tutor_mode" in st.session_state:
            del st.session_state.ai_tutor_mode
        if "error_context" in st.session_state:
            del st.session_state.error_context
        # Clear context activation flag so it re-activates on next entry
        if "chat_context_activated" in st.session_state:
            del st.session_state.chat_context_activated
        st.rerun()

    # Check if in AI Tutor mode
    ai_tutor_mode = st.session_state.get("ai_tutor_mode", False)
    error_ctx = st.session_state.get("error_context", {})
    
    # Load analytics context (always, for all chat modes)
    analytics_context = st.session_state.get("analytics_context")
    analytics_data = st.session_state.get("analytics_data")
    if analytics_context is None:
        try:
            analytics_data = api_analytics_dashboard()
            if analytics_data:
                # Phase 4: Add eligibility info
                eligibility_text = ""
                if analytics_data.get('level_eligible'):
                    current_level = analytics_data.get('eligibility_details', {}).get('current_level', 'A1')
                    eligibility_text = f"\n- **ĐỦ ĐIỀU KIỆN LÊN LEVEL {current_level}→{chr(ord(current_level[0])+1) if current_level[0] < 'C' else 'C'}{int(current_level[1])+1 if current_level[1] == '1' else '2'}!**"
                
                analytics_context = f"""**THỐNG KÊ NGƯỜI HỌC HIỆN TẠI:**
- Streak: {analytics_data.get('study_streak', 0)} ngày
- Tổng bài tập: {analytics_data.get('total_exercises', 0)}
- Tỷ lệ đúng: {int(analytics_data.get('correct_rate', 0) * 100)}%
- Điểm yếu: {', '.join(analytics_data.get('weak_skills', {}).keys()) or 'Không có'}{eligibility_text}
"""
                st.session_state.analytics_context = analytics_context
                st.session_state.analytics_data = analytics_data
            else:
                analytics_context = ""
                st.session_state.analytics_context = ""
        except Exception as e:
            analytics_context = ""
            st.session_state.analytics_context = ""
    
    if ai_tutor_mode:
        st.markdown("## AI Tutor - Ôn Lại Kiến Thức")
        st.info(f"AI đang giúp bạn khắc phục lỗi: **{error_ctx.get('skill_tag', 'unknown')}** (đã sai {error_ctx.get('frequency', 0)} lần)")
    else:
        st.markdown("## Chat với AI Tutor")
        
        # Check if user has active context
        has_active_context = st.session_state.get("chat_context_activated", False)
        
        # A1: Display learning context from backend (not just session_state)
        try:
            context_data = api_get_learning_context()
            if context_data and context_data.get("active_topic_id"):
                with st.expander("Bạn đang học gì?", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Level", context_data.get("current_level", "N/A"))
                    with col2:
                        lesson_info = f"{context_data.get('lesson_completed', 0)}/{context_data.get('total_lessons', '?')}"
                        st.metric("Bài hoàn thành", lesson_info)
                    with col3:
                        quiz_score = context_data.get("quiz_score")
                        if quiz_score is not None:
                            st.metric("Quiz", f"{quiz_score}%")
                        else:
                            st.metric("Quiz", "Chưa làm")
                    
                    # Topic and grammar
                    topic_name_vi = context_data.get("topic_name_vi", context_data.get("topic_name", ""))
                    st.markdown(f"**Chủ đề**: {topic_name_vi}")
                    
                    grammar = context_data.get("grammar_focus", [])
                    if grammar:
                        st.markdown(f"**Ngữ pháp**: {', '.join(grammar)}")
                    
                    # Current lesson
                    if context_data.get("lesson_title"):
                        st.markdown(f"**Bài học**: {context_data.get('lesson_title')}")
                    
                    # Quick actions
                    st.markdown("**Gợi ý câu hỏi**:")
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        if st.button("Giải thích bài", use_container_width=True, key="preset_explain"):
                            st.session_state.preset_input = "Giải thích chi tiết bài học này"
                            st.rerun()
                    with col_b:
                        if st.button("5 câu luyện", use_container_width=True, key="preset_practice"):
                            st.session_state.preset_input = "Cho tôi 5 câu hỏi luyện tập"
                            st.rerun()
                    with col_c:
                        # P1: Add "Phân tích tiến bộ"
                        if st.button("📈 Phân tích tiến bộ", use_container_width=True, key="preset_progress"):
                            st.session_state.preset_input = "Phân tích tiến bộ học tập của tôi và đưa ra gợi ý cải thiện"
                            st.rerun()
                    with col_d:
                        if st.button("Chat tự do", use_container_width=True, key="preset_free"):
                            st.session_state.preset_input = ""
            else:
                # No active context - show warning
                st.warning("**Bạn chưa chọn bài học nào.** Hãy vào Dashboard → chọn chủ đề → bấm 'Học tiếp' để AI Tutor biết bạn đang học gì.")
                
                with st.expander("Hướng dẫn", expanded=True):
                    st.markdown("""
                    **Để AI Tutor biết bạn đang học gì:**
                    1. Về [Dashboard](/?page=dashboard)
                    2. Chọn một chủ đề (topic)
                    3. Bấm nút **"Học tiếp"** hoặc chọn một bài học cụ thể
                    4. Quay lại Chat AI Tutor
                    
                    AI Tutor sẽ nhớ bài học bạn đang học và trả lời theo ngữ cảnh đó.
                    """)
                    
                    if st.button("Về Dashboard", use_container_width=True):
                        st.session_state.page = "dashboard"
                        st.rerun()
                
                topic = st.session_state.get("current_topic")
                if topic:
                    st.markdown(f"*Đang ôn luyện chủ đề: **{topic['name']}** – {topic['name_vi']}*")
        except Exception as e:
            # Fallback to session_state if API fails
            topic = st.session_state.get("current_topic")
            if topic:
                st.markdown(f"*Đang ôn luyện chủ đề: **{topic['name']}** – {topic['name_vi']}*")
    
    st.divider()
    
    # Display Analytics Dashboard on Chat page
    if analytics_data and not ai_tutor_mode:
        st.markdown("### Tiến độ học tập hiện tại")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Streak", f"{analytics_data.get('study_streak', 0)} ngày")
        with col2:
            st.metric("Bài tập", analytics_data.get('total_exercises', 0))
        with col3:
            correct_rate = analytics_data.get('correct_rate', 0)
            st.metric("Tỷ lệ đúng", f"{int(correct_rate * 100)}%")
        with col4:
            weak_count = len(analytics_data.get('weak_skills', {}))
            st.metric("Cần cải thiện", weak_count)
        
        # Show weak skills if any
        weak_skills = analytics_data.get('weak_skills', {})
        if weak_skills:
            st.markdown("**Các điểm yếu cần chú ý:**")
            weak_list = ", ".join([f"**{k}** ({int(v*100)}%)" for k, v in weak_skills.items()])
            st.warning(f"{weak_list}")
        
        st.divider()

    # Load messages from session_state or from database
    msgs = st.session_state.get("messages")
    if msgs is None:
        msgs = []
        # Try to load from database on first load
        db_history = api_chat_get_history(session_id)
        if db_history:
            # Convert DB format to Streamlit format
            for m in db_history:
                msgs.append({
                    "role": m.get("role", "user"),
                    "content": m.get("content", m.get("message", ""))  # Handle both keys
                })
            st.info(f"Đã tải {len(msgs)} message từ lịch sử")
        st.session_state.messages = msgs
    
    # P2.8: PROACTIVE - Auto send greeting when entering chat first time
    if len(msgs) == 0 and not ai_tutor_mode and "proactive_sent" not in st.session_state:
        # Check if user has active context - MUST verify from backend first
        try:
            context_data = api_get_learning_context()
            if context_data and context_data.get("active_topic_id"):
                # Wait a moment for DB sync after activation
                import time
                time.sleep(0.5)
                
                # Verify context one more time
                context_verify = api_get_learning_context()
                if context_verify and context_verify.get("active_topic_id"):
                    # Auto-send greeting with learning summary - BE SPECIFIC about current topic
                    topic_name = context_verify.get("topic_name_vi", context_verify.get("topic_name", ""))
                    lesson_title = context_verify.get("lesson_title", "")
                    
                    if topic_name and lesson_title:
                        proactive_msg = f"Chào bạn! Tôi đang học chủ đề '{topic_name}', bài '{lesson_title}'. Hãy tóm tắt nội dung bài học này và gợi ý cách luyện tập hiệu quả nhất."
                    elif topic_name:
                        proactive_msg = f"Chào bạn! Tôi đang học chủ đề '{topic_name}'. Hãy tóm tắt nội dung và gợi ý cách luyện tập."
                    else:
                        proactive_msg = "Chào bạn! Hãy tóm tắt bài học tôi đang học và gợi ý cách luyện tập hiệu quả nhất."
                    
                    # Add to messages
                    msgs.append({"role": "user", "content": proactive_msg})
                    st.session_state.messages = msgs
                    
                    # Get AI response
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(proactive_msg)
                    
                    with st.chat_message("assistant", avatar="🤖"):
                        with st.spinner("AI đang chuẩn bị bài học cho bạn..."):
                            ok, reply, metadata = call_chat_api(proactive_msg)
                        
                        if ok:
                            st.markdown(reply)
                            msgs.append({"role": "assistant", "content": reply})
                            st.session_state.messages = msgs
                            st.session_state.proactive_sent = True  # Mark as sent
                            
                            # Render suggested actions if any
                            suggested_actions = metadata.get("suggested_actions", [])
                            if suggested_actions:
                                st.markdown("---")
                                st.markdown("**💡 Bạn có thể:**")
                                cols = st.columns(len(suggested_actions))
                                for idx, action in enumerate(suggested_actions):
                                    with cols[idx]:
                                        if st.button(action.get("label", "Hành động"), key=f"proactive_action_{idx}", use_container_width=True):
                                            result = api_execute_action(action.get("type"), action.get("params", {}))
                                            if result and result.get("success"):
                                                st.success(result.get("message", ""))
                                                st.rerun()
                            st.rerun()
                else:
                    logger.warning("⚠️ PROACTIVE: Context verification failed, skipping proactive greeting")
        except Exception as e:
            # Silently fail proactive greeting if error
            logger.error(f"❌ PROACTIVE: Failed to send proactive greeting: {e}")
            pass
    
    # C1: Handle preset button input (if user clicked a preset button)
    if "preset_input" in st.session_state and st.session_state.preset_input:
        preset_msg = st.session_state.preset_input
        st.session_state.preset_input = ""  # Clear it
        
        # Add to messages
        msgs.append({"role": "user", "content": preset_msg})
        # Backend auto-saves (A4)
        
        # Get AI response immediately
        with st.chat_message("user", avatar="👤"):
            st.markdown(preset_msg)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI đang suy nghĩ..."):
                ok, reply, metadata = call_chat_api(preset_msg)
            
            if ok:
                st.markdown(reply)
                
                # Phase 3: Render suggested action buttons for preset as well
                suggested_actions = metadata.get("suggested_actions", [])
                if suggested_actions:
                    st.markdown("---")
                    st.markdown("**💡 Bạn có thể:**")
                    
                    cols = st.columns(len(suggested_actions))
                    for idx, action in enumerate(suggested_actions):
                        with cols[idx]:
                            action_type = action.get("type")
                            label = action.get("label", "Hành động")
                            params = action.get("params", {})
                            
                            if st.button(label, key=f"action_preset_{action_type}_{idx}", use_container_width=True):
                                result = api_execute_action(action_type, params)
                                
                                if result and result.get("success"):
                                    st.success(result.get("message", "Thành công!"))
                                    
                                    redirect = result.get("redirect_page")
                                    if redirect == "quiz":
                                        st.session_state.page = "quiz"
                                        st.session_state.current_topic = {"id": params.get("topic_id")}
                                        st.rerun()
                                    elif redirect == "lesson":
                                        st.session_state.page = "lesson"
                                        st.rerun()
                                    elif redirect == "level_up":
                                        st.session_state.page = "level_up_test"
                                        st.rerun()
                                    elif redirect is None and action_type == "offer_practice":
                                        count = params.get("count", 5)
                                        st.session_state.preset_input = f"Cho tôi {count} bài tập luyện tập"
                                        st.rerun()
                                else:
                                    st.error(result.get("message", "Có lỗi") if result else "Không thực hiện được")
                # Backend auto-saves (A4)
                msgs.append({"role": "assistant", "content": reply})
                st.session_state.messages = msgs
            else:
                st.error(reply)
        st.rerun()
    
    # Display existing messages
    for m in msgs:
        role = m.get("role", m.get("role") if isinstance(m, dict) else "user")
        avatar = "👤" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(m.get("content") if isinstance(m, dict) else m)

    # If first message in AI tutor mode, send it automatically
    if ai_tutor_mode and len(msgs) == 1 and msgs[0].get("role") == "user":
        # Display user's initial message (already displayed above)
        
        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI đang chuẩn bị bài ôn tập cho bạn..."):
                # Build context message for the first response
                user_initial = msgs[0].get("content")
                
                # Check if this is quiz review mode
                weak_skills = error_ctx.get("quiz_weak_skills", [])
                is_quiz_review = error_ctx.get("is_from_quiz", False)
                
                if error_ctx and is_quiz_review and weak_skills:
                    # Quiz review - build error context from weak_skills
                    quiz_errors = ""
                    for i, item in enumerate(weak_skills, 1):
                        quiz_errors += f"{i}. Câu: {item.get('question', '')}\n"
                        quiz_errors += f"   Trả lời: {item.get('user_answer', '')}\n"
                        quiz_errors += f"   Đúng: {item.get('correct_answer', '')}\n\n"
                    
                    context_msg = f"""[QUIZ REVIEW MODE - TUTOR BEHAVIOR REQUIRED]

**HỌC VIÊN VỪA SỬ DỤNG TÍNH NĂNG: ÔN BÀI VỚI AI**

**Chủ đề:** {error_ctx.get('skill_tag', 'unknown')}
**Số câu sai:** {error_ctx.get('frequency', 0)}

---

**CHI TIẾT CÁC CÂU SAI:**

{quiz_errors}

---

**HÀNH ĐỘNG (TRONG MỘT MESSAGE DUY NHẤT):**

1. **Phân loại lỗi:** Chỉ ra từng lỗi thuộc loại nào (từ vựng / ngữ pháp / hiểu lầm)
2. **Giải thích lý thuyết:** Giải thích các quy tắc liên quan (tiếng Việt)
3. **Ví dụ minh họa:** Cho 3-5 ví dụ cụ thể cho mỗi lỗi
4. **Bài tập mới:** Đưa ra 5 bài tập tương tự để luyện tập
5. **Hướng dẫn:** Nói học viên gửi đáp án

**ĐỊNH DẠNG:**
- **BẮT BUỘC TOÀN BỘ TRONG MỘT MESSAGE** (không cắt đứt)
- Xuống dòng rõ ràng, dùng emoji: 1️⃣ 2️⃣ ✅ ❌ 💡
- Bold cho tiêu đề, bullet/số cho danh sách

Bắt đầu ngay!"""
                    ok, reply, metadata = call_chat_api(context_msg)
                elif error_ctx:
                    # Regular AI tutor mode
                    context_msg = f"""[AI TUTOR MODE - ERROR REMEDIATION]

STUDENT MADE THIS MISTAKE {error_ctx.get('frequency', 0)} TIMES:

**Error Type:** {error_ctx.get('error_type', 'unknown').replace('_', ' ').upper()}
**Skill:** {error_ctx.get('skill_tag', 'unknown')}
**Question:** {error_ctx.get('question', '')}
**Student's Answer:** {error_ctx.get('user_answer', '')}
**Correct Answer:** {error_ctx.get('correct_answer', '')}

---

YOUR TASK: Create a complete remediation lesson IN ONE SEAMLESS MESSAGE:

**STRUCTURE (follow strictly):**

1️⃣ **Error Recognition** (2-3 sentences)
   - Identify what mistake the student made
   - Why it's wrong
   
2️⃣ **Theory Explanation** (in Vietnamese, 2-3 paragraphs)
   - Explain the grammar rule/concept clearly
   - Use simple language
   - Include formula if applicable
   
3️⃣ **Examples** (3-5 examples)
   - Show correct usage
   - Include both English and Vietnamese translation
   - Use ✅ for correct, ❌ for wrong examples
   
4️⃣ **Practice Exercises** (EXACTLY 5 exercises)
   - **CRITICAL:** Exercises must test THE SAME SKILL as the original error
   - Format: [sentence with blank] _____ (verb/word in parentheses)
   - Example format: "She _____ (watch) TV now."
   - **DO NOT** ask students to fill in time adverbs if the original error was about verb forms
   - Keep it simple and focused on the core error
   
5️⃣ **Instructions**
   - Ask student to submit their answers
   - You will grade them

**FORMATTING RULES:**
- Use clear line breaks (each point on new line)
- Use emoji: 1️⃣ 2️⃣ 3️⃣ ✅ ❌ 💡
- Bold for headings
- All in ONE message (no splitting)

Start now!"""
                    ok, reply, metadata = call_chat_api(context_msg)
                else:
                    # Regular chat - include analytics context
                    system_context = f"""Bạn là một giáo viên tiếng Anh chuyên nghiệp, am hiểu CEFR và các phương pháp dạy học hiệu quả.

{analytics_context}

HỖ TRỢ NGƯỜI HỌC CẢ VỀ:
- Giải thích văn phạm & từ vựng
- Luyện tập nói & viết
- Cải thiện những điểm yếu
- Khuyến khích & động viên

Luôn trả lời tính toán cá nhân hóa theo tiến độ và điểm yếu của người học.
"""
                    user_prompt = f"{system_context}\n\nNgười học: {user_initial}"
                    ok, reply, metadata = call_chat_api(user_prompt)
            
            if ok:
                st.markdown(reply)
                
                # Backend auto-saves both messages (A4)
                
                # Phase 3: Render suggested action buttons
                suggested_actions = metadata.get("suggested_actions", [])
                if suggested_actions:
                    st.markdown("---")
                    st.markdown("**💡 Bạn có thể:**")
                    
                    # Render up to 3 action buttons
                    cols = st.columns(len(suggested_actions))
                    for idx, action in enumerate(suggested_actions):
                        with cols[idx]:
                            action_type = action.get("type")
                            label = action.get("label", "Hành động")
                            params = action.get("params", {})
                            
                            if st.button(label, key=f"action_{action_type}_{idx}", use_container_width=True):
                                # Execute action
                                result = api_execute_action(action_type, params)
                                
                                if result and result.get("success"):
                                    st.success(result.get("message", "Thành công!"))
                                    
                                    # Handle redirect
                                    redirect = result.get("redirect_page")
                                    if redirect == "quiz":
                                        st.session_state.page = "quiz"
                                        st.session_state.current_topic = {
                                            "id": params.get("topic_id")
                                        }
                                        st.rerun()
                                    elif redirect == "lesson":
                                        st.session_state.page = "lesson"
                                        st.session_state.current_lesson = result.get("data", {})
                                        st.rerun()
                                    elif redirect == "level_up":
                                        st.session_state.page = "level_up_test"
                                        st.rerun()
                                    elif redirect is None:
                                        # Stay on chat, optionally auto-send follow-up
                                        if action_type == "offer_practice":
                                            # Auto-send request for practice
                                            count = params.get("count", 5)
                                            st.session_state.preset_input = f"Cho tôi {count} bài tập luyện tập"
                                            st.rerun()
                                else:
                                    st.error(result.get("message", "Có lỗi xảy ra") if result else "Không thực hiện được")
                
                # Add to session state
                msgs.append({"role": "assistant", "content": reply})
                st.session_state.messages = msgs
            else:
                st.error(reply)

    # Chat input - ALWAYS display (not in conditional)
    user_inp = st.chat_input("Nhập câu hỏi hoặc luyện tập tại đây...")
    if user_inp:
        msgs.append({"role": "user", "content": user_inp})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_inp)
        
        # Backend auto-saves (A4)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI đang suy nghĩ..."):
                # If in AI Tutor mode, include full context to maintain conversation
                if ai_tutor_mode and error_ctx:
                    # ✨ KEY FIX: Extract LATEST exercises from BEFORE the last user message
                    # Get the last user message index
                    last_user_idx = -1
                    for i in range(len(msgs) - 1, -1, -1):
                        if msgs[i].get("role") == "user":
                            last_user_idx = i
                            break
                    
                    # Search backwards from last user message to find latest assistant response with exercises
                    prev_exercises = ""
                    if last_user_idx > 0:
                        for i in range(last_user_idx - 1, -1, -1):
                            if msgs[i].get("role") == "assistant":
                                content = msgs[i].get("content", "")
                                if ("1️⃣" in content or "Bài tập" in content or "___" in content):
                                    # Extract full exercises up to "Hướng dẫn" or similar cutoff
                                    # Find the end of exercises section (usually before "Hướng dẫn", "Chấm", etc.)
                                    cutoff_idx = content.find("Hướng dẫn")
                                    if cutoff_idx == -1:
                                        cutoff_idx = content.find("Chấm")
                                    if cutoff_idx == -1:
                                        cutoff_idx = len(content)
                                    
                                    # Extract exercises section
                                    # Find the start of exercises (after "Bài tập")
                                    start_idx = content.find("Bài tập")
                                    if start_idx == -1:
                                        start_idx = 0
                                    
                                    exercises_section = content[start_idx:cutoff_idx]
                                    prev_exercises = exercises_section.strip()
                                    break
                    
                    # Check if this is from quiz weak_skills
                    weak_skills = error_ctx.get("quiz_weak_skills", [])
                    is_quiz_review = error_ctx.get("is_from_quiz", False)
                    
                    if is_quiz_review and weak_skills:
                        # Quiz review mode - focus on weak_skills
                        quiz_errors = ""
                        for i, item in enumerate(weak_skills, 1):
                            quiz_errors += f"{i}. Câu: {item.get('question', '')}\n"
                            quiz_errors += f"   Trả lời: {item.get('user_answer', '')}\n"
                            quiz_errors += f"   Đúng: {item.get('correct_answer', '')}\n\n"
                        
                        context_msg = f"""[QUIZ REVIEW MODE - TUTOR BEHAVIOR REQUIRED]

**HỌC VIÊN VỪA SỬ DỤNG TÍNH NĂNG: ÔN BÀI VỚI AI**

**Chủ đề:** {error_ctx.get('skill_tag', 'unknown')}
**Số câu sai:** {error_ctx.get('frequency', 0)}

---

**CHI TIẾT CÁC CÂU SAI:**

{quiz_errors}

---

**HÀNH ĐỘNG (TRONG MỘT MESSAGE DUY NHẤT):**

1. **Phân loại lỗi:** Chỉ ra từng lỗi thuộc loại nào (từ vựng / ngữ pháp / hiểu lầm)
2. **Giải thích lý thuyết:** Giải thích các quy tắc liên quan (tiếng Việt)
3. **Ví dụ minh họa:** Cho 3-5 ví dụ cụ thể cho mỗi lỗi
4. **Bài tập mới:** Đưa ra 5 bài tập tương tự để luyện tập
5. **Hướng dẫn:** Nói học viên gửi đáp án

**ĐỊNH DẠNG:**
- **BẮT BUỘC TOÀN BỘ TRONG MỘT MESSAGE** (không cắt đứt)
- Xuống dòng rõ ràng, dùng emoji: 1️⃣ 2️⃣ ✅ ❌ 💡
- Bold cho tiêu đề, bullet/số cho danh sách

Bắt đầu ngay!"""
                    else:
                        # Regular AI tutor mode (non-quiz)
                        context_msg = f"""[AI TUTOR MODE - GRADING STUDENT ANSWERS]

**ORIGINAL ERROR CONTEXT:**
- Error Type: {error_ctx.get('error_type', 'unknown').replace('_', ' ').upper()}
- Times Wrong: {error_ctx.get('frequency', 0)}
- Skill: {error_ctx.get('skill_tag', 'unknown')}

---

**EXERCISES FROM PREVIOUS MESSAGE:**

{prev_exercises if prev_exercises else "[No exercises found - grade based on logic]"}

---

**STUDENT'S SUBMISSION:** 
{user_inp}

---

**YOUR TASK: Grade the student's answers**

**GRADING RULES:**
1. Match student's answer to the exercise number (1️⃣ → 1, 2️⃣ → 2, etc.)
2. Check if the verb form/grammar is correct
3. **IMPORTANT:** If exercises asked for verb forms, only check verb forms - ignore time adverbs
4. Be strict but fair

**OUTPUT FORMAT:**

✅ **Grading Results**

1️⃣ [student answer] – ✅/❌ 
   Reason: [brief explanation]

2️⃣ [student answer] – ✅/❌ 
   Reason: [brief explanation]

(Continue for all 5)

---

🌟 **Feedback:** [Praise + constructive feedback]

✏️ **New Practice** (5 new exercises - same format as before)

1️⃣ [exercise 1]
2️⃣ [exercise 2]
3️⃣ [exercise 3]
4️⃣ [exercise 4]
5️⃣ [exercise 5]

📮 **Instructions:** Submit your answers to continue practice.

Start grading now!"""
                    
                    ok, reply, metadata = call_chat_api(context_msg)
                else:
                    # Regular chat - include analytics context
                    system_context = f"""Bạn là một giáo viên tiếng Anh chuyên nghiệp, am hiểu CEFR và các phương pháp dạy học hiệu quả.

{analytics_context}

HỖ TRỢ NGƯỜI HỌC CẢ VỀ:
- Giải thích văn phạm & từ vựng
- Luyện tập nói & viết
- Cải thiện những điểm yếu
- Khuyến khích & động viên

Luôn trả lời tính toán cá nhân hóa theo tiến độ và điểm yếu của người học.
"""
                    user_prompt = f"{system_context}\n\nNgười học: {user_inp}"
                    ok, reply, metadata = call_chat_api(user_prompt)
            
            if ok:
                st.markdown(reply)
                
                # Backend auto-saves (A4)
                
                # Phase 3: Render suggested action buttons
                # Filter out "continue chat" action when already in chat
                suggested_actions = metadata.get("suggested_actions", [])
                suggested_actions = [a for a in suggested_actions if a.get("label") != "Tiếp tục chat"]
                
                if suggested_actions:
                    st.markdown("---")
                    st.markdown("**💡 Bạn có thể:**")
                    
                    # Render up to 3 action buttons
                    cols = st.columns(len(suggested_actions))
                    for idx, action in enumerate(suggested_actions):
                        with cols[idx]:
                            action_type = action.get("type")
                            label = action.get("label", "Hành động")
                            params = action.get("params", {})
                            
                            if st.button(label, key=f"action_user_{action_type}_{idx}", use_container_width=True):
                                # Execute action
                                result = api_execute_action(action_type, params)
                                
                                if result and result.get("success"):
                                    st.success(result.get("message", "Thành công!"))
                                    
                                    # Handle redirect
                                    redirect = result.get("redirect_page")
                                    if redirect == "quiz":
                                        st.session_state.page = "quiz"
                                        st.session_state.current_topic = {
                                            "id": params.get("topic_id")
                                        }
                                        st.rerun()
                                    elif redirect == "lesson":
                                        st.session_state.page = "lesson"
                                        st.session_state.current_lesson = result.get("data", {})
                                        st.rerun()
                                    elif redirect == "level_up":
                                        st.session_state.page = "level_up_test"
                                        st.rerun()
                                    elif redirect is None:
                                        # Stay on chat, optionally auto-send follow-up
                                        if action_type == "offer_practice":
                                            # Auto-send request for practice
                                            count = params.get("count", 5)
                                            st.session_state.preset_input = f"Cho tôi {count} bài tập luyện tập"
                                            st.rerun()
                                else:
                                    st.error(result.get("message", "Có lỗi xảy ra") if result else "Không thực hiện được")
                
                msgs.append({"role": "assistant", "content": reply})
            else:
                st.error(f"❌ Lỗi API: {reply}")
                st.caption("Thử reload trang hoặc gửi lại tin nhắn")
        
        st.session_state.messages = msgs


# ═══════════════════════════════════════════════════════════════
# PAGE: LEVEL-UP TEST
# ═══════════════════════════════════════════════════════════════
def page_levelup():
    # Show sidebar with user info and logout
    _show_sidebar_user_info()
    
    level = current_level()

    if st.button("← Về Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    _next = {"A1":"A2","A2":"B1","B1":"B2","B2":"C1","C1":"C2"}.get(level,"C2")
    st.markdown(f"## 🏆 Level-Up Test: {level} → {_next}")
    st.markdown(f"Điểm ≥ **75%** để nâng lên level tiếp theo.")
    st.divider()

    questions = st.session_state.get("levelup_questions", [])
    if not questions:
        if st.button("📥 Tải câu hỏi Level-Up"):
            with st.spinner("Đang tải..."):
                questions = api_level_questions(level)
            st.session_state.levelup_questions = questions
            st.rerun()
        return

    with st.form("levelup_form"):
        answers = {}
        for i, q in enumerate(questions, 1):
            qid = q["question_id"]
            opts = q.get("options", [])
            st.markdown(f"**Câu {i}:** {q['question']}")
            if opts:
                answers[qid] = st.radio("Chọn đáp án", opts, key=f"lu_{qid}", label_visibility="collapsed")
            else:
                answers[qid] = st.text_input("", key=f"lu_{qid}")
            st.markdown("---")

        sub = st.form_submit_button("📤 Nộp bài", type="primary", use_container_width=True)

    if sub:
        with st.spinner("Đang chấm điểm..."):
            result = api_submit_levelup(level, answers)
        if result:
            new_level = result.get("new_level", level)
            score = result.get("score", 0)
            passed = result.get("passed", False)
            if passed and new_level != level:
                st.success(f"🎉 Xuất sắc! Bạn nâng cấp từ **{level}** lên **{new_level}**! (Điểm: {score}%)")
                st.balloons()
                _fetch_profile()
                st.session_state.dashboard = None
            else:
                st.warning(f"📚 Điểm {score}% – Chưa đủ để nâng cấp. Tiếp tục ôn luyện nhé!")
                st.info(result.get("recommendation", ""))
            st.session_state.levelup_questions = []
            st.session_state.test_answers = {}
            if st.button("Về Dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ═══════════════════════════════════════════════════════════════
def page_analytics():
    """Trang thống kê chi tiết"""
    _show_sidebar_user_info()
    
    st.markdown("## Phân Tích Học Tập")
    st.markdown("Thống kê chi tiết về tiến trình học và kỹ năng")
    st.divider()
    
    # Load analytics data
    with st.spinner("Đang tải thống kê..."):
        dashboard_analytics = api_analytics_dashboard()
        skill_breakdown = api_analytics_skills()
        due_reviews = api_analytics_reviews()
        timeline = api_analytics_timeline(30)
    
    if not dashboard_analytics:
        st.error("Không tải được dữ liệu analytics")
        return
    
    # Study Streak
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _stat(dashboard_analytics.get("study_streak", 0), "Streak (ngày)")
    with col2:
        _stat(dashboard_analytics.get("total_exercises", 0), "Bài tập")
    with col3:
        correct_rate = dashboard_analytics.get("correct_rate", 0)
        _stat(f"{correct_rate*100:.0f}%", "Tỷ lệ đúng")
    with col4:
        weak_count = len(dashboard_analytics.get("weak_skills", {}))
        _stat(weak_count, "Cần cải thiện")
    
    st.markdown("")
    
    # Weak Skills Section
    weak_skills = dashboard_analytics.get("weak_skills", {})
    if weak_skills:
        st.markdown('<div class="lp-card">', unsafe_allow_html=True)
        st.markdown("### Kỹ năng cần cải thiện (< 60% đúng)")
        
        for skill, accuracy in sorted(weak_skills.items(), key=lambda x: x[1]):
            skill_name = skill.replace("_", " ").title()
            pct = accuracy * 100
            color = "#f87171" if pct < 40 else "#fbbf24"
            
            st.markdown(f"**{skill_name}**: {pct:.0f}%")
            st.markdown(_progress_html(pct, color), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("🎉 Không có kỹ năng yếu! Bạn làm rất tốt!")
    
    st.markdown("")
    
    # Skill Breakdown
    if skill_breakdown:
        st.markdown('<div class="lp-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Phân tích chi tiết theo kỹ năng")
        
        for skill, data in sorted(skill_breakdown.items(), key=lambda x: x[1]["accuracy"], reverse=True):
            skill_name = skill.replace("_", " ").title()
            acc = data["accuracy"] * 100
            correct = data["correct"]
            total = data["total"]
            
            # Color based on accuracy
            if acc >= 80:
                color = "#34d399"
                emoji = ""
            elif acc >= 60:
                color = "#60a5fa"
                emoji = ""
            elif acc >= 40:
                color = "#fbbf24"
                emoji = ""
            else:
                color = "#f87171"
                emoji = ""
            
            st.markdown(f"{emoji} **{skill_name}**: {correct}/{total} đúng ({acc:.0f}%)")
            st.markdown(_progress_html(acc, color), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    
    # NEW: Chat Learning Activities Section
    st.markdown('<div class="lp-card" style="border-color:#60a5fa;">', unsafe_allow_html=True)
    st.markdown("### 💬 Học qua AI Tutor Chat")
    st.markdown("Hoạt động học tập từ chat với AI (30 ngày gần đây)")
    
    # Call API to get chat activities
    chat_activities_data = api_chat_activities(30)
    
    if chat_activities_data and chat_activities_data.get("total", 0) > 0:
        summary = chat_activities_data.get("summary", {})
        activities = chat_activities_data.get("activities", [])
        
        # Show summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            lesson_count = summary.get("lesson", {}).get("count", 0)
            st.metric("📖 Bài học", lesson_count)
        with col2:
            practice_count = summary.get("practice", {}).get("count", 0)
            practice_score = summary.get("practice", {}).get("avg_score")
            st.metric("Luyện tập", practice_count, 
                     delta=f"{practice_score:.0f}%" if practice_score else None)
        with col3:
            quiz_count = summary.get("quiz", {}).get("count", 0)
            quiz_score = summary.get("quiz", {}).get("avg_score")
            st.metric("📝 Quiz", quiz_count,
                     delta=f"{quiz_score:.0f}%" if quiz_score else None)
        with col4:
            vocab_count = summary.get("vocabulary", {}).get("count", 0)
            st.metric("📚 Từ vựng", vocab_count)
        
        st.markdown("")
        
        # Show recent activities (top 10)
        if activities:
            st.markdown("**Hoạt động gần đây:**")
            for activity in activities[:10]:
                activity_type = activity["type"]
                title = activity["title"]
                score = activity.get("score")
                created_at = activity["created_at"]
                custom_topic = activity.get("custom_topic")
                
                # Icon based on type
                icon_map = {
                    "lesson": "",
                    "practice": "",
                    "quiz": "",
                    "vocabulary": ""
                }
                icon = icon_map.get(activity_type, "📌")
                
                # Format display
                score_text = f" - Điểm: {score:.0f}%" if score is not None else ""
                topic_text = f" ({custom_topic})" if custom_topic else ""
                date_str = created_at[:10]  # Get date part
                
                st.markdown(f"{icon} **{title}**{topic_text}{score_text} - _{date_str}_")
            
            if len(activities) > 10:
                st.markdown(f"_... và {len(activities) - 10} hoạt động khác_")
    else:
        st.info("Chưa có hoạt động học qua AI Tutor chat. Hãy thử chat với AI để học thêm!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    
    # Due Reviews
    if due_reviews:
        st.markdown('<div class="lp-card" style="border-color:#fbbf24;">', unsafe_allow_html=True)
        st.markdown(f"### 📚 Chủ đề cần ôn tập ({len(due_reviews)})")
        st.markdown("Các chủ đề sau đến hạn ôn tập theo spaced repetition:")
        
        for review in due_reviews:
            topic_id = review["topic_id"]
            last_score = review.get("last_score", 0)
            weak_skills_review = review.get("weak_skills", {})
            
            st.markdown(f"- **Topic ID**: {topic_id[:8]}... | Điểm gần nhất: {last_score:.0f}%")
            if weak_skills_review:
                skills_text = ", ".join(weak_skills_review.keys())
                st.markdown(f"  Kỹ năng yếu: {skills_text}")
            
            if st.button(f"Ôn tập ngay", key=f"review_{topic_id}"):
                # Navigate to topic
                st.session_state.page = "topic"
                detail = api_topic_detail(topic_id)
                if detail:
                    st.session_state.current_topic = detail
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👍 Không có chủ đề nào cần ôn tập hôm nay!")
    
    st.markdown("")
    
    # Timeline Chart
    if timeline:
        st.markdown('<div class="lp-card">', unsafe_allow_html=True)
        st.markdown("### 📅 Timeline học tập (30 ngày gần đây)")
        
        # Prepare data for chart
        import pandas as pd
        dates = [t["date"] for t in timeline]
        scores = [t["score"] for t in timeline]
        topics_completed = [t["topics_completed"] for t in timeline]
        
        df = pd.DataFrame({
            "Ngày": dates,
            "Điểm TB": scores,
            "Chủ đề hoàn thành": topics_completed
        })
        
        st.line_chart(df.set_index("Ngày"))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Back button
    st.divider()
    if st.button("← Về Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
def _sidebar():
    with st.sidebar:
        if st.session_state.get("access_token"):
            user = st.session_state.user or {}
            profile = st.session_state.profile or {}
            level = profile.get("current_level", "A1")
            lcolor = LEVEL_COLORS.get(level, "#6ee7b7")

            st.markdown(f"""
            <div style="text-align:center; padding:1rem 0.5rem;">
                <div style="font-size:2.5rem;">👤</div>
                <div style="font-weight:700; font-size:1rem;">{user.get('full_name','Học viên')}</div>
                <div style="font-size:0.82rem; color:rgba(255,255,255,0.45);">{user.get('email','')}</div>
                <div style="margin-top:8px;">{_badge(f'CEFR {level}', lcolor)}</div>
            </div>
            """, unsafe_allow_html=True)
            st.divider()

            # Navigation
            nav_items = [
                ("🏠", "Dashboard", "dashboard"),
                ("📚", "Chủ đề học", "topics"),
                ("💬", "Chat AI Tutor", "chat"),
            ]
            for icon, label, pg in nav_items:
                active = st.session_state.page == pg
                if st.button(
                    f"{icon} {label}",
                    use_container_width=True,
                    key=f"nav_{pg}",
                    type="primary" if active else "secondary",
                ):
                    st.session_state.dashboard = None
                    st.session_state.page = pg
                    st.rerun()

            st.divider()

            # Placement re-test
            if st.button(" Làm lại Placement Test", use_container_width=True):
                qs = api_get_placement_q()
                st.session_state.placement_questions = qs
                st.session_state.test_answers = {}
                st.session_state.page = "placement"
                st.rerun()

            st.divider()
            if st.button("Đăng xuất", use_container_width=True):
                _logout()  # Already includes st.rerun()

        else:
            st.markdown("### 🎓 AI Language Tutor")
            st.markdown("Đăng nhập để bắt đầu học")

            # Backend status
            try:
                with httpx.Client(timeout=3) as c:
                    r = c.get(_url("/health"))
                if r.status_code == 200:
                    st.success("Backend online")
                else:
                    st.error("Backend lỗi")
            except Exception:
                st.error("Không kết nối được backend")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    _init()

    st.set_page_config(
        page_title="AI Language Tutor",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    _inject_css()
    # _sidebar()  ← REMOVED: Using _show_sidebar_user_info() in each page instead

    # Handle Google OAuth token from URL
    qp = st.query_params
    # IMPORTANT: Don't auto-login if user just logged out
    if "token" in qp and not st.session_state.access_token and not st.session_state.get("just_logged_out", False):
        st.session_state.access_token = qp["token"]
        _fetch_profile()
        
        # Check if onboarding is needed
        if "onboarding" in qp and qp["onboarding"] == "true":
            st.session_state.page = "onboarding"
        else:
            st.session_state.page = "dashboard"
        
        st.success("Đăng nhập Google thành công!")
        st.rerun()

    # ── CHECK LOGOUT FIRST ──────────────────────────────────────────
    # If access_token is None, always go to auth page (even if already logged in)
    if not st.session_state.access_token:
        st.session_state.page = "auth"
        # Reset just_logged_out flag when showing auth page
        st.session_state.just_logged_out = False
        page_auth()
        return
    
    # Ensure user is loaded when we have token but no user
    # BUT NOT during logout!
    if st.session_state.access_token and not st.session_state.user and not st.session_state.get("is_logging_out"):
        _fetch_profile()
        if not st.session_state.user:  # Still no user after fetch
            st.error("Could not load user profile. Please login again.")
            st.session_state.access_token = None
            st.rerun()

    page = st.session_state.page

    if page == "onboarding":
        page_onboarding()
    elif page == "placement":
        page_placement()
    elif page == "dashboard":
        page_dashboard()
    elif page == "analytics":  # P1: Add analytics route
        page_analytics()
    elif page == "topics":
        page_topics()
    elif page == "topic":
        page_topic()
    elif page == "lesson":
        page_lesson()
    elif page == "quiz":
        page_quiz()
    elif page == "quiz_result":
        page_quiz_result()
    elif page == "chat":
        page_chat()
    elif page == "levelup":
        page_levelup()
    else:
        # Default: go to dashboard
        st.session_state.page = "dashboard"
        st.rerun()


if __name__ == "__main__":
    main()
