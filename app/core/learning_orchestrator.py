# app/core/learning_orchestrator.py
"""
Phase 3: Learning Orchestrator
Agent decides what action to suggest next based on learning state
"""
from typing import Dict, Any, Optional, List
from loguru import logger

from app.schemas.learning_action import SuggestedAction, SuggestedActionType

# Mapping skill_tag (code) → Vietnamese display name
SKILL_DISPLAY_NAMES = {
    "irregular_verbs": "động từ bất quy tắc",
    "regular_verbs": "động từ có quy tắc",
    "verb_conjugation": "chia động từ",
    "present_simple": "thì hiện tại đơn",
    "present_continuous": "thì hiện tại tiếp diễn",
    "past_simple": "thì quá khứ đơn",
    "past_continuous": "thì quá khứ tiếp diễn",
    "present_perfect": "thì hiện tại hoàn thành",
    "future_simple": "thì tương lai đơn",
    "articles": "mạo từ (a/an/the)",
    "prepositions": "giới từ",
    "pronouns": "đại từ",
    "possessive_adjectives": "tính từ sở hữu",
    "adjectives": "tính từ",
    "adverbs": "trạng từ",
    "sentence_structure": "cấu trúc câu",
    "question_formation": "đặt câu hỏi",
    "negative_sentences": "câu phủ định",
    "conditionals": "câu điều kiện",
    "passive_voice": "câu bị động",
    "modal_verbs": "động từ khiếm khuyết",
    "gerunds_infinitives": "danh động từ",
    "vocabulary": "từ vựng",
    "spelling": "chính tả",
    "punctuation": "dấu câu",
    "word_order": "trật tự từ",
    "countable_uncountable": "danh từ đếm được/không đếm được",
}


