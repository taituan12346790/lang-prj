# app/utils/level_utils.py
from typing import Tuple, List
from app.schemas.test import Level   # import enum từ schema


def get_level_from_score(score: float) -> Level:
    """Chuyển điểm số thành level CEFR (dùng enum)"""
    if score >= 90:
        return Level.C1
    elif score >= 75:
        return Level.B2
    elif score >= 60:
        return Level.B1
    elif score >= 45:
        return Level.A2
    else:
        return Level.A1


def get_level_range(level: Level) -> Tuple[float, float]:
    """Trả về khoảng điểm cho level (nhận enum)"""
    ranges = {
        Level.A1: (0, 45),
        Level.A2: (45, 60),
        Level.B1: (60, 75),
        Level.B2: (75, 90),
        Level.C1: (90, 100),
    }
    return ranges.get(level, (0, 100))


def get_recommended_focus(level: Level) -> List[str]:
    """Gợi ý kỹ năng nên tập trung theo level (nhận enum)"""
    focus_map = {
        Level.A1: ["basic_vocabulary", "simple_grammar", "listening"],
        Level.A2: ["daily_conversation", "basic_tenses", "reading"],
        Level.B1: ["complex_sentences", "speaking", "listening"],
        Level.B2: ["advanced_vocabulary", "writing", "idioms"],
        Level.C1: ["nuance", "formal_writing", "debate"],
    }
    return focus_map.get(level, ["general_practice"])


def can_level_up(current_level: Level, test_score: float) -> bool:
    """Kiểm tra có đủ điều kiện lên level không (nhận enum)"""
    thresholds = {
        Level.A1: 70,
        Level.A2: 75,
        Level.B1: 78,
        Level.B2: 80,
    }
    return test_score >= thresholds.get(current_level, 75)