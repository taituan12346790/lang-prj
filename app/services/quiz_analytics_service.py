"""
Quiz Analytics Service - Phân tích điểm yếu và tạo feedback chi tiết
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from ..models.user_topic_progress import UserTopicProgress
from ..models.exercise_result import ExerciseResult
from ..models.user import User
import json


class QuizAnalyticsService:
    """Service xử lý phân tích quiz và tạo feedback thông minh"""
    
    @staticmethod
    def analyze_quiz_results(
        quiz_data: List[Dict[str, Any]],
        user_answers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Phân tích kết quả quiz chi tiết
        
        Args:
            quiz_data: Danh sách câu hỏi với metadata
            user_answers: Dict {question_id: user_answer}
            
        Returns:
            {
                "score": float,
                "passed": bool,
                "correct_count": int,
                "total_count": int,
                "results": [...],  # Chi tiết từng câu
                "weak_skills": {...},  # Skill nào cần cải thiện
                "feedback": str
            }
        """
        results = []
        correct_count = 0
        skill_performance = {}  # {skill_tag: {"correct": int, "total": int}}
        
        for q in quiz_data:
            qid = q["id"]
            user_ans = user_answers.get(qid, "")
            # Try multiple possible keys for correct answer
            correct_ans = q.get("correct_answer") or q.get("correct") or q.get("answer", "")
            
            # Handle None values safely
            user_ans_clean = (user_ans or "").strip().lower()
            correct_ans_clean = (correct_ans or "").strip().lower()
            is_correct = user_ans_clean == correct_ans_clean
            
            if is_correct:
                correct_count += 1
            
            # Track skill performance
            skill_tag = q.get("skill_tag", "general")
            if skill_tag not in skill_performance:
                skill_performance[skill_tag] = {"correct": 0, "total": 0}
            
            skill_performance[skill_tag]["total"] += 1
            if is_correct:
                skill_performance[skill_tag]["correct"] += 1
            
            results.append({
                "question": q["question"],
                "your_answer": user_ans,
                "correct_answer": correct_ans,
                "is_correct": is_correct,
                "explanation": q.get("explanation", ""),
                "skill_tag": skill_tag
            })
        
        total_count = len(quiz_data)
        score = (correct_count / total_count * 100) if total_count > 0 else 0
        passed = score >= 70
        
        # Calculate weak skills (< 60% accuracy)
        weak_skills = {}
        for skill, perf in skill_performance.items():
            accuracy = perf["correct"] / perf["total"] if perf["total"] > 0 else 0
            if accuracy < 0.6:  # Weak if < 60%
                weak_skills[skill] = round(accuracy, 2)
        
        # Generate feedback
        feedback = QuizAnalyticsService._generate_feedback(
            score, passed, weak_skills, correct_count, total_count
        )
        
        return {
            "score": round(score, 1),
            "passed": passed,
            "correct_count": correct_count,
            "total_count": total_count,
            "results": results,
            "weak_skills": weak_skills,
            "feedback": feedback,
            "skill_performance": skill_performance
        }
    
    @staticmethod
    def _generate_feedback(
        score: float,
        passed: bool,
        weak_skills: Dict[str, float],
        correct: int,
        total: int
    ) -> str:
        """Tạo feedback văn bản dựa trên kết quả"""
        if score >= 90:
            feedback = f"🎉 Xuất sắc! Bạn trả lời đúng {correct}/{total} câu."
        elif score >= 80:
            feedback = f"👏 Rất tốt! Bạn đã nắm vững phần lớn nội dung ({correct}/{total} đúng)."
        elif score >= 70:
            feedback = f"✅ Đạt yêu cầu! Bạn trả lời đúng {correct}/{total} câu."
        elif score >= 50:
            feedback = f"📚 Cần cố gắng thêm. Bạn đúng {correct}/{total} câu."
        else:
            feedback = f"💪 Hãy ôn lại bài và thử lại. Bạn đúng {correct}/{total} câu."
        
        if weak_skills:
            skills_text = ", ".join([
                f"{skill.replace('_', ' ').title()} ({int(acc*100)}%)" 
                for skill, acc in weak_skills.items()
            ])
            feedback += f"\n⚠️ Cần cải thiện: {skills_text}"
        
        return feedback
    
    @staticmethod
    def save_weak_skills_to_progress(
        db: Session,
        user_id: str,
        topic_id: str,
        weak_skills: Dict[str, float]
    ):
        """Lưu weak skills vào UserTopicProgress để tracking"""
        progress = db.query(UserTopicProgress).filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.topic_id == topic_id
        ).first()
        
        if progress:
            # Merge với weak_skills cũ (nếu có)
            existing_weak = progress.weak_skills or {}
            existing_weak.update(weak_skills)
            progress.weak_skills = existing_weak
            db.commit()
    
    @staticmethod
    def calculate_next_review_date(
        quiz_attempts: int,
        quiz_score: float
    ) -> datetime:
        """
        Tính ngày ôn tập tiếp theo theo spaced repetition
        
        Thuật toán đơn giản:
        - Điểm >= 90: Ôn sau 7 ngày
        - Điểm >= 80: Ôn sau 3 ngày
        - Điểm >= 70: Ôn sau 1 ngày
        - Điểm < 70: Ôn ngay hôm sau
        
        Nếu đã làm nhiều lần, tăng khoảng cách
        """
        from datetime import timezone as tz
        
        if quiz_score >= 90:
            days = 7 * (1 + quiz_attempts * 0.5)  # Càng làm nhiều càng dãn ra
        elif quiz_score >= 80:
            days = 3 * (1 + quiz_attempts * 0.3)
        elif quiz_score >= 70:
            days = 1 * (1 + quiz_attempts * 0.2)
        else:
            days = 1  # Phải ôn lại sớm
        
        return datetime.now(tz.utc) + timedelta(days=int(days))
    
    @staticmethod
    async def update_study_streak(db: AsyncSession, user_id: UUID):
        """
        Cập nhật study streak của user (async version)
        Nếu học hôm nay → tăng streak
        Nếu bỏ quá 1 ngày → reset streak = 1
        """
        from sqlalchemy import select
        from datetime import timezone as tz
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return
        
        today = datetime.now(tz.utc).date()
        last_study = user.last_study_date.date() if user.last_study_date else None
        
        if last_study is None:
            # Lần đầu học
            user.study_streak = 1
            user.last_study_date = datetime.now(tz.utc)
        elif last_study == today:
            # Đã học hôm nay rồi, không thay đổi
            pass
        elif last_study == today - timedelta(days=1):
            # Học liên tục, tăng streak
            user.study_streak += 1
            user.last_study_date = datetime.now(tz.utc)
        else:
            # Bỏ quá 1 ngày, reset streak
            user.study_streak = 1
            user.last_study_date = datetime.now(tz.utc)
        
        await db.commit()
    
    @staticmethod
    async def get_due_reviews(db: AsyncSession, user_id: str) -> List[Dict]:
        """Lấy danh sách topics cần ôn tập hôm nay"""
        from sqlalchemy import select
        from datetime import datetime
        
        today = datetime.now()
        
        result = await db.execute(
            select(UserTopicProgress).where(
                UserTopicProgress.user_id == user_id,
                UserTopicProgress.status == "completed",
                UserTopicProgress.next_review_date <= today
            )
        )
        due_topics = result.scalars().all()
        
        return [
            {
                "topic_id": str(p.topic_id),
                "last_score": p.quiz_score,
                "next_review_date": p.next_review_date.isoformat() if p.next_review_date else None,
                "weak_skills": p.weak_skills or {}
            }
            for p in due_topics
        ]
    
    @staticmethod
    async def get_skill_breakdown(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """
        Phân tích performance theo từng skill của user
        
        Returns:
            {
                "grammar_past_tense": {"correct": 10, "total": 15, "accuracy": 0.67},
                "vocabulary_food": {"correct": 8, "total": 10, "accuracy": 0.80},
                ...
            }
        """
        from sqlalchemy import select
        
        # Query all exercise results
        result = await db.execute(
            select(ExerciseResult).where(
                ExerciseResult.user_id == user_id
            )
        )
        results = result.scalars().all()
        
        skill_stats = {}
        for r in results:
            skill = r.skill_tag
            if skill not in skill_stats:
                skill_stats[skill] = {"correct": 0, "total": 0}
            
            skill_stats[skill]["total"] += 1
            if r.is_correct:
                skill_stats[skill]["correct"] += 1
        
        # Calculate accuracy
        for skill in skill_stats:
            total = skill_stats[skill]["total"]
            correct = skill_stats[skill]["correct"]
            skill_stats[skill]["accuracy"] = round(correct / total, 2) if total > 0 else 0
        
        return skill_stats
    
    @staticmethod
    async def get_learning_timeline(
        db: AsyncSession,
        user_id: str,
        days: int = 30
    ) -> List[Dict]:
        """
        Lấy timeline học tập của user trong N ngày gần đây
        
        Returns:
            [
                {"date": "2026-06-01", "score": 85, "topics_completed": 2},
                ...
            ]
        """
        start_date = datetime.now() - timedelta(days=days)
        
        result = await db.execute(
            select(UserTopicProgress).where(
                UserTopicProgress.user_id == user_id,
                UserTopicProgress.last_activity >= start_date
            ).order_by(UserTopicProgress.last_activity.desc())
        )
        progress_records = result.scalars().all()
        
        # Group by date
        timeline = {}
        for p in progress_records:
            date_key = p.last_activity.date().isoformat()
            if date_key not in timeline:
                timeline[date_key] = {
                    "date": date_key,
                    "scores": [],
                    "topics_completed": 0
                }
            
            if p.quiz_score:
                timeline[date_key]["scores"].append(p.quiz_score)
            if p.status == "completed":
                timeline[date_key]["topics_completed"] += 1
        
        # Calculate average score per day
        result_list = []
        for date_key, data in sorted(timeline.items()):
            avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
            result_list.append({
                "date": data["date"],
                "score": round(avg_score, 1),
                "topics_completed": data["topics_completed"]
            })
        
        return result_list
