# app/utils/helpers.py
from typing import Dict, Any, List
import re
from datetime import datetime, timezone


def normalize_text(text: str) -> str:
    """Chuẩn hóa text cho so sánh"""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\sÀ-ỹ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def calculate_streak(last_active: datetime) -> int:
    """Tính streak days (timezone-aware)"""
    if not last_active:
        return 0
    now = datetime.now(timezone.utc)
    delta = now - last_active
    if delta.days < 0:
        return 0
    return max(0, 7 - delta.days) if delta.days < 7 else 0


def split_into_sentences(text: str) -> List[str]:
    """Chia văn bản thành câu"""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def format_duration(minutes: int) -> str:
    """Format thời gian"""
    if minutes < 60:
        return f"{minutes} phút"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours} giờ {mins} phút" if mins > 0 else f"{hours} giờ"


# Giữ lại nhưng không bắt buộc dùng
def is_valid_email(email: str) -> bool:
    """Kiểm tra email hợp lệ (dùng Pydantic EmailStr là đủ)"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None