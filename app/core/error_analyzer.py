# app/core/error_analyzer.py
"""
Error Analyzer - Phân tích lỗi sai của user và classify
"""
from typing import Dict, Any, List, Optional
from loguru import logger
import re

from app.llm.llm_client import LLMClient


class ErrorAnalyzer:
    """Analyze user errors and classify them"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    async def analyze(
        self,
        question: str,
        user_answer: str,
        correct_answer: str,
        skill_tag: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Phân tích lỗi của user
        
        Returns:
            {
                "error_type": "GRAMMAR_ERROR" or "VOCABULARY_ERROR",
                "skill_tag": "past_tense",
                "severity": "HIGH",
                "explanation": "...",
                "user_mistake": "...",
                "why_wrong": "..."
            }
        """
        try:
            # Use AI to classify error type
            prompt = f"""Analyze this language learning error and classify it:

Question: {question}
Student's Answer: {user_answer}
Correct Answer: {correct_answer}

YOUR TASK:
1. Classify the error type (ONLY ONE):
   - GRAMMAR_ERROR: Grammar mistakes (tense, verb form, sentence structure, preposition, article, word order, PRONOUN CHOICE, subject-verb agreement)
   - VOCABULARY_ERROR: Vocabulary mistakes (using a completely different word with different meaning)

2. Assess severity: LOW, MEDIUM, HIGH

3. Provide brief explanation (1-2 sentences in Vietnamese for the student)

CLASSIFICATION RULES:
- If student chose WRONG PRONOUN (e.g., "She" instead of "I", "They" instead of "He") → GRAMMAR_ERROR
- If student chose WRONG VERB FORM with grammatical implications (e.g., "She" requires "is", "I" requires "am") → GRAMMAR_ERROR
- If student used WRONG TENSE (e.g., "go" instead of "went", "go" instead of "goes") → GRAMMAR_ERROR  
- If student used WRONG GRAMMATICAL STRUCTURE (e.g., "there are much" instead of "there is much") → GRAMMAR_ERROR
- If student used COMPLETELY DIFFERENT WORD with unrelated meaning (e.g., "color" instead of "size", "big" instead of "small") → VOCABULARY_ERROR

CRITICAL EXAMPLES:
Q: "I ___ am a student. (I/She/They)" → Student: "She", Correct: "I"
→ GRAMMAR_ERROR (wrong pronoun choice - grammatical error)

Q: "___ am a student" → Student: "She", Correct: "I"  
→ GRAMMAR_ERROR (pronoun must agree with verb "am")

Q: "What ___ do you wear?" → Student: "color", Correct: "size"
→ VOCABULARY_ERROR (chose wrong word, different concept)

Q: "She ___ to school" → Student: "go", Correct: "goes"
→ GRAMMAR_ERROR (missing -s for third person)

Q: "I ___ yesterday" → Student: "go", Correct: "went"
→ GRAMMAR_ERROR (wrong tense form)

Q: "What ___ is the shirt?" → Student: "number", Correct: "size"  
→ VOCABULARY_ERROR (wrong word choice, different meaning)

Respond in this format:
ERROR_TYPE: [GRAMMAR_ERROR or VOCABULARY_ERROR]
SEVERITY: [LOW/MEDIUM/HIGH]
EXPLANATION: [Brief explanation in Vietnamese]"""

            llm_response = await self.llm.generate_async(
                user_input=prompt,
                system_prompt="You are a Language Learning Error Classification Expert. Your job is to accurately classify student errors as GRAMMAR_ERROR or VOCABULARY_ERROR. Focus on the fundamental nature of the mistake.",
                temperature=0.1  # Lower temperature for more consistent classification
            )
            
            # Parse LLM response
            error_data = self._parse_llm_response_simple(llm_response, skill_tag)
            
            return error_data
            
        except Exception as e:
            logger.error(f"Error analysis failed: {e}")
            return self._fallback_analysis(skill_tag)
    
    def _parse_llm_response_simple(self, llm_response: str, skill_tag: Optional[str]) -> Dict[str, Any]:
        """Parse LLM response - simple format"""
        error_type = "GRAMMAR_ERROR"  # Default
        severity = "MEDIUM"
        explanation = llm_response.strip()
        
        # Extract error type from response
        response_upper = llm_response.upper()
        if "ERROR_TYPE:" in response_upper or "ERROR TYPE:" in response_upper:
            if "VOCABULARY_ERROR" in response_upper or "VOCABULARY ERROR" in response_upper:
                error_type = "VOCABULARY_ERROR"
            elif "GRAMMAR_ERROR" in response_upper or "GRAMMAR ERROR" in response_upper:
                error_type = "GRAMMAR_ERROR"
        else:
            # Fallback: check keywords
            if "VOCABULARY" in response_upper or "TỪ VỰNG" in response_upper or "SAI TỪ" in response_upper:
                error_type = "VOCABULARY_ERROR"
        
        # Extract severity
        if "SEVERITY:" in response_upper:
            if "HIGH" in response_upper:
                severity = "HIGH"
            elif "LOW" in response_upper:
                severity = "LOW"
        
        # Extract explanation
        if "EXPLANATION:" in llm_response:
            parts = llm_response.split("EXPLANATION:", 1)
            if len(parts) > 1:
                explanation = parts[1].strip()
        
        return {
            "error_type": error_type,
            "skill_tag": skill_tag or error_type.lower(),
            "severity": severity,
            "explanation": explanation[:500],
            "analysis_method": "AI_CLASSIFICATION"
        }
    
    def _fallback_analysis(self, skill_tag: Optional[str]) -> Dict[str, Any]:
        """Fallback khi analysis fail"""
        return {
            "error_type": "GRAMMAR_ERROR",
            "skill_tag": skill_tag or "general",
            "severity": "MEDIUM",
            "explanation": "Đáp án chưa chính xác. Hãy xem lại lý thuyết và thử lại nhé!",
            "analysis_method": "FALLBACK"
        }
