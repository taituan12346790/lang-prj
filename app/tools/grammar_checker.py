from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError
from enum import Enum
import language_tool_python
import logging
import asyncio
import json

logger = logging.getLogger(__name__)

GRAMMAR_SYSTEM_PROMPT = """Bạn là giáo viên {teaching_lang} chuyên nghiệp, cẩn thận và chính xác.
Giải thích rõ ràng, khích lệ cho học viên người Việt.
**Quan trọng**: Chỉ sửa lỗi thật sự. Nếu câu đã đúng thì KHÔNG sửa và ghi nhận là tốt.
Chỉ trả về JSON thuần theo schema, không markdown, không code block."""


# ========================== MODELS ==========================
class GrammarErrorType(str, Enum):
    SPELLING = "spelling"
    GRAMMAR = "grammar"
    PUNCTUATION = "punctuation"
    STYLE = "style"
    AGREEMENT = "agreement"
    TENSE = "tense"
    ARTICLE = "article"
    PREPOSITION = "preposition"
    WORD_CHOICE = "word_choice"
    SENTENCE_STRUCTURE = "sentence_structure"
    OTHER = "other"


class GrammarError(BaseModel):
    error_type: GrammarErrorType
    original: str
    corrected: str
    message: str
    explanation: str
    suggestions: List[str] = Field(default_factory=list)


