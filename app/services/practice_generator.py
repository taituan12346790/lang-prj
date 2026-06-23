# app/services/practice_generator.py
"""
Generate practice questions based on error type and skill
"""
from typing import List, Dict, Any
from loguru import logger

class PracticeGenerator:
    """Generate targeted practice exercises"""
    
    # Question templates by error type
    TEMPLATES = {
        "TENSE_MISMATCH": {
            "questions": [
                {
                    "text": "Yesterday, I ___ to the market.",
                    "options": ["go", "went", "going"],
                    "answer": "went",
                    "explanation": "Yesterday = quá khứ, nên dùng 'went' (V2)"
                },
                {
                    "text": "Last week, she ___ a new car.",
                    "options": ["buy", "bought", "buying"],
                    "answer": "bought",
                    "explanation": "Last week = quá khứ, 'buy' → 'bought' (irregular)"
                },
                {
                    "text": "Two days ago, they ___ home early.",
                    "options": ["come", "came", "coming"],
                    "answer": "came",
                    "explanation": "Two days ago = quá khứ, 'come' → 'came'"
                },
                {
                    "text": "I ___ coffee every morning.",
                    "options": ["drank", "drink", "drinking"],
                    "answer": "drink",
                    "explanation": "Every morning = hiện tại đơn, nên dùng 'drink'"
                },
                {
                    "text": "Last month, we ___ in London.",
                    "options": ["are", "were", "being"],
                    "answer": "were",
                    "explanation": "Last month = quá khứ, 'be' → 'were' (plural)"
                }
            ]
        },
        "SUBJECT_VERB_AGREEMENT": {
            "questions": [
                {
                    "text": "She ___ to school every day.",
                    "options": ["go", "goes", "going"],
                    "answer": "goes",
                    "explanation": "She = 3rd person singular, động từ thêm 's'"
                },
                {
                    "text": "They ___ very happy.",
                    "options": ["is", "are", "am"],
                    "answer": "are",
                    "explanation": "They = plural, dùng 'are'"
                },
                {
                    "text": "It ___ cold today.",
                    "options": ["are", "is", "am"],
                    "answer": "is",
                    "explanation": "It = 3rd person singular, dùng 'is'"
                },
                {
                    "text": "The dog ___ in the garden.",
                    "options": ["run", "runs", "running"],
                    "answer": "runs",
                    "explanation": "The dog = singular, động từ thêm 's'"
                },
                {
                    "text": "He ___ me a book.",
                    "options": ["give", "gives", "giving"],
                    "answer": "gives",
                    "explanation": "He = 3rd person singular, động từ thêm 's'"
                }
            ]
        },
        "VOCABULARY_CHOICE": {
            "questions": [
                {
                    "text": "I ___ in a comfortable bed.",
                    "options": ["sleep", "dream", "rest"],
                    "answer": "sleep",
                    "explanation": "'Sleep in a bed' = ngủ trên giường (đúng)"
                },
                {
                    "text": "She ___ a cup of tea.",
                    "options": ["drink", "eat", "taste"],
                    "answer": "drink",
                    "explanation": "'Drink tea' = uống trà (đúng)"
                },
                {
                    "text": "They ___ the meeting yesterday.",
                    "options": ["join", "attend", "participate"],
                    "answer": "attend",
                    "explanation": "'Attend a meeting' = tham dự cuộc họp"
                },
                {
                    "text": "I ___ my homework every day.",
                    "options": ["make", "do", "perform"],
                    "answer": "do",
                    "explanation": "'Do homework' = làm bài tập (collocation)"
                },
                {
                    "text": "She ___ a beautiful song.",
                    "options": ["speak", "sing", "say"],
                    "answer": "sing",
                    "explanation": "'Sing a song' = hát bài hát (đúng)"
                }
            ]
        },
        "WORD_ORDER": {
            "questions": [
                {
                    "text": "What time ___ you arrive?",
                    "options": ["do", "are", "can"],
                    "answer": "do",
                    "explanation": "Question: What time + do + you + verb?"
                },
                {
                    "text": "Where ___ they live?",
                    "options": ["do", "are", "can"],
                    "answer": "do",
                    "explanation": "Question: Where + do + they + live?"
                },
                {
                    "text": "I like very much this book.",
                    "options": ["I like this book very much", "I very like this book", "I like very much this book"],
                    "answer": "I like this book very much",
                    "explanation": "Adverb of degree đứng trước object: S + V + O + adv"
                },
                {
                    "text": "___ you understand this lesson?",
                    "options": ["Do", "Are", "Can"],
                    "answer": "Do",
                    "explanation": "Yes/No question: Do + you + understand?"
                },
                {
                    "text": "He speaks English very ___.",
                    "options": ["good", "well", "better"],
                    "answer": "well",
                    "explanation": "Sau 'speaks' (verb) dùng adverb 'well'"
                }
            ]
        }
    }
    
    @staticmethod
    def generate(error_type: str, skill_tag: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate practice questions based on error type"""
        try:
            if error_type in PracticeGenerator.TEMPLATES:
                template_questions = PracticeGenerator.TEMPLATES[error_type]["questions"]
                # Return first 'count' questions
                return template_questions[:count]
            else:
                # Fallback for unknown error types
                logger.warning(f"No template for error type: {error_type}")
                return PracticeGenerator._generate_generic(skill_tag, count)
        except Exception as e:
            logger.error(f"Failed to generate practice: {e}")
            return []
    
    @staticmethod
    def _generate_generic(skill_tag: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate generic practice questions"""
        return [
            {
                "text": "Fill in the blank with correct word",
                "answer": "example",
                "explanation": "This is a generic practice question",
                "difficulty": "beginner"
            }
        ] * count
    
    @staticmethod
    def check_answer(user_answer: str, question: Dict[str, Any]) -> Dict[str, Any]:
        """Check if user's answer is correct"""
        try:
            correct_answer = question.get("answer", "").lower().strip()
            user_answer_clean = user_answer.lower().strip()
            
            is_correct = user_answer_clean == correct_answer
            
            return {
                "is_correct": is_correct,
                "correct_answer": question.get("answer"),
                "explanation": question.get("explanation", ""),
                "feedback": "✅ Đúng rồi!" if is_correct else "❌ Chưa đúng"
            }
        except Exception as e:
            logger.error(f"Failed to check answer: {e}")
            return {"is_correct": False, "error": str(e)}