class LearningOrchestrator:
    """
    Orchestrator decides next action after each chat turn
    Based on: learning_context, analytics, reflection, strategy
    """
    
    @staticmethod
    def suggest_next_action(
        learning_context: Optional[Dict[str, Any]] = None,
        analytics_context: Optional[Dict[str, Any]] = None,
        reflection: Optional[Dict[str, Any]] = None,
        strategy_mode: Optional[str] = None,
        quiz_context: Optional[Dict[str, Any]] = None,
    ) -> List[SuggestedAction]:
        """
        Suggest 1-3 actions for user based on current state
        Returns list ordered by priority
        """
        actions: List[SuggestedAction] = []
        
        # Priority 1: Quiz review mode
        if quiz_context and quiz_context.get("wrong_answers"):
            actions.append(SuggestedAction(
                type=SuggestedActionType.QUIZ_REVIEW,
                label="📝 Làm bài tập ôn lỗi",
                reasoning="Bạn vừa làm quiz và có câu sai, nên luyện thêm",
                params={"quiz_context": quiz_context},
                confidence=0.95,
                priority=1
            ))
            return actions  # Quiz review is highest priority
        
        # Priority 2: Due reviews (spaced repetition)
        if analytics_context and analytics_context.get("needs_review"):
            due_count = analytics_context.get("due_reviews_count", 0)
            if due_count > 0:
                actions.append(SuggestedAction(
                    type=SuggestedActionType.REVIEW_WEAK_SKILL,
                    label=f"🔄 Ôn {due_count} chủ đề cũ",
                    reasoning="Đã đến lúc ôn lại kiến thức cũ (spaced repetition)",
                    params={"due_reviews_count": due_count},
                    confidence=0.85,
                    priority=1
                ))
        
        # Priority 3: Active lesson context
        if learning_context:
            lesson_type = learning_context.get("lesson_type")
            lesson_completed = learning_context.get("lesson_completed", 0)
            total_lessons = learning_context.get("total_lessons", 4)
            current_lesson_order = learning_context.get("current_lesson_order", 1)
            
            # Get topic_id for actions
            topic_id = learning_context.get("topic_id")
            
            # If user understanding is good (from reflection), suggest completion
            understanding = reflection.get("understanding", "fair") if reflection else "fair"
            engagement = reflection.get("engagement", "medium") if reflection else "medium"
            
            if lesson_type in ["grammar", "vocabulary"]:
                # If understanding is good, offer practice
                if understanding in ["good", "excellent"] and engagement in ["high", "medium"]:
                    actions.append(SuggestedAction(
                        type=SuggestedActionType.OFFER_PRACTICE,
                        label="✏️ Làm 3-5 câu luyện tập",
                        reasoning="Bạn đã hiểu bài, hãy thực hành để nhớ lâu hơn",
                        params={
                            "count": 5,
                            "topic_id": topic_id,
                            "lesson_order": current_lesson_order
                        },
                        confidence=0.9,
                        priority=1
                    ))
                
                # If practiced enough, suggest complete lesson
                if strategy_mode == "exercise" and understanding == "good":
                    actions.append(SuggestedAction(
                        type=SuggestedActionType.COMPLETE_LESSON,
                        label=f"✅ Hoàn thành bài {current_lesson_order}",
                        reasoning="Bạn đã luyện tập đủ, có thể chuyển bài mới",
                        params={
                            "topic_id": topic_id,
                            "lesson_order": current_lesson_order
                        },
                        confidence=0.85,
                        priority=2
                    ))
                    
                    # P2.6: After COMPLETE_LESSON, suggest GO_TO_LESSON for next lesson
                    if current_lesson_order < total_lessons:
                        next_lesson_order = current_lesson_order + 1
                        actions.append(SuggestedAction(
                            type=SuggestedActionType.GO_TO_LESSON,
                            label=f"📖 Chuyển sang bài {next_lesson_order}",
                            reasoning=f"Tiếp tục học bài {next_lesson_order}",
                            params={
                                "topic_id": topic_id,
                                "lesson_order": next_lesson_order
                            },
                            confidence=0.8,
                            priority=2
                        ))
            
            # If all lessons done, suggest quiz
            if lesson_completed >= total_lessons and lesson_completed > 0:
                quiz_score = learning_context.get("quiz_score")
                if quiz_score is None or quiz_score < 70:
                    actions.append(SuggestedAction(
                        type=SuggestedActionType.START_QUIZ,
                        label="🎯 Làm quiz kiểm tra",
                        reasoning="Bạn đã học xong tất cả bài, hãy kiểm tra kiến thức",
                        params={"topic_id": learning_context.get("topic_id")},
                        confidence=0.9,
                        priority=1
                    ))
        
        # Priority 4: Level-up eligibility
        if analytics_context and analytics_context.get("level_eligible"):
            actions.append(SuggestedAction(
                type=SuggestedActionType.START_LEVEL_UP_TEST,
                label="🚀 Thi lên level cao hơn",
                reasoning="Bạn đã đủ điều kiện để thi lên level!",
                params={"current_level": analytics_context.get("current_level", "A1")},
                confidence=0.95,
                priority=1
            ))
        
        # Default: Suggest based on weak skills or start new topic
        if not actions:
            # Priority: Review weakest skill if available
            if analytics_context:
                weak_skills = analytics_context.get("weak_skills", {})
                if weak_skills:
                    # Get weakest skill (lowest accuracy)
                    weakest_skill_tag, accuracy = min(weak_skills.items(), key=lambda x: x[1])
                    
                    # Convert skill_tag to Vietnamese display name
                    skill_display = SKILL_DISPLAY_NAMES.get(weakest_skill_tag, weakest_skill_tag.replace("_", " "))
                    
                    actions.append(SuggestedAction(
                        type=SuggestedActionType.REVIEW_WEAK_SKILL,
                        label=f"🔄 Ôn lại {skill_display}",
                        reasoning=f"Bạn còn yếu về {skill_display} ({int(accuracy*100)}% độ chính xác)",
                        params={"skill_tag": weakest_skill_tag, "skill_name": skill_display},
                        confidence=0.85,
                        priority=1
                    ))
        
        # If still no actions and no active learning context, suggest start new topic
        if not actions and not learning_context:
            actions.append(SuggestedAction(
                type=SuggestedActionType.FREE_CHAT,
                label="📚 Bắt đầu chủ đề học mới",
                reasoning="Chọn chủ đề từ 190 topics CEFR (A1-B2) để bắt đầu học có hệ thống",
                params={},
                confidence=0.75,
                priority=2
            ))
        
        # Sort by priority (1=highest)
        actions.sort(key=lambda a: a.priority)
        
        # Return top 3 (or empty if no meaningful suggestions)
        return actions[:3]
