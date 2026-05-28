# app/core/intent_classifier.py
from typing import Dict, Any
from loguru import logger


class LearningIntentClassifier:
    def classify(self, user_input: str) -> Dict[str, Any]:
        lower = user_input.lower().strip()

        intent = {
            "primary_intent": "general",
            "secondary_intent": None,
            "topic": "general",
            "needs_explanation": False,
            "needs_practice": False,
            "confidence": 0.6
        }

        if any(k in lower for k in ["ngữ pháp", "grammar", "cấu trúc", "thì", "tense", "sửa lỗi", "correct", "cách dùng"]):
            intent.update({"primary_intent": "grammar", "needs_explanation": True, "confidence": 0.9})

        elif any(k in lower for k in ["từ vựng", "vocabulary", "nghĩa của", "nghĩa là gì", "how do i say", "how to say", "gọi là gì"]):
            intent.update({"primary_intent": "vocabulary", "needs_translation": True, "confidence": 0.85})

        elif any(k in lower for k in ["bài tập", "exercise", "practice", "luyện", "quiz"]):
            intent.update({"primary_intent": "exercise", "needs_practice": True, "confidence": 0.88})

        elif any(k in lower for k in ["dịch", "translate", "sang", "into"]):
            intent.update({"primary_intent": "translation", "needs_translation": True, "confidence": 0.92})

        elif any(k in lower for k in ["giải thích", "explain", "tại sao", "ý nghĩa"]):
            intent.update({"primary_intent": "explanation", "needs_explanation": True, "confidence": 0.8})

        logger.info(f"[IntentClassifier] {intent['primary_intent']} (conf: {intent['confidence']:.2f})")
        return intent