class GrammarCorrectionResult(BaseModel):
    original_text: str
    corrected_text: str
    errors: List[GrammarError] = Field(..., max_length=10)
    overall_feedback: str
    teaching_points: List[str] = Field(..., max_length=6)
    target_lang: str
    teaching_lang: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class GrammarChecker:
    """Grammar Checker Hybrid - Production Ready (Final Version)"""

    def __init__(self, llm):
        self.llm = llm
        self.tools = {}
        self.max_retries = 3
        self.timeout_seconds = 35

    def _map_rule_to_error_type(self, rule_id: str) -> GrammarErrorType:
        """Mapping chặt chẽ hơn với thứ tự ưu tiên"""
        if not rule_id:
            return GrammarErrorType.OTHER
            
        rule = rule_id.upper()
        
        # Mapping ưu tiên
        if "SPELL" in rule or "TYPO" in rule:
            return GrammarErrorType.SPELLING
        if "PUNCT" in rule:
            return GrammarErrorType.PUNCTUATION
        if "TENSE" in rule:
            return GrammarErrorType.TENSE
        if "ARTICLE" in rule:
            return GrammarErrorType.ARTICLE
        if "PREP" in rule:
            return GrammarErrorType.PREPOSITION
        if "AGREEMENT" in rule or "SUBJ" in rule:
            return GrammarErrorType.AGREEMENT
        if "STYLE" in rule:
            return GrammarErrorType.STYLE
        if "SENTENCE" in rule or "STRUCTURE" in rule:
            return GrammarErrorType.SENTENCE_STRUCTURE
        if any(x in rule for x in ["GRAMMAR", "MORF", "SYN"]):
            return GrammarErrorType.GRAMMAR
        if "WORD" in rule or "CHOICE" in rule:
            return GrammarErrorType.WORD_CHOICE
            
        return GrammarErrorType.OTHER

    def _get_language_tool(self, target_lang: str):
        lang_map = {
            "English": "en-US",
            "Portuguese": "pt-BR",
            "Spanish": "es",
            "French": "fr",
            "German": "de-DE",
            "Italian": "it-IT",
            "Russian": "ru-RU",
            "Chinese": "zh-CN",
            "Japanese": "ja-JP",
            "Korean": "ko-KR",
            "Polish": "pl-PL",
        }
        lang_code = lang_map.get(target_lang, "en-US")
        
        if target_lang not in lang_map:
            logger.warning(f"⚠️ No specific LanguageTool for '{target_lang}', using en-US")

        if lang_code not in self.tools:
            try:
                self.tools[lang_code] = language_tool_python.LanguageTool(lang_code)
                logger.info(f"✅ LanguageTool initialized: {target_lang} ({lang_code})")
            except Exception as e:
                logger.error(f"❌ LanguageTool failed for {target_lang}: {e}")
                self.tools[lang_code] = None
        return self.tools[lang_code]

    def _prepare_tool_errors(self, matches) -> str:
        """Xử lý an toàn và giới hạn sớm"""
        processed = []
        for match in list(matches)[:12]:  # Giới hạn sớm
            # Lấy đúng đoạn lỗi
            error_text = ""
            if hasattr(match, 'sentence') and hasattr(match, 'offset') and hasattr(match, 'errorLength'):
                try:
                    error_text = match.sentence[match.offset:match.offset + match.errorLength]
                except:
                    error_text = match.sentence or ""

            # Xử lý replacement an toàn
            corrected = ""
            if match.replacements:
                corrected = match.replacements[0]
            else:
                corrected = error_text  # giữ nguyên nếu không có gợi ý

            processed.append({
                "error_type": match.ruleId if hasattr(match, 'ruleId') else "",
                "original": error_text or match.sentence,
                "corrected": corrected,
                "message": getattr(match, 'message', '')
            })
        return json.dumps(processed, ensure_ascii=False, separators=(",", ":"))

    async def _safe_llm_enhance(self, input_data: dict) -> Optional[GrammarCorrectionResult]:
        system_prompt = GRAMMAR_SYSTEM_PROMPT.format(
            teaching_lang=input_data["teaching_lang"]
        )
        user_prompt = f"""Original text: {input_data['original_text']}
Corrected text (từ rule-based): {input_data['corrected_text']}
Lỗi từ LanguageTool: {input_data['tool_errors_json']}
Điểm yếu của học viên: {input_data['weaknesses']}"""

        for attempt in range(self.max_retries):
            try:
                logger.info(f"GrammarChecker LLM Attempt {attempt+1}/{self.max_retries}")

                result = await asyncio.wait_for(
                    self.llm.generate_structured_async(
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        response_format=GrammarCorrectionResult,
                        temperature=0.25,
                        max_retries=0,
                    ),
                    timeout=self.timeout_seconds,
                )
                if result is not None:
                    return result

            except asyncio.TimeoutError:
                logger.warning(f"Timeout at attempt {attempt+1}")
            except ValidationError as ve:
                logger.warning(f"ValidationError (attempt {attempt+1}): {ve}")
            except Exception as e:
                error_str = str(e).lower()
                if any(k in error_str for k in ["rate limit", "timeout", "connection", "overloaded", "busy"]):
                    logger.warning(f"Retryable error (attempt {attempt+1})")
                else:
                    logger.error(f"Non-retryable: {e}")
                    raise

            if attempt < self.max_retries - 1:
                await asyncio.sleep(1.6 ** attempt)

        return None

    async def check(
        self,
        text: str,
        target_lang: str = "English",
        teaching_lang: str = "Vietnamese",
        user_weaknesses: Optional[List[str]] = None
    ) -> Dict:
        if not text or not text.strip():
            return {"error": "Text is empty"}

        original_text = text[:1200] if len(text) > 1200 else text
        user_weaknesses = user_weaknesses or []
        weaknesses_str = ", ".join(user_weaknesses[:6]) if user_weaknesses else "không có"

        # Rule-based
        tool = self._get_language_tool(target_lang)
        tool_matches = []
        corrected_text = original_text

        if tool:
            try:
                matches = tool.check(original_text)
                tool_matches = list(matches)[:15]  # Giới hạn sớm
                if tool_matches:
                    corrected_text = language_tool_python.utils.correct(original_text, tool_matches)
            except Exception as e:
                logger.error(f"LanguageTool error: {e}")

        # LLM Enhancement
        try:
            tool_errors_json = self._prepare_tool_errors(tool_matches)

            input_data = {
                "teaching_lang": teaching_lang,
                "original_text": original_text,
                "corrected_text": corrected_text,
                "tool_errors_json": tool_errors_json,
                "weaknesses": weaknesses_str
            }

            result = await self._safe_llm_enhance(input_data)

            if result is None:
                return self._fallback_result(original_text, corrected_text, tool_matches, target_lang, teaching_lang)

            data = result.model_dump()
            # Ưu tiên confidence từ LLM, chỉ fallback nếu quá thấp
            if data.get("confidence", 0) < 0.6:
                data["confidence"] = max(0.75 - (len(data.get("errors", [])) * 0.07), 0.6)
            return data

        except Exception as e:
            logger.exception(f"GrammarChecker unexpected error: {e}")
            return self._fallback_result(original_text, corrected_text, tool_matches, target_lang, teaching_lang)

    def _fallback_result(self, original: str, corrected: str, tool_matches, 
                        target_lang: str, teaching_lang: str) -> Dict:
        errors_list = []
        for m in tool_matches[:6]:
            error_type = self._map_rule_to_error_type(getattr(m, 'ruleId', ''))
            error_text = getattr(m, 'sentence', '')[getattr(m, 'offset', 0):getattr(m, 'offset', 0) + getattr(m, 'errorLength', 0)]
            
            corrected_text = m.replacements[0] if m.replacements else error_text

            errors_list.append({
                "error_type": error_type.value,
                "original": error_text or getattr(m, 'sentence', ''),
                "corrected": corrected_text,
                "message": getattr(m, 'message', ''),
                "explanation": "",
                "suggestions": m.replacements[:3] if m.replacements else []
            })

        return {
            "original_text": original,
            "corrected_text": corrected,
            "errors": errors_list,
            "overall_feedback": f"Đã kiểm tra ngữ pháp. Phát hiện {len(errors_list)} lỗi và gợi ý sửa.",
            "teaching_points": [],
            "target_lang": target_lang,
            "teaching_lang": teaching_lang,
            "confidence": 0.65
        }