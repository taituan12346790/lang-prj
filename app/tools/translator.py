# app/tools/translator.py
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from loguru import logger
import asyncio


# ---- Model chỉ dùng cho LLM (không chứa success/warning/error) ----
class LLMTranslationResult(BaseModel):
    translated_text: str = Field(..., description="Văn bản đã dịch")
    explanation: str = Field(..., description="Giải thích ngắn gọn, tự nhiên")

# ---- Model dùng để trả về cho caller (wrapper) ----
class TranslationOutput(BaseModel):
    success: bool = True
    original_text: str
    translated_text: str = ""
    source_lang: str = "auto"
    target_lang: str = ""
    teaching_lang: str = ""
    explanation: str = ""
    warning: Optional[str] = None
    error: Optional[str] = None


TRANSLATOR_SYSTEM_PROMPT = """Bạn là translator chuyên nghiệp và giáo viên ngôn ngữ.
Dịch chính xác từ {source_lang} sang {target_lang}.
Giải thích ngắn gọn, tự nhiên bằng {teaching_lang}.
Chỉ trả về JSON thuần theo schema với các field translated_text và explanation, không markdown."""


class TranslatorTool:
    """Translation Tool"""

    def __init__(self, llm):
        self.llm = llm
        self.max_retries = 2
        self.timeout_seconds = 30

    async def _safe_llm_translate(self, input_data: dict) -> Optional[LLMTranslationResult]:
        """Safe LLM call với retry logic"""
        system_prompt = TRANSLATOR_SYSTEM_PROMPT.format(
            source_lang=input_data["source_lang"],
            target_lang=input_data["target_lang"],
            teaching_lang=input_data["teaching_lang"],
        )
        user_prompt = f"Text to translate: {input_data['text']}"

        for attempt in range(self.max_retries):
            try:
                logger.info(f"TranslatorTool LLM Attempt {attempt+1}/{self.max_retries}")

                result = await asyncio.wait_for(
                    self.llm.generate_structured_async(
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        response_format=LLMTranslationResult,
                        temperature=0.3,
                        max_retries=0,
                    ),
                    timeout=self.timeout_seconds,
                )
                if result is not None:
                    return result

            except asyncio.TimeoutError:
                logger.warning(f"Translation timeout at attempt {attempt+1}")
            except Exception as e:
                error_str = str(e).lower()
                if any(k in error_str for k in ["rate limit", "timeout", "connection", "overloaded"]):
                    logger.warning(f"Retryable error (attempt {attempt+1}): {e}")
                else:
                    logger.error(f"Non-retryable error: {e}")
                    raise

            if attempt < self.max_retries - 1:
                await asyncio.sleep(1.5 ** attempt)

        return None

    async def execute(self, params: Dict[str, Any]) -> TranslationOutput:
        """
        Dịch theo params từ Strategy
        """
        try:
            content = params.get("content", "").strip()
            source_lang = params.get("source_lang", "auto")
            target_lang = params.get("target_lang", "English")
            teaching_lang = params.get("teaching_lang", "Vietnamese")

            if not content:
                return TranslationOutput(
                    success=False,
                    original_text="",
                    error="Không có nội dung để dịch"
                )

            # Chuẩn bị input cho chain
            input_data = {
                "text": content[:1500],  # Giới hạn độ dài
                "source_lang": source_lang,
                "target_lang": target_lang,
                "teaching_lang": teaching_lang
            }

            # Gọi LLM với retry
            result = await self._safe_llm_translate(input_data)

            if result is None:
                return self._fallback_result(
                    original_text=content,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    teaching_lang=teaching_lang
                )

            return TranslationOutput(
                success=True,
                original_text=content,
                translated_text=result.translated_text,
                source_lang=source_lang,
                target_lang=target_lang,
                teaching_lang=teaching_lang,
                explanation=result.explanation,
                warning=params.get("warning"),
            )

        except Exception as e:
            logger.exception(f"TranslatorTool error: {e}")
            return TranslationOutput(
                success=False,
                original_text=params.get("content", ""),
                source_lang=params.get("source_lang", "auto"),
                target_lang=params.get("target_lang", "English"),
                teaching_lang=params.get("teaching_lang", "Vietnamese"),
                error="Dịch thất bại. Vui lòng thử lại."
            )

    def _fallback_result(self, original_text: str, source_lang: str, 
                        target_lang: str, teaching_lang: str) -> TranslationOutput:
        """Fallback khi LLM không thể dịch"""
        return TranslationOutput(
            success=False,
            original_text=original_text,
            source_lang=source_lang,
            target_lang=target_lang,
            teaching_lang=teaching_lang,
            error="Dịch thất bại sau khi thử lại. Vui lòng thử lại sau."
        )