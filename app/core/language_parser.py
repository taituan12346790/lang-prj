# app/core/language_parser.py
import re
from typing import Dict, Any
from loguru import logger

try:
    from langdetect import detect
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False


class LanguageParser:
    """Chỉ parse ngôn ngữ + override + cleaning. KHÔNG quyết định intent."""

    def __init__(self):
        self.lang_map = {
            "tiếng đức": "German", "german": "German", "deutsch": "German", "đức": "German",
            "tiếng anh": "English", "english": "English", "anh": "English",
            "tiếng pháp": "French", "french": "French", "pháp": "French",
            "tiếng tây ban nha": "Spanish", "spanish": "Spanish",
            "bồ đào nha": "Portuguese", "portuguese": "Portuguese",
            "tiếng việt": "Vietnamese", "vietnamese": "Vietnamese",
        }

    def parse(self, user_input: str, learning_target: str, teaching_lang: str) -> Dict[str, Any]:
        lower = user_input.lower()

        result = {
            "source_lang": "auto",
            "target_lang": learning_target,           # Default là ngôn ngữ đang học
            "teaching_lang": teaching_lang,
            "user_explicit_override": False,
            "content": self._clean_content(user_input),
            "input_type": "general",
            "is_foreign_sentence": False 
        }

        # Explicit override (sang ..., to ..., into ...)
        if self._has_explicit_target(lower):
            target = self._detect_target_language(lower)
            if target:
                result["target_lang"] = target
                result["user_explicit_override"] = True
                result["input_type"] = "explicit_override"

        # Foreign sentence rule (chỉ áp dụng khi KHÔNG có command và KHÔNG có override)
        elif not self._has_translate_command(lower) and self._is_foreign_sentence(user_input):
            result["is_foreign_sentence"] = True
            result["input_type"] = "foreign_sentence"

        return result

    def _has_translate_command(self, text: str) -> bool:
        return any(k in text for k in ["dịch", "translate", "traduzir", "tłumaczyć", "übersetzen", "sang", "into"])

    def _has_explicit_target(self, text: str) -> bool:
        return any(k in text for k in list(self.lang_map.keys()) + ["sang", "to", "into"])

    def _detect_target_language(self, text: str) -> str | None:
        for key, lang in self.lang_map.items():
            if key in text:
                return lang
        return None

    def _is_foreign_sentence(self, text: str) -> bool:
        if LANGDETECT_AVAILABLE:
            try:
                return detect(text[:250]) != 'vi'
            except:
                pass
        return False  # fallback safe

    def _clean_content(self, text: str) -> str:
        text = re.sub(r'^(dịch|translate|traduzir|tłumaczyć|übersetzen)\s*[:：-]?\s*', '', text, flags=re.IGNORECASE)
        return text.strip()