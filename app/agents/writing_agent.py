# app/agents/writing_agent.py
"""
Writing Evaluator Agent: Specialized AI Agent for evaluating student writing submissions.
Role: Grade writing based on CEFR criteria and provide detailed feedback.
"""
import json
from typing import Dict, Any, Optional
from uuid import UUID
from loguru import logger

from app.agents.base_agent import AIAgent
from app.services.writing_service import WritingService
from app.llm.llm_client import get_llm_client


class WritingAgent(AIAgent):
    """
    Writing Evaluator Agent handles writing assessment tasks:
    - Grade writing submissions based on CEFR criteria
    - Provide detailed feedback on grammar, vocabulary, content, structure
    - Track writing progress over time
    - Suggest improvements and practice areas
    """
    
    def __init__(self, service: WritingService):
        """
        Initialize Writing Evaluator Agent.
        
        Args:
            service: WritingService instance
        """
        super().__init__(agent_name="WritingAgent", tool_instance=service)
        self.service = service
        self.llm_client = get_llm_client()
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute writing evaluation task.
        
        Args:
            params: Must contain:
                - user_text: The student's writing submission
                - prompt: The writing prompt/topic
                - cefr_level: Target CEFR level (A1-C2)
                - lesson_id: Optional lesson ID for tracking
                - topic_id: Optional topic ID for tracking
                
        Returns:
            Dict with evaluation results and detailed feedback
        """
        try:
            logger.debug(f"{self.agent_name} evaluating writing submission")
            
            user_text = params.get("user_text", "")
            prompt = params.get("prompt", "")
            cefr_level = params.get("cefr_level", "B1")
            
            if not user_text:
                return {
                    "success": False,
                    "error": "Không có nội dung để đánh giá"
                }
            
            # Generate detailed feedback using LLM
            feedback_result = await self._generate_feedback(
                user_text=user_text,
                prompt=prompt,
                cefr_level=cefr_level
            )
            
            logger.debug(f"{self.agent_name} completed evaluation successfully")
            return feedback_result
            
        except Exception as e:
            logger.error(f"{self.agent_name} error: {e}")
            return {
                "success": False,
                "error": "Đánh giá bài viết thất bại",
                "details": str(e)
            }
    
    async def _generate_feedback(
        self,
        user_text: str,
        prompt: str,
        cefr_level: str
    ) -> Dict[str, Any]:
        """
        Generate detailed feedback for writing submission using LLM.
        
        Evaluates based on 4 CEFR criteria:
        - Grammar (25 points)
        - Vocabulary (25 points)
        - Content (25 points)
        - Structure (25 points)
        
        Args:
            user_text: Student's writing
            prompt: Writing prompt
            cefr_level: Target level
            
        Returns:
            Dict with scores and feedback
        """
        evaluation_prompt = f"""You are an English writing evaluator. Evaluate the following writing submission based on CEFR {cefr_level} level.

Writing Prompt: {prompt}

Student's Writing:
{user_text}

Evaluate based on 4 criteria (each out of 25 points):

1. **Grammar** (25 points):
   - Sentence structure correctness
   - Verb tense accuracy
   - Subject-verb agreement
   - Punctuation and capitalization

2. **Vocabulary** (25 points):
   - Word choice appropriateness
   - Range of vocabulary
   - Collocation accuracy
   - Spelling

3. **Content** (25 points):
   - Task achievement
   - Relevance to prompt
   - Development of ideas
   - Examples and details

4. **Structure** (25 points):
   - Organization and coherence
   - Paragraph structure
   - Logical flow
   - Use of linking words

Provide response in this JSON format:
{{
    "score_grammar": 0-25,
    "score_vocabulary": 0-25,
    "score_content": 0-25,
    "score_structure": 0-25,
    "feedback": "Overall feedback in Vietnamese",
    "grammar_notes": ["List of grammar issues"],
    "vocabulary_notes": ["List of vocabulary suggestions"],
    "content_notes": ["List of content improvements"],
    "structure_notes": ["List of structure improvements"],
    "strengths": ["What the student did well"],
    "improvements": ["Specific areas to improve"]
}}

Respond ONLY with valid JSON, no additional text."""

        try:
            response = await self.llm_client.generate_text(evaluation_prompt)
            
            # Parse JSON response
            # Remove markdown code blocks if present
            response_clean = response.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]
            if response_clean.startswith("```"):
                response_clean = response_clean[3:]
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]
            response_clean = response_clean.strip()
            
            result = json.loads(response_clean)
            
            # Calculate total score
            total = (
                result.get("score_grammar", 0) +
                result.get("score_vocabulary", 0) +
                result.get("score_content", 0) +
                result.get("score_structure", 0)
            )
            
            return {
                "success": True,
                "score_grammar": result.get("score_grammar", 0),
                "score_vocabulary": result.get("score_vocabulary", 0),
                "score_content": result.get("score_content", 0),
                "score_structure": result.get("score_structure", 0),
                "score_total": total,
                "feedback": result.get("feedback", ""),
                "detailed_feedback": {
                    "grammar_notes": result.get("grammar_notes", []),
                    "vocabulary_notes": result.get("vocabulary_notes", []),
                    "content_notes": result.get("content_notes", []),
                    "structure_notes": result.get("structure_notes", []),
                    "strengths": result.get("strengths", []),
                    "improvements": result.get("improvements", [])
                }
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            return {
                "success": False,
                "error": "Không thể phân tích kết quả đánh giá",
                "details": str(e)
            }
        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            return {
                "success": False,
                "error": "Lỗi khi tạo phản hồi",
                "details": str(e)
            }
