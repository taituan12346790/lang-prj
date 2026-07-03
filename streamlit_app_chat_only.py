"""
AI Language Tutor - Redesigned Frontend with ChatGPT-like UI

Backend:  python -m uvicorn app.main:app --reload
Frontend: streamlit run streamlit_app_redesigned.py
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import httpx
import streamlit as st

# ============================================================================
# Configuration
# ============================================================================
DEFAULT_API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
DATA_DIR = Path(__file__).resolve().parent / ".streamlit_data"

LANGUAGES = {
    "en": "English", "vi": "Tieng Viet", "zh": "Chinese", "ja": "Japanese",
    "ko": "Korean", "fr": "French", "es": "Spanish", "pt": "Portuguese",
    "de": "German", "ru": "Russian",
}

TARGET_LANG_OPTIONS = {
    "English": "English", "Vietnamese": "Vietnamese", "Chinese": "Chinese",
    "Japanese": "Japanese", "Korean": "Korean", "French": "French",
    "Spanish": "Spanish", "Portuguese": "Portuguese", "German": "German",
    "Russian": "Russian",
}

CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
LEVEL_NEXT = {"A1": "A2", "A2": "B1", "B1": "B2", "B2": "C1", "C1": "C2"}


# ============================================================================
# Session Data Management
# ============================================================================
def _user_id() -> Optional[str]:
    user = st.session_state.get("user") or {}
    uid = user.get("id")
    return str(uid) if uid else None


def _data_file() -> Optional[Path]:
    uid = _user_id()
    if not uid:
        return None
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR / f"{uid}.json"


def _default_user_data() -> dict[str, Any]:
    return {
        "onboarding_done": False,
        "placement_completed": False,
        "placement_level": None,
        "sessions": [],
        "current_session_id": None,
    }


def load_user_data() -> dict[str, Any]:
    path = _data_file()
    if not path or not path.exists():
        return _default_user_data()
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        base = _default_user_data()
        base.update(data)
        return base
    except Exception:
        return _default_user_data()


def save_user_data(data: dict[str, Any]) -> None:
    path = _data_file()
    if not path:
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def persist_messages() -> None:
    uid = _user_id()
    if not uid or "messages" not in st.session_state:
        return
    data = load_user_data()
    sid = st.session_state.get("current_session_id")
    if not sid:
        sid = str(uuid.uuid4())
        st.session_state.current_session_id = sid

    sessions: list = data.get("sessions", [])
    title = "New Conversation"
    for m in st.session_state.messages:
        if m.get("role") == "user":
            title = (m.get("content") or "")[:50]
            if len(m.get("content", "")) > 50:
                title += "..."
            break

    entry = {
        "id": sid,
        "title": title,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "messages": st.session_state.messages,
    }
    found = False
    for i, s in enumerate(sessions):
        if s.get("id") == sid:
            sessions[i] = entry
            found = True
            break
    if not found:
        sessions.insert(0, entry)
    data["sessions"] = sessions[:50]
    data["current_session_id"] = sid
    save_user_data(data)


def load_session(session_id: str) -> None:
    data = load_user_data()
    for s in data.get("sessions", []):
        if s.get("id") == session_id:
            st.session_state.current_session_id = session_id
            st.session_state.messages = list(s.get("messages", []))
            data["current_session_id"] = session_id
            save_user_data(data)
            return


def new_chat_session() -> None:
    st.session_state.current_session_id = str(uuid.uuid4())
    st.session_state.messages = []
    data = load_user_data()
    data["current_session_id"] = st.session_state.current_session_id
    save_user_data(data)


def total_user_messages() -> int:
    data = load_user_data()
    return sum(
        len([m for m in s.get("messages", []) if m.get("role") == "user"])
        for s in data.get("sessions", [])
    )


def needs_placement_test() -> bool:
    data = load_user_data()
    if data.get("placement_completed"):
        return False
    profile = st.session_state.get("profile") or {}
    if float(profile.get("placement_score") or 0) > 0:
        return False
    return True


def current_level() -> str:
    data = load_user_data()
    if data.get("placement_level"):
        return data["placement_level"]
    profile = st.session_state.get("profile") or {}
    return profile.get("current_level") or "A1"


def ready_for_level_up() -> bool:
    level = current_level()
    if level == "C2":
        return False
    profile = st.session_state.get("profile") or {}
    sessions = int(profile.get("total_sessions") or 0)
    placement = float(profile.get("placement_score") or 0)
    msg_count = total_user_messages()
    
    for m in reversed(st.session_state.get("messages", [])):
        if m.get("role") == "assistant" and m.get("metadata"):
            meta = m["metadata"]
            if meta.get("success") or meta.get("intent") in ("translate", "grammar", "exercise"):
                return sessions >= 3 or msg_count >= 5 or placement >= 60
    
    return sessions >= 5 or msg_count >= 10 or placement >= 70


# ============================================================================
# Session State Initialization
# ============================================================================
def _init_session() -> None:
    defaults = {
        "access_token": None,
        "user": None,
        "profile": None,
        "messages": [],
        "api_base": DEFAULT_API_BASE,
        "current_session_id": None,
        "app_page": "auth",
        "test_answers": {},
        "placement_questions": [],
        "levelup_questions": [],
        "chat_target_lang": "",
        "chat_explain_in": "vi",
        "chat_difficulty": "",
        "chat_temperature": 0.7,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================================
# HTTP Helpers & API Calls
# ============================================================================
def _headers() -> dict[str, str]:
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    token = st.session_state.get("access_token")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _api_url(path: str) -> str:
    return f"{st.session_state.api_base.rstrip('/')}{path}"


def _parse_error(resp: httpx.Response) -> str:
    try:
        data = resp.json()
        if isinstance(data, dict):
            if isinstance(data.get("detail"), list):
                return "; ".join(str(x.get("msg", x)) for x in data["detail"])
            return data.get("error") or data.get("detail") or resp.text
    except Exception:
        pass
    return resp.text or f"HTTP {resp.status_code}"


def api_register(email: str, password: str, full_name: str, native_lang: str, target_lang: str) -> tuple[bool, str]:
    payload = {
        "email": email.strip().lower(),
        "password": password,
        "full_name": full_name.strip(),
        "native_language": native_lang,
        "target_language": target_lang,
    }
    try:
        with httpx.Client(timeout=30.0) as client:
            r = client.post(_api_url("/api/auth/register"), json=payload, headers=_headers())
        if r.status_code == 201:
            return True, "registered"
        return False, _parse_error(r)
    except httpx.ConnectError:
        return False, "Cannot connect to backend."
    except Exception as e:
        return False, str(e)


def api_login(email: str, password: str) -> tuple[bool, str]:
    payload = {"email": email.strip().lower(), "password": password}
    try:
        with httpx.Client(timeout=30.0) as client:
            r = client.post(_api_url("/api/auth/login"), json=payload, headers=_headers())
        if r.status_code == 200:
            data = r.json()
            st.session_state.access_token = data["access_token"]
            st.session_state.user = data.get("user", {})
            api_fetch_profile()
            _after_auth_load_state()
            name = data.get("user", {}).get("full_name") or data.get("user", {}).get("email", "")
            return True, f"Welcome {name}!"
        return False, _parse_error(r)
    except httpx.ConnectError:
        return False, "Cannot connect to backend."
    except Exception as e:
        return False, str(e)


def api_fetch_profile() -> None:
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.get(_api_url("/api/profile/"), headers=_headers())
        if r.status_code == 200:
            st.session_state.profile = r.json()
    except Exception:
        st.session_state.profile = None


def _after_auth_load_state() -> None:
    data = load_user_data()
    cid = data.get("current_session_id")
    if cid:
        load_session(cid)
    else:
        new_chat_session()


def api_chat(user_input: str, target_lang: Optional[str], explain_in: str, difficulty: Optional[str], temperature: float) -> tuple[bool, str, dict]:
    payload: dict[str, Any] = {
        "user_input": user_input,
        "explain_in": explain_in,
        "temperature": temperature,
    }
    if target_lang:
        payload["target_lang"] = target_lang
    if difficulty:
        payload["difficulty"] = difficulty
    try:
        with httpx.Client(timeout=120.0) as client:
            r = client.post(_api_url("/api/chat/"), json=payload, headers=_headers())
        if r.status_code == 200:
            data = r.json()
            text = data.get("response", "")
            if not data.get("success", True) and data.get("error"):
                text = f"[Error] {data['error']}\n\n{text}".strip()
            return True, text or "(No response)", data.get("metadata", {})
        if r.status_code == 401:
            _logout()
            return False, "Session expired - please login again.", {}
        return False, _parse_error(r), {}
    except httpx.TimeoutException:
        return False, "Request timeout. Try a shorter message.", {}
    except httpx.ConnectError:
        return False, "Backend connection lost.", {}
    except Exception as e:
        return False, str(e), {}


def api_get_placement_questions() -> tuple[bool, list, str]:
    try:
        with httpx.Client(timeout=20.0) as client:
            r = client.get(_api_url("/api/test/placement/questions"))
        if r.status_code == 200:
            return True, r.json().get("questions", []), ""
        return False, [], _parse_error(r)
    except Exception as e:
        return False, [], str(e)


def api_submit_placement(answers: dict[str, str]) -> tuple[bool, dict, str]:
    try:
        with httpx.Client(timeout=30.0) as client:
            r = client.post(_api_url("/api/test/placement"), json={"answers": answers}, headers=_headers())
        if r.status_code == 200:
            return True, r.json(), ""
        return False, {}, _parse_error(r)
    except Exception as e:
        return False, {}, str(e)


def api_get_level_questions(level: str) -> tuple[bool, list, str]:
    try:
        with httpx.Client(timeout=20.0) as client:
            r = client.get(_api_url(f"/api/test/level/{level}/questions"), headers=_headers())
        if r.status_code == 200:
            return True, r.json().get("questions", []), ""
        return False, [], _parse_error(r)
    except Exception as e:
        return False, [], str(e)


def api_submit_level_up(level: str, test_type: str, answers: dict[str, str]) -> tuple[bool, dict, str]:
    payload = {"test_type": test_type, "current_level": level, "num_questions": len(answers), "answers": answers}
    try:
        with httpx.Client(timeout=30.0) as client:
            r = client.post(_api_url("/api/test/level-up"), json=payload, headers=_headers())
        if r.status_code == 200:
            return True, r.json(), ""
        return False, {}, _parse_error(r)
    except Exception as e:
        return False, {}, str(e)


def api_health() -> tuple[bool, str]:
    try:
        with httpx.Client(timeout=5.0) as client:
            r = client.get(_api_url("/health"))
        if r.status_code == 200:
            return True, f"OK ({r.json().get('environment', '?')})"
        return False, _parse_error(r)
    except Exception:
        return False, "No response"


def _logout() -> None:
    st.session_state.access_token = None
    st.session_state.user = None
    st.session_state.profile = None
    st.session_state.messages = []
    st.session_state.current_session_id = None
    st.session_state.app_page = "auth"


# ============================================================================
# UI Pages - Auth
# ============================================================================
def _render_auth_page() -> None:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Email/Password")
        auth_mode = st.radio("Choose:", ["Login", "Register"], horizontal=True, label_visibility="collapsed")
        
        if auth_mode == "Login":
            email = st.text_input("Email", key="login_email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login", type="primary", use_container_width=True):
                if email and password:
                    ok, msg = api_login(email, password)
                    if ok:
                        st.session_state.app_page = "chat"
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter email and password")
        
        else:  # Register
            reg_email = st.text_input("Email", key="reg_email", placeholder="your@email.com")
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_pw = st.text_input("Password (8+ chars)", type="password", key="reg_pw")
            reg_pw2 = st.text_input("Confirm Password", type="password", key="reg_pw2")
            
            lang_keys = list(LANGUAGES.keys())
            col_a, col_b = st.columns(2)
            with col_a:
                native = st.selectbox("Native Language", lang_keys, format_func=lambda k: LANGUAGES[k], index=lang_keys.index("vi"))
            with col_b:
                targets = [k for k in lang_keys if k != native]
                target = st.selectbox("Learning Language", targets, format_func=lambda k: LANGUAGES[k], index=targets.index("en") if "en" in targets else 0)
            
            if st.button("Register", type="primary", use_container_width=True):
                if not reg_email or not reg_name:
                    st.warning("Please fill in all fields")
                elif len(reg_pw) < 8:
                    st.warning("Password must be 8+ characters")
                elif reg_pw != reg_pw2:
                    st.warning("Passwords don't match")
                else:
                    ok, msg = api_register(reg_email, reg_pw, reg_name, native, target)
                    if ok:
                        ok2, msg2 = api_login(reg_email, reg_pw)
                        if ok2:
                            data = load_user_data()
                            data["onboarding_done"] = False
                            data["placement_completed"] = False
                            save_user_data(data)
                            st.session_state.app_page = "placement"
                            st.success("Registration successful! Starting placement test...")
                            st.rerun()
                        else:
                            st.error(f"Registration OK but login failed: {msg2}")
                    else:
                        st.error(msg)
    
    with col2:
        st.subheader("Google Sign In")
        st.markdown("Sign in quickly with your Google account.")
        st.markdown("---")
        
        google_login_url = f"{st.session_state.api_base}/api/auth/google"
        st.markdown(
            f'<a href="{google_login_url}" target="_blank" style="text-decoration:none;"><button style="width:100%; padding:12px; background-color:#4285F4; color:white; border:none; border-radius:4px; font-weight:bold; font-size:16px; cursor:pointer;">Sign in with Google</button></a>',
            unsafe_allow_html=True,
        )
        
        st.caption("After completing Google login, you will return to continue.")


# ============================================================================
# UI Pages - Placement Test
# ============================================================================
def _render_placement_test() -> None:
    st.header("Placement Test")
    st.markdown("Answer these questions so we can determine your English level (CEFR A1-C2).")
    
    questions = st.session_state.get("placement_questions") or []
    if not questions:
        if st.button("Load Questions"):
            ok, qs, err = api_get_placement_questions()
            if ok:
                st.session_state.placement_questions = qs
                st.rerun()
            else:
                st.error(f"Failed to load: {err}")
        return
    
    st.progress(min(len(st.session_state.test_answers) / max(len(questions), 1), 1.0))
    
    with st.form("placement_form"):
        answers = {}
        for i, q in enumerate(questions, 1):
            qid = q["question_id"]
            opts = q.get("options") or []
            st.markdown(f"**Question {i}:** {q['question']}")
            
            if opts:
                choice = st.radio("Select answer", opts, key=f"pl_{qid}", label_visibility="collapsed")
                answers[qid] = choice
            else:
                answers[qid] = st.text_input("Your answer", key=f"pl_{qid}")
        
        submitted = st.form_submit_button("Submit Test", type="primary")
    
    if submitted and len(answers) == len(questions):
        ok, result, err = api_submit_placement(answers)
        if ok:
            level = result.get("level", "A1")
            score = result.get("score", 0)
            data = load_user_data()
            data["placement_completed"] = True
            data["placement_level"] = level
            data["onboarding_done"] = True
            save_user_data(data)
            
            st.success(f"Test completed! Your level: **{level}** (Score: {score}%)")
            st.balloons()
            st.session_state.app_page = "chat"
            st.rerun()
        else:
            st.error(f"Submission failed: {err}")


# ============================================================================
# UI Pages - Level Up Test
# ============================================================================
def _render_level_up_test() -> None:
    st.header("Level Up Test")
    level = current_level()
    st.markdown(f"Your current level: **{level}**. Pass this test to advance!")
    
    questions = st.session_state.get("levelup_questions") or []
    if not questions:
        if st.button("Load Level Up Questions"):
            ok, qs, err = api_get_level_questions(level)
            if ok:
                st.session_state.levelup_questions = qs
                st.rerun()
            else:
                st.error(f"Failed to load: {err}")
        return
    
    st.progress(min(len(st.session_state.test_answers) / max(len(questions), 1), 1.0))
    
    with st.form("levelup_form"):
        answers = {}
        for i, q in enumerate(questions, 1):
            qid = q["question_id"]
            opts = q.get("options") or []
            st.markdown(f"**Question {i}:** {q['question']}")
            
            if opts:
                choice = st.radio("Select answer", opts, key=f"lu_{qid}", label_visibility="collapsed")
                answers[qid] = choice
            else:
                answers[qid] = st.text_input("Your answer", key=f"lu_{qid}")
        
        submitted = st.form_submit_button("Submit Test", type="primary")
    
    if submitted and len(answers) == len(questions):
        ok, result, err = api_submit_level_up(level, "grammar", answers)
        if ok:
            new_level = result.get("new_level", level)
            if new_level != level:
                st.success(f"Congratulations! You advanced from **{level}** to **{new_level}**!")
                st.balloons()
            else:
                st.info(f"You did well but need more practice before advancing. Keep learning!")
            st.session_state.app_page = "chat"
            st.rerun()
        else:
            st.error(f"Submission failed: {err}")


# ============================================================================
# UI Pages - Main Chat (ChatGPT-like Layout)
# ============================================================================
def _render_chat_sidebar() -> None:
    """Left sidebar with chat history"""
    user = st.session_state.user or {}
    st.markdown(f"**{user.get('full_name') or user.get('email', 'User')}**")
    st.caption(f"Level: {current_level()}")
    st.divider()
    
    if st.button("New Chat", use_container_width=True):
        new_chat_session()
        st.rerun()
    
    st.markdown("**History**")
    data = load_user_data()
    sessions = data.get("sessions", [])
    
    for session in sessions:
        sid = session.get("id")
        title = session.get("title", "Conversation")
        if st.button(title[:30], use_container_width=True, key=f"sess_{sid}"):
            load_session(sid)
            st.rerun()
    
    st.divider()
    st.markdown("**Settings**")
    
    st.session_state.chat_target_lang = st.selectbox(
        "Target Language",
        [""] + list(TARGET_LANG_OPTIONS.keys()),
        format_func=lambda x: "Auto" if x == "" else TARGET_LANG_OPTIONS[x],
        key="sel_target",
    )
    st.session_state.chat_explain_in = st.selectbox(
        "Explain in", ["vi", "en"],
        format_func=lambda x: "Vietnamese" if x == "vi" else "English",
        key="sel_explain",
    )
    st.session_state.chat_difficulty = st.selectbox(
        "Difficulty", ["", "easy", "medium", "hard"],
        format_func=lambda x: "Auto" if x == "" else x.capitalize(),
        key="sel_diff",
    )
    st.session_state.chat_temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05, key="sel_temp")
    
    st.divider()
    
    if st.button("Retake Placement Test", use_container_width=True):
        ok, qs, err = api_get_placement_questions()
        if ok:
            st.session_state.placement_questions = qs
            st.session_state.test_answers = {}
            st.session_state.app_page = "placement"
            st.rerun()
        else:
            st.error(err)
    
    if ready_for_level_up() and st.button("Level Up Test", type="primary", use_container_width=True):
        level = current_level()
        ok, qs, err = api_get_level_questions(level)
        if ok:
            st.session_state.levelup_questions = qs
            st.session_state.test_answers = {}
            st.session_state.app_page = "levelup"
            st.rerun()
        else:
            st.error(err)
    
    st.divider()
    if st.button("Logout", use_container_width=True):
        _logout()
        st.rerun()


def _render_chat_main() -> None:
    """Main chat interface"""
    st.markdown(f"**Current Level: {current_level()}**")
    st.markdown("Type a message to chat with AI. Try: **translate to English**, **check grammar**, or **give me an exercise**")
    st.markdown("---")
    
    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("metadata") and msg["role"] == "assistant":
                with st.expander("Details"):
                    st.json(msg["metadata"])
    
    # Input box
    user_input = st.chat_input("Your message...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        target = st.session_state.get("chat_target_lang") or None
        if target == "":
            target = None
        explain_in = st.session_state.get("chat_explain_in", "vi")
        difficulty = st.session_state.get("chat_difficulty") or None
        if difficulty == "":
            difficulty = None
        temperature = float(st.session_state.get("chat_temperature", 0.7))
        
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                ok, reply, metadata = api_chat(user_input, target, explain_in, difficulty, temperature)
            
            if ok:
                st.markdown(reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply, "metadata": metadata}
                )
            else:
                st.error(reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"[Error] {reply}"}
                )
        
        persist_messages()
        st.rerun()


# ============================================================================
# Main Application
# ============================================================================
def main() -> None:
    _init_session()
    
    st.set_page_config(
        page_title="AI Language Tutor",
        page_icon="Books",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Handle OAuth callback
    query_params = st.query_params
    if "token" in query_params and not st.session_state.access_token:
        token = query_params["token"]
        st.session_state.access_token = token
        api_fetch_profile()
        _after_auth_load_state()
        st.success("Google login successful!")
        st.rerun()
    
    # Main layout
    if not st.session_state.access_token:
        # Auth page - full width
        with st.sidebar:
            st.markdown("**Backend Status**")
            ok, status = api_health()
            st.success(f"Connected: {status}") if ok else st.error(f"Disconnected: {status}")
        
        st.title("AI Language Tutor")
        st.markdown("Learn English with AI-powered personalized lessons")
        st.divider()
        _render_auth_page()
    
    else:
        # Logged in - ChatGPT layout with sidebar
        with st.sidebar:
            st.markdown("**Backend Status**")
            ok, status = api_health()
            st.success(f"Connected: {status}") if ok else st.error(f"Disconnected: {status}")
            st.divider()
            _render_chat_sidebar()
        
        # Main content
        page = st.session_state.app_page
        
        if page == "placement" and needs_placement_test():
            _render_placement_test()
        elif page == "levelup":
            _render_level_up_test()
        else:
            st.title("AI Language Tutor")
            _render_chat_main()


if __name__ == "__main__":
    main()
