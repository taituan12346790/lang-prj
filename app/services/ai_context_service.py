"""
AI Context Service - Cung cấp context từ bài học cho AI Chat
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from ..models.user_topic_progress import UserTopicProgress
from ..models.topic import Topic
from ..models.lesson import Lesson
from ..models.exercise_result import ExerciseResult


class AIContextService:
    """Service tạo context-aware prompts cho AI"""
    
    @staticmethod
    def build_learning_context(
        db: Session,
        user_id: str,
        topic_id: Optional[str] = None,
        lesson_id: Optional[str] = None
    ) -> str:
        """
        Tạo context string cho AI dựa trên:
        - Topic hiện tại (nếu có)
        - Lesson hiện tại (nếu có)
        - Weak skills của user
        - Recent mistakes
        
        Returns:
            Context string để thêm vào system prompt của AI
        """
        context_parts = []
        
        # 1. Current topic & lesson
        if topic_id:
            topic = db.query(Topic).filter(Topic.id == topic_id).first()
            if topic:
                context_parts.append(f"📚 Current Topic: {topic.name} ({topic.name_vi})")
                context_parts.append(f"Description: {topic.description}")
                
                # Get progress
                progress = db.query(UserTopicProgress).filter(
                    UserTopicProgress.user_id == user_id,
                    UserTopicProgress.topic_id == topic_id
                ).first()
                
                if progress:
                    context_parts.append(f"Progress: {progress.lesson_completed}/5 lessons completed")
                    if progress.quiz_score:
                        context_parts.append(f"Last quiz score: {progress.quiz_score}%")
                    
                    if progress.weak_skills:
                        weak_list = [f"{k} ({v*100:.0f}%)" for k, v in progress.weak_skills.items()]
                        context_parts.append(f"⚠️ Weak skills: {', '.join(weak_list)}")
        
        if lesson_id:
            lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
            if lesson:
                context_parts.append(f"📖 Current Lesson: {lesson.title}")
                context_parts.append(f"Type: {lesson.lesson_type}")
        
        # 2. Recent mistakes (last 5)
        recent_mistakes = db.query(ExerciseResult).filter(
            ExerciseResult.user_id == user_id,
            ExerciseResult.is_correct == False
        ).order_by(ExerciseResult.created_at.desc()).limit(5).all()
        
        if recent_mistakes:
            context_parts.append("\n🔍 Recent Mistakes:")
            for i, err in enumerate(recent_mistakes, 1):
                context_parts.append(
                    f"{i}. [{err.skill_tag}] User answered: '{err.user_answer}' "
                    f"(correct: '{err.expected_answer}')"
                )
        
        # 3. Overall skill assessment
        skill_summary = AIContextService._get_skill_summary(db, user_id)
        if skill_summary:
            context_parts.append("\n📊 Skill Summary:")
            for skill, acc in sorted(skill_summary.items(), key=lambda x: x[1]):
                emoji = "✅" if acc >= 0.7 else "⚠️" if acc >= 0.5 else "❌"
                context_parts.append(f"{emoji} {skill}: {acc*100:.0f}%")
        
        return "\n".join(context_parts)
    
    @staticmethod
    def _get_skill_summary(db: Session, user_id: str) -> Dict[str, float]:
        """Lấy tóm tắt accuracy theo từng skill"""
        results = db.query(ExerciseResult).filter(
            ExerciseResult.user_id == user_id
        ).all()
        
        skill_stats = {}
        for r in results:
            skill = r.skill_tag
            if skill not in skill_stats:
                skill_stats[skill] = {"correct": 0, "total": 0}
            
            skill_stats[skill]["total"] += 1
            if r.is_correct:
                skill_stats[skill]["correct"] += 1
        
        return {
            skill: stats["correct"] / stats["total"]
            for skill, stats in skill_stats.items()
            if stats["total"] > 0
        }
    
    @staticmethod
    def generate_system_prompt_with_context(
        base_prompt: str,
        learning_context: str
    ) -> str:
        """
        Kết hợp base system prompt với learning context
        
        Args:
            base_prompt: Prompt gốc (role: language tutor)
            learning_context: Context từ build_learning_context()
            
        Returns:
            Enhanced system prompt
        """
        enhanced = f"""{base_prompt}

--- STUDENT LEARNING CONTEXT ---
{learning_context}

IMPORTANT INSTRUCTIONS:
1. Use the context above to provide personalized help
2. Focus on weak skills mentioned in the context
3. When explaining, reference their recent mistakes
4. Adjust difficulty based on their current topic level
5. Encourage them based on their progress
6. If they ask about quiz questions, explain the correct answer and WHY it's correct
---
"""
        return enhanced
    
    @staticmethod
    def suggest_exercises_for_weak_skills(
        weak_skills: Dict[str, float],
        target_count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Đề xuất prompt để AI generate bài tập cho weak skills
        
        Args:
            weak_skills: {skill_tag: accuracy}
            target_count: Số bài tập cần generate
            
        Returns:
            List of exercise generation prompts
        """
        suggestions = []
        
        for skill, accuracy in sorted(weak_skills.items(), key=lambda x: x[1]):
            # Determine difficulty based on accuracy
            if accuracy < 0.3:
                difficulty = "basic"
            elif accuracy < 0.5:
                difficulty = "easy"
            else:
                difficulty = "medium"
            
            suggestions.append({
                "skill_tag": skill,
                "difficulty": difficulty,
                "accuracy": accuracy,
                "prompt": f"Generate {target_count} {difficulty} exercises for {skill.replace('_', ' ')}. "
                         f"Focus on common mistakes. Format: Question, Options (A/B/C/D), Correct Answer, Explanation."
            })
        
        return suggestions
    
    @staticmethod
    def build_quiz_review_context(
        quiz_results: List[Dict[str, Any]]
    ) -> str:
        """
        Tạo context từ kết quả quiz để AI có thể giải thích chi tiết
        
        Args:
            quiz_results: List từ QuizAnalyticsService.analyze_quiz_results()["results"]
            
        Returns:
            Context string với wrong answers
        """
        wrong_answers = [r for r in quiz_results if not r["is_correct"]]
        
        if not wrong_answers:
            return "🎉 All answers are correct! Great job!"
        
        context_parts = ["❌ INCORRECT ANSWERS TO EXPLAIN:"]
        
        for i, wrong in enumerate(wrong_answers, 1):
            context_parts.append(
                f"\n{i}. Q: {wrong['question']}\n"
                f"   Student answered: {wrong['your_answer']}\n"
                f"   Correct answer: {wrong['correct_answer']}\n"
                f"   Skill: {wrong['skill_tag']}"
            )
        
        context_parts.append(
            "\n💡 TASK: Explain each wrong answer above in simple terms. "
            "Why was their answer incorrect? What's the correct rule/concept? "
            "Provide 1-2 similar practice examples."
        )
        
        return "\n".join(context_parts)
