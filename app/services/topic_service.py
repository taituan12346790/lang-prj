# app/services/topic_service.py
"""
Service xử lý toàn bộ logic Learning Path:
- Lấy danh sách chủ đề theo level
- Theo dõi tiến độ học
- Submit quiz & tính điểm
- Kiểm tra điều kiện Level-Up
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from loguru import logger

from app.models.topic import Topic
from app.models.lesson import Lesson
from app.models.user_topic_progress import UserTopicProgress
from app.models.user_profile import UserProfile
from app.schemas.learning import (
    TopicResponse, TopicDetailResponse, TopicProgressInfo, TopicStatus,
    LevelProgressResponse, DashboardResponse,
    LessonSummary, LessonResponse,
    QuizQuestionsResponse, QuizQuestion,
    QuizSubmitRequest, QuizSubmitResponse, QuizQuestionResult,
    UpdateLessonProgressResponse,
)


# ─────────────────────────────────────────────────────────────
# Helper: seed topics into DB (called at startup if empty)
# ─────────────────────────────────────────────────────────────

async def seed_topics_if_empty(db: AsyncSession) -> None:
    """Seed A1 topics into DB if the topics table is empty."""
    from app.data.topics_data import get_all_topics
    result = await db.execute(select(func.count()).select_from(Topic))
    count = result.scalar()
    if count and count > 0:
        return  # Already seeded

    logger.info("🌱 Seeding topics into database...")
    topics_data = get_all_topics()

    for t_data in topics_data:
        lessons_data = t_data.pop("lessons", [])

        topic = Topic(**t_data)
        db.add(topic)
        await db.flush()  # get topic.id

        for l_data in lessons_data:
            lesson = Lesson(topic_id=topic.id, **l_data)
            db.add(lesson)

    await db.commit()
    logger.success(f"✅ Seeded {len(topics_data)} topics")


# ─────────────────────────────────────────────────────────────
# Helper: merge progress into topic response
# ─────────────────────────────────────────────────────────────

def _progress_info(prog: Optional[UserTopicProgress]) -> TopicProgressInfo:
    if not prog:
        return TopicProgressInfo()
    return TopicProgressInfo(
        status=TopicStatus(prog.status),
        lesson_completed=prog.lesson_completed or 0,
        quiz_score=prog.quiz_score,
        quiz_attempts=prog.quiz_attempts or 0,
        started_at=prog.started_at,
        completed_at=prog.completed_at,
    )


def _topic_to_response(topic: Topic, prog: Optional[UserTopicProgress]) -> TopicResponse:
    return TopicResponse(
        id=topic.id,
        level=topic.level,
        order=topic.order,
        name=topic.name,
        name_vi=topic.name_vi,
        description=topic.description,
        description_vi=topic.description_vi,
        grammar_focus=topic.grammar_focus or [],
        vocabulary_tags=topic.vocabulary_tags or [],
        estimated_minutes=topic.estimated_minutes or 30,
        lesson_count=len(topic.lessons) if topic.lessons else 5,
        progress=_progress_info(prog),
    )


# ─────────────────────────────────────────────────────────────
# TopicService
# ─────────────────────────────────────────────────────────────

class TopicService:

    # ── Topics List ──────────────────────────────────────────

    async def get_topics_by_level(
        self, level: str, user_id: UUID, db: AsyncSession
    ) -> List[TopicResponse]:
        """Danh sách chủ đề + tiến độ của user theo level."""
        # Ensure topics are seeded
        await seed_topics_if_empty(db)

        result = await db.execute(
            select(Topic)
            .where(Topic.level == level.upper(), Topic.is_active == True)
            .order_by(Topic.order)
            .options(selectinload(Topic.lessons))  # Eager load lessons
        )
        topics = result.scalars().unique().all()

        # Fetch all progress for this user in one query
        prog_result = await db.execute(
            select(UserTopicProgress)
            .where(UserTopicProgress.user_id == user_id)
        )
        prog_map: Dict[UUID, UserTopicProgress] = {
            p.topic_id: p for p in prog_result.scalars().all()
        }

        return [_topic_to_response(t, prog_map.get(t.id)) for t in topics]

    # ── Topic Detail ─────────────────────────────────────────

    async def get_topic_detail(
        self, topic_id: UUID, user_id: UUID, db: AsyncSession
    ) -> Optional[TopicDetailResponse]:
        result = await db.execute(
            select(Topic)
            .where(Topic.id == topic_id)
            .options(selectinload(Topic.lessons))
        )
        topic = result.scalar_one_or_none()
        if not topic:
            return None

        # Progress
        prog_result = await db.execute(
            select(UserTopicProgress).where(
                UserTopicProgress.user_id == user_id,
                UserTopicProgress.topic_id == topic_id,
            )
        )
        prog = prog_result.scalar_one_or_none()

        # Lessons (from eager loaded relationship)
        lessons = topic.lessons if topic.lessons else []

        lesson_summaries = [
            LessonSummary(
                id=l.id, order=l.order,
                lesson_type=l.lesson_type,
                title=l.title, title_vi=l.title_vi,
            )
            for l in lessons
        ]

        base = _topic_to_response(topic, prog)
        return TopicDetailResponse(
            **base.model_dump(),
            lessons=lesson_summaries,
        )

    # ── Lesson Content ────────────────────────────────────────

    async def get_lesson(
        self, lesson_id: UUID, db: AsyncSession
    ) -> Optional[LessonResponse]:
        result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = result.scalar_one_or_none()
        if not lesson:
            return None
        return LessonResponse(
            id=lesson.id, topic_id=lesson.topic_id,
            order=lesson.order, lesson_type=lesson.lesson_type,
            title=lesson.title, title_vi=lesson.title_vi,
            content=lesson.content or {},
        )

    # ── Update Lesson Progress ────────────────────────────────

    async def complete_lesson(
        self, topic_id: UUID, lesson_order: int, user_id: UUID, db: AsyncSession
    ) -> UpdateLessonProgressResponse:
        """Mark a lesson as completed, update UserTopicProgress."""
        # Get or create progress record
        prog_result = await db.execute(
            select(UserTopicProgress).where(
                UserTopicProgress.user_id == user_id,
                UserTopicProgress.topic_id == topic_id,
            )
        )
        prog = prog_result.scalar_one_or_none()

        now = datetime.now(timezone.utc)
        if not prog:
            prog = UserTopicProgress(
                user_id=user_id,
                topic_id=topic_id,
                status="in_progress",
                lesson_completed=lesson_order,
                started_at=now,
            )
            db.add(prog)
        else:
            if lesson_order > (prog.lesson_completed or 0):
                prog.lesson_completed = lesson_order
            if prog.status == "not_started":
                prog.status = "in_progress"
                prog.started_at = now

        await db.commit()
        await db.refresh(prog)
        
        # P2.5: DISABLED C3 - Let orchestrator handle next step suggestion
        # Agent should suggest GO_TO_LESSON, not backend auto-activate
        # C3: Auto-activate next lesson if available
        # try:
        #     next_lesson_order = lesson_order + 1
        #     next_lesson_result = await db.execute(
        #         select(Lesson).where(
        #             Lesson.topic_id == topic_id,
        #             Lesson.order == next_lesson_order
        #         )
        #     )
        #     next_lesson = next_lesson_result.scalar_one_or_none()
        #     
        #     if next_lesson:
        #         # Activate next lesson
        #         await self.set_active_context(
        #             user_id=user_id,
        #             topic_id=str(topic_id),  # Convert UUID to string
        #             lesson_order=next_lesson_order,
        #             learning_mode="lesson",
        #             db=db
        #         )
        #         logger.info(f"✨ C3: Auto-activated next lesson {next_lesson_order} for user {user_id}")
        # except Exception as e:
        #     logger.warning(f"C3: Failed to auto-activate next lesson: {e}")

        return UpdateLessonProgressResponse(
            topic_id=topic_id,
            lesson_completed=prog.lesson_completed,
            status=TopicStatus(prog.status),
            message=f"Lesson {lesson_order} completed! ✅",
        )

    # ── Quiz ─────────────────────────────────────────────────

    async def get_quiz_questions(
        self, topic_id: UUID, db: AsyncSession
    ) -> Optional[QuizQuestionsResponse]:
        """Get the quiz lesson's questions (without correct answers)."""
        result = await db.execute(
            select(Lesson).where(
                Lesson.topic_id == topic_id,
                Lesson.lesson_type == "quiz",
            )
        )
        lesson = result.scalar_one_or_none()
        if not lesson:
            return None

        topic_result = await db.execute(select(Topic).where(Topic.id == topic_id))
        topic = topic_result.scalar_one_or_none()

        raw_questions = (lesson.content or {}).get("questions", [])
        safe_questions = [
            QuizQuestion(
                id=q["id"],
                question=q["question"],
                question_vi=q.get("question_vi"),  # ADD THIS
                options=q["options"],
            )
            for q in raw_questions
        ]

        return QuizQuestionsResponse(
            topic_id=topic_id,
            topic_name=topic.name if topic else "",
            questions=safe_questions,
            total=len(safe_questions),
        )

    async def submit_quiz(
        self,
        topic_id: UUID,
        user_id: UUID,
        request: QuizSubmitRequest,
        db: AsyncSession,
    ) -> QuizSubmitResponse:
        """Grade quiz, update progress, return detailed results with analytics."""
        from app.services.quiz_analytics_service import QuizAnalyticsService
        
        # Get quiz lesson
        result = await db.execute(
            select(Lesson).where(
                Lesson.topic_id == topic_id,
                Lesson.lesson_type == "quiz",
            )
        )
        lesson = result.scalar_one_or_none()
        if not lesson:
            raise ValueError("Quiz lesson not found")

        raw_questions = (lesson.content or {}).get("questions", [])
        answers = request.answers

        # Grade using Analytics Service
        analysis = QuizAnalyticsService.analyze_quiz_results(
            raw_questions,
            answers
        )
        
        score = analysis["score"]
        passed = analysis["passed"]
        correct_count = analysis["correct_count"]
        total = analysis["total_count"]
        results_list = analysis["results"]
        weak_skills = analysis["weak_skills"]
        feedback = analysis["feedback"]

        # Convert to schema format
        results: List[QuizQuestionResult] = []
        for r in results_list:
            results.append(QuizQuestionResult(
                id=str(hash(r["question"]))[:8],  # Generate consistent ID
                question=r["question"],
                your_answer=r["your_answer"],
                correct_answer=r["correct_answer"],
                is_correct=r["is_correct"],
                explanation=r["explanation"],
            ))

        # Update progress
        prog_result = await db.execute(
            select(UserTopicProgress).where(
                UserTopicProgress.user_id == user_id,
                UserTopicProgress.topic_id == topic_id,
            )
        )
        prog = prog_result.scalar_one_or_none()
        now = datetime.now(timezone.utc)

        topic_completed = False
        if not prog:
            prog = UserTopicProgress(
                user_id=user_id, topic_id=topic_id,
                status="in_progress", lesson_completed=5,
                quiz_score=score, quiz_attempts=1, started_at=now,
                weak_skills=weak_skills  # NEW: Save weak skills
            )
            db.add(prog)
        else:
            prog.quiz_attempts = (prog.quiz_attempts or 0) + 1
            # Keep best score
            if prog.quiz_score is None or score > prog.quiz_score:
                prog.quiz_score = score
            prog.lesson_completed = max(prog.lesson_completed or 0, 5)
            
            # Update weak skills
            prog.weak_skills = weak_skills

        if passed and (prog.status != "completed"):
            prog.status = "completed"
            prog.completed_at = now
            topic_completed = True
            
            # Calculate next review date for spaced repetition
            next_review = QuizAnalyticsService.calculate_next_review_date(
                prog.quiz_attempts, score
            )
            prog.next_review_date = next_review

        # Update study streak
        await QuizAnalyticsService.update_study_streak(db, user_id)

        await db.commit()
        
        # P2.2: DISABLED C3 - Let orchestrator suggest next topic via START_QUIZ for new topic
        # C3: Auto-activate next topic if quiz passed and topic completed
        # if passed and topic_completed:
        #     try:
        #         # Get current topic to find next topic
        #         topic_result = await db.execute(select(Topic).where(Topic.id == topic_id))
        #         current_topic = topic_result.scalar_one_or_none()
        #         
        #         if current_topic:
        #             # Find next topic in same level
        #             next_topic_result = await db.execute(
        #                 select(Topic)
        #                 .where(
        #                     Topic.level == current_topic.level,
        #                     Topic.order > current_topic.order,
        #                     Topic.is_active == True
        #                 )
        #                 .order_by(Topic.order)
        #                 .limit(1)
        #             )
        #             next_topic = next_topic_result.scalar_one_or_none()
        #             
        #             if next_topic:
        #                 # Activate first lesson of next topic
        #                 await self.set_active_context(
        #                     user_id=user_id,
        #                     topic_id=str(next_topic.id),  # Convert UUID to string
        #                     lesson_order=1,
        #                     learning_mode="topic",
        #                     db=db
        #                 )
        #                 logger.info(f"✨ C3: Auto-activated next topic {next_topic.id} for user {user_id}")
        #     except Exception as e:
        #         logger.warning(f"C3: Failed to auto-activate next topic: {e}")

        return QuizSubmitResponse(
            topic_id=topic_id,
            score=score,
            passed=passed,
            correct_count=correct_count,
            total_count=total,
            results=results,
            feedback=feedback,
            topic_completed=topic_completed,
        )

    # ── Dashboard ────────────────────────────────────────────

    async def get_dashboard(
        self, user_id: UUID, db: AsyncSession
    ) -> DashboardResponse:
        """Build dashboard data for the user."""
        # Get user profile for current level
        prof_result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = prof_result.scalar_one_or_none()
        current_level = profile.current_level if profile else "A1"

        topics = await self.get_topics_by_level(current_level, user_id, db)
        total = len(topics)
        completed = sum(1 for t in topics if t.progress.status == TopicStatus.COMPLETED)
        in_progress = sum(1 for t in topics if t.progress.status == TopicStatus.IN_PROGRESS)
        pct = round((completed / total) * 100, 1) if total > 0 else 0.0

        # Average quiz score (only for completed topics with scores)
        scores = [t.progress.quiz_score for t in topics
                  if t.progress.quiz_score is not None]
        avg_score = round(sum(scores) / len(scores), 1) if scores else None

        # Level-up eligibility: ≥75% topics completed AND avg quiz ≥70
        can_level_up = (
            current_level != "C2"
            and pct >= 75
            and (avg_score is None or avg_score >= 70)
        )
        lu_msg = (
            "🎉 Bạn đủ điều kiện làm bài kiểm tra nâng cấp!"
            if can_level_up else
            f"Hoàn thành {max(0, round(total * 0.75) - completed)} chủ đề nữa để mở khóa Level-Up Test."
        )

        # Next topic to study
        next_topic: Optional[TopicResponse] = None
        current_topic: Optional[TopicResponse] = None
        for t in topics:
            if t.progress.status == TopicStatus.IN_PROGRESS and not current_topic:
                current_topic = t
            if t.progress.status == TopicStatus.NOT_STARTED and not next_topic:
                next_topic = t

        # Recent completed (last 3)
        recent = [t for t in reversed(topics) if t.progress.status == TopicStatus.COMPLETED][:3]

        return DashboardResponse(
            current_level=current_level,
            level_progress=LevelProgressResponse(
                level=current_level,
                total_topics=total,
                completed_topics=completed,
                in_progress_topics=in_progress,
                completion_percentage=pct,
                average_quiz_score=avg_score,
                can_level_up=can_level_up,
                level_up_message=lu_msg,
            ),
            next_topic=next_topic,
            current_topic=current_topic,
            recent_completed=recent,
        )

    # ── Level eligibility (for existing level-up test router) ─

    async def check_level_up_eligibility(
        self, user_id: UUID, db: AsyncSession
    ) -> Dict[str, Any]:
        dashboard = await self.get_dashboard(user_id, db)
        lp = dashboard.level_progress
        return {
            "can_level_up": lp.can_level_up,
            "message": lp.level_up_message,
            "completion_percentage": lp.completion_percentage,
            "average_quiz_score": lp.average_quiz_score,
            "current_level": dashboard.current_level,
        }

    # ── Learning Context (Sprint 1) ──────────────────────────

    async def set_active_context(
        self,
        user_id: UUID,
        topic_id: str,
        lesson_order: Optional[int],
        learning_mode: str,
        db: AsyncSession,
    ) -> None:
        """Set active topic/lesson/mode on user profile."""
        prof_result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = prof_result.scalar_one_or_none()
        if not profile:
            raise ValueError(f"Profile not found for user {user_id}")

        # Ensure topic_id is string (convert UUID to str if needed)
        profile.active_topic_id = str(topic_id) if topic_id else None
        profile.active_lesson_order = lesson_order
        profile.learning_mode = learning_mode

        # Auto-mark topic as in_progress if not already
        if lesson_order is not None:
            from uuid import UUID as UUID_type
            try:
                topic_uuid = UUID_type(topic_id)
                prog_result = await db.execute(
                    select(UserTopicProgress).where(
                        UserTopicProgress.user_id == user_id,
                        UserTopicProgress.topic_id == topic_uuid,
                    )
                )
                prog = prog_result.scalar_one_or_none()
                if not prog:
                    prog = UserTopicProgress(
                        user_id=user_id,
                        topic_id=topic_uuid,
                        status="in_progress",
                        lesson_completed=0,
                        started_at=datetime.now(timezone.utc),
                    )
                    db.add(prog)
                elif prog.status == "not_started":
                    prog.status = "in_progress"
                    prog.started_at = datetime.now(timezone.utc)
            except Exception as e:
                logger.warning(f"Could not auto-progress topic: {e}")

        await db.commit()
        logger.info(f"✅ Set active context for {user_id}: topic={topic_id}, lesson={lesson_order}, mode={learning_mode}")

    async def get_learning_context(
        self,
        user_id: UUID,
        db: AsyncSession,
    ) -> Optional[Dict[str, Any]]:
        """Get current learning context for user with progress info."""
        from app.schemas.learning import LearningContextResponse
        from sqlalchemy import func
        
        prof_result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = prof_result.scalar_one_or_none()
        if not profile:
            return None

        topic_name = None
        topic_name_vi = None
        lesson_title = None
        lesson_type = None
        grammar_focus = []
        estimated_minutes = 0
        lesson_completed = 0
        total_lessons = 0
        quiz_score = None
        quiz_attempts = 0
        status = None

        if profile.active_topic_id:
            from uuid import UUID as UUID_type
            try:
                topic_uuid = UUID_type(profile.active_topic_id)
                topic_result = await db.execute(
                    select(Topic).where(Topic.id == topic_uuid)
                    .options(selectinload(Topic.lessons))
                )
                topic = topic_result.scalar_one_or_none()
                if topic:
                    topic_name = topic.name
                    topic_name_vi = topic.name_vi
                    grammar_focus = topic.grammar_focus or []
                    estimated_minutes = topic.estimated_minutes or 30
                    
                    # Count total lessons
                    total_lessons_result = await db.execute(
                        select(func.count(Lesson.id)).where(Lesson.topic_id == topic_uuid)
                    )
                    total_lessons = total_lessons_result.scalar()
                    
                    # Get progress
                    progress_result = await db.execute(
                        select(UserTopicProgress).where(
                            UserTopicProgress.user_id == user_id,
                            UserTopicProgress.topic_id == topic_uuid
                        )
                    )
                    progress = progress_result.scalar_one_or_none()
                    if progress:
                        lesson_completed = progress.lesson_completed
                        quiz_score = progress.quiz_score
                        quiz_attempts = progress.quiz_attempts
                        status = progress.status

                    # Find current lesson
                    if profile.active_lesson_order and topic.lessons:
                        lesson = next(
                            (l for l in topic.lessons if l.order == profile.active_lesson_order),
                            None,
                        )
                        if lesson:
                            lesson_title = lesson.title
                            lesson_type = lesson.lesson_type
            except Exception as e:
                logger.warning(f"Could not load topic context: {e}")

        return LearningContextResponse(
            active_topic_id=profile.active_topic_id,
            active_lesson_order=profile.active_lesson_order,
            learning_mode=profile.learning_mode,
            topic_name=topic_name,
            topic_name_vi=topic_name_vi,
            lesson_title=lesson_title,
            lesson_type=lesson_type,
            grammar_focus=grammar_focus,
            estimated_minutes=estimated_minutes,
            current_level=profile.current_level,
            lesson_completed=lesson_completed,
            total_lessons=total_lessons,
            quiz_score=quiz_score,
            quiz_attempts=quiz_attempts,
            status=status,
        ).model_dump()
