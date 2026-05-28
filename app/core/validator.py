import re
from typing import Dict, Any, Tuple, List


class ResponseValidator:
    """
    Validator toàn diện cho AI Language Tutor
    - Input Guardrail mạnh
    - Output Safety + Pedagogy
    """

    def __init__(self):
        # =========================================================
        # 1. ABSOLUTE BLOCK - Tuyệt đối KHÔNG cho qua dù có intent gì
        # =========================================================
        self.absolute_block_patterns = [
            # Sexual explicit / NSFW
            r'sexting|dirty talk|erotic roleplay|sex chat',
            r'cho anh bú|lồn em ướt|cặc anh to|quan hệ tình dục',
            # Religious hate
            r'đụ chúa|địt phật|địt jesus|chửi allah|chửi đức phật|đụ mẹ chúa',
            # Violence & Extremism
            r'khủng bố|diệt chủng|giết hết|lật đổ chính quyền|đảo chính',
            # Geopolitical conflicts & Territorial disputes (SIẾT CHẮT)
            r'hoàng sa|trường sa|biển đông.*(tranh chấp|chiếm)',
            r'đài loan.*(độc lập|quốc gia|country)',
            r'palestine|israel|gaza|crimea',
            r'chiến tranh.*(ukraine|nga|gaza|israel)',
        ]

        # =========================================================
        # 2. SENSITIVE TOPICS - Cho phép chỉ khi có educational intent rõ
        # =========================================================
        self.sensitive_topic_patterns = [
            r'chính trị|cộng sản|tư bản|xã hội chủ nghĩa|left wing|right wing',
            r'hồi giáo|islam|jihad|thiên chúa|kitô|phật giáo',
            r'đảng cộng sản|bác hồ|chủ tịch hồ chí minh',
        ]

        # =========================================================
        # 3. VULGAR / THÔ TỤC - Cho phép nếu học ngôn ngữ
        # =========================================================
        self.vulgar_patterns = [
            r'đụ|địt|đm|đmm|lồn|cặc|buồi|clmm|đéo|vãi lồn',
            r'fuck|shit|bitch|porn|sex|nude|naked|onlyfans',
        ]

        # =========================================================
        # 4. EDUCATIONAL SIGNALS
        # =========================================================
        self.educational_signals = {
            "nghĩa là gì", "dịch", "translate", "giải thích", "cách dùng",
            "ví dụ", "ngữ cảnh", "sắc thái", "mức độ", "từ lóng", "thô tục",
            "tục", "phân biệt", "etymology", "origin", "slang", "offensive",
            "what does it mean", "meaning", "usage", "example", "context"
        }

    def normalize(self, text: str) -> str:
        """Chuẩn hóa text để kiểm tra"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\sÀ-ỹ]', ' ', text)   # giữ chữ Việt
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def has_educational_intent(self, text: str) -> bool:
        """Kiểm tra có ý định học ngôn ngữ không"""
        norm = self.normalize(text)
        return any(signal in norm for signal in self.educational_signals)

    def contains_pattern(self, text: str, patterns: List[str]) -> bool:
        """Kiểm tra có khớp pattern nào không"""
        norm = self.normalize(text)
        for pattern in patterns:
            if re.search(pattern, norm, re.IGNORECASE):
                return True
        return False

    # ====================== INPUT GUARDRAIL ======================
    def validate_input(self, user_input: str) -> Tuple[bool, str]:
        """Kiểm tra input - Đây là lớp bảo vệ đầu tiên"""
        if not user_input or len(user_input.strip()) < 3:
            return False, "Input too short"

        norm = self.normalize(user_input)
        is_educational = self.has_educational_intent(user_input)

        # 1. Tuyệt đối chặn
        if self.contains_pattern(user_input, self.absolute_block_patterns):
            return False, "absolute_prohibited_topic"

        # 2. Chủ đề nhạy cảm (chính trị, tôn giáo, địa chính trị)
        if self.contains_pattern(user_input, self.sensitive_topic_patterns):
            if not is_educational:
                return False, "sensitive_topic_without_educational_intent"

        # 3. Nội dung thô tục
        if self.contains_pattern(user_input, self.vulgar_patterns):
            if not is_educational:
                return False, "vulgar_content_without_educational_intent"

        return True, "allowed"

    # ====================== OUTPUT VALIDATION ======================
    def validate_output_safety(self, response: str) -> Tuple[bool, str]:
        if len(response.strip()) < 30:
            return False, "Response too short"

        if self.contains_pattern(response, self.absolute_block_patterns):
            return False, "dangerous_content_in_output"

        return True, "safe"

    def validate_pedagogy(self, response: str, intent: str = "") -> Tuple[bool, str]:
        """Kiểm tra chất lượng sư phạm"""
        if intent not in ["grammar", "vocabulary", "explanation", "translation"]:
            return True, "skip"

        response_lower = response.lower()
        has_concept = any(k in response_lower for k in ["khái niệm", "nghĩa là", "là gì", "định nghĩa"])
        has_usage = any(k in response_lower for k in ["cách dùng", "dùng khi", "cấu trúc", "quy tắc"])
        has_example = any(k in response_lower for k in ["ví dụ", "example", "chẳng hạn"])

        missing = []
        if not has_concept: missing.append("concept")
        if not has_usage: missing.append("usage")
        if not has_example: missing.append("example")

        if len(missing) >= 2:
            return False, f"Pedagogy insufficient: missing {missing}"

        return True, "pedagogy_ok"

    def validate_language(self, response: str, teaching_lang: str = "vi") -> Tuple[bool, str]:
        """Kiểm tra tỷ lệ tiếng Việt"""
        if teaching_lang not in ["vi", "Tiếng Việt"]:
            return True, "skip"

        response_lower = response.lower()
        viet_chars = len(re.findall(r'[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]', response_lower))
        total_chars = max(len(response_lower), 1)
        ratio = viet_chars / total_chars

        if len(response_lower) > 100 and ratio < 0.12:
            return False, "language_drift"

        return True, "language_ok"

    # ====================== MAIN VALIDATE ======================
    def validate(self, response: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        user_input = context.get("user_input", "")
        intent = context.get("intent", "")
        teaching_lang = context.get("teaching_lang", "vi")

        # 1. Kiểm tra Input trước
        allowed, reason = self.validate_input(user_input)
        if not allowed:
            return False, f"Input blocked: {reason}"

        # 2. Safety Output
        safe, reason = self.validate_output_safety(response)
        if not safe:
            return False, reason

        # 3. Pedagogy
        pedagogy_ok, reason = self.validate_pedagogy(response, intent)
        if not pedagogy_ok:
            return False, reason

        # 4. Language
        lang_ok, reason = self.validate_language(response, teaching_lang)
        if not lang_ok:
            return False, reason

        return True, "Passed"
        return True, ""