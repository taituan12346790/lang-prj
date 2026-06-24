from typing import Dict, Any, Optional
from uuid import UUID
from loguru import logger
from langgraph.graph import StateGraph, END
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.graph_state import AgentState
from app.core.strategy import StrategySelector
from app.core.planner import ReActPlanner
from app.core.pipeline import Pipeline
from app.core.reflector_enhanced import ReflectorEnhanced
from app.core.learning_orchestrator import LearningOrchestrator
from app.memory.memory_service import MemoryService
from app.services.quiz_analytics_service import QuizAnalyticsService
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.topic import Topic
from app.models.lesson import Lesson
from app.models.user_topic_progress import UserTopicProgress


class LearningService:
    """Learning Service sử dụng LangGraph - production ready"""

    def __init__(self):
        self.memory = MemoryService()
        self.strategy_selector = StrategySelector()
        self.planner = ReActPlanner()
        self.pipeline = Pipeline()
        self.reflector = ReflectorEnhanced()
        self.orchestrator = LearningOrchestrator()  # Phase 3
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(AgentState)

        # Nodes
        graph.add_node("load_memory", self._load_memory_node)
        graph.add_node("select_strategy", self._strategy_node)  # Renamed to avoid conflict with state attribute
        graph.add_node("planner", self._planner_node)
        graph.add_node("execute", self._execute_node)
        graph.add_node("reflect", self._reflect_node)
        graph.add_node("orchestrate", self._orchestrate_node)  # Phase 3
        graph.add_node("update_memory", self._update_memory_node)

        # Entry point
        graph.set_entry_point("load_memory")

        # Conditional edges
        graph.add_conditional_edges(
            "load_memory",
            self._after_load_memory,
            {"continue": "select_strategy", "error": END}
        )
        graph.add_conditional_edges(
            "select_strategy",
            self._after_strategy,
            {"continue": "planner", "error": END}
        )
        graph.add_conditional_edges(
            "planner",
            self._after_planner,
            {"continue": "execute", "error": END}
        )
        graph.add_conditional_edges(
            "execute",
            self._after_execute,
            {"continue": "reflect", "error": END}
        )
        graph.add_edge("reflect", "orchestrate")  # Phase 3
        graph.add_edge("orchestrate", "update_memory")  # Phase 3
        graph.add_edge("update_memory", END)

        return graph.compile()

    # ========== Conditional routing ==========
    @staticmethod
    def _after_load_memory(state: AgentState) -> str:
        return "error" if state.get("error") else "continue"

    @staticmethod
    def _after_strategy(state: AgentState) -> str:
        return "error" if state.get("error") else "continue"

    @staticmethod
    def _after_planner(state: AgentState) -> str:
        return "error" if state.get("error") else "continue"

    @staticmethod
    def _after_execute(state: AgentState) -> str:
        return "error" if state.get("error") else "continue"

    # ========== Nodes ==========
    async def _load_memory_node(self, state: AgentState) -> Dict[str, Any]:
        """Load long-term và short-term memory + analytics context + learning context"""
        try:
            # A5: Load short-term from DB (last 5-10 messages from session)
            short_mem_from_db = await self._load_short_term_from_db(
                state["db"],
                state["user_id"],
                state.get("session_id")
            )
            
            # Load from MemoryService (may include RAM cache)
            short_mem, long_mem = await self.memory.load(state["user_id"], state["db"])
            
            # Merge: DB history has priority over RAM
            if short_mem_from_db:
                short_mem = short_mem_from_db  # Use DB conversation history
            
            # Load analytics context
            analytics_context = await self._build_analytics_context_async(state["db"], state["user_id"])
            
            # Load learning context (active topic/lesson) if available
            # IMPORTANT: Don't merge into long_mem, it needs to stay as UserProfile object
            # Instead, we'll enhance analytics_context with learning info
            learning_context = await self._build_learning_context_dict(state["db"], state["user_id"])
            if learning_context:
                analytics_context["learning_context"] = learning_context
                logger.info(f"✅ Learning context loaded: {learning_context.get('topic_name', 'unknown')}")
            else:
                logger.warning(f"⚠️ No learning context available for {state['user_id']} (no active topic)")
            
            return {
                "short_mem": short_mem, 
                "long_mem": long_mem,  # Keep as UserProfile object
                "analytics_context": analytics_context
            }
        except Exception:
            logger.exception(f"Load memory failed for {state['user_id']}")
            return {"error": "memory_load_failed"}

    async def _strategy_node(self, state: AgentState) -> Dict[str, Any]:
        """Quyết định chiến lược học tập với analytics context"""
        try:
            # Truyền analytics context vào strategy selector
            analytics = state.get("analytics_context", {})
            
            strategy = await self.strategy_selector.decide(
                user_id=state["user_id"],
                user_input=state["user_input"],
                long_mem=state["long_mem"],
                analytics_context=analytics
            )
            return {"strategy": strategy}
        except Exception:
            logger.exception(f"Strategy failed for {state['user_id']}")
            return {"error": "strategy_failed"}

    async def _planner_node(self, state: AgentState) -> Dict[str, Any]:
        """Tạo kế hoạch học tập với analytics guidance"""
        try:
            analytics = state.get("analytics_context", {})
            
            plan_obj = await self.planner.create_plan(
                user_input=state["user_input"],
                user_id=state["user_id"],
                strategy=state["strategy"],
                long_mem=state["long_mem"],
                analytics_context=analytics
            )
            # Chuyển sang dict để pipeline dễ xử lý
            return {"plan": plan_obj.model_dump()}
        except Exception:
            logger.exception(f"Planner failed for {state['user_id']}")
            return {"error": "planner_failed"}

    async def _execute_node(self, state: AgentState) -> Dict[str, Any]:
        """Thực thi pipeline"""
        try:
            # Phase 0: Extract short_mem as string for prompt
            # Handle both str (from DB) and ShortTermMemory object
            short_mem_str = None
            sm = state.get("short_mem")
            if sm:
                if isinstance(sm, str):
                    short_mem_str = sm
                elif hasattr(sm, "get_context_for_prompt"):
                    short_mem_str = sm.get_context_for_prompt()
                else:
                    logger.warning(f"short_mem has unexpected type: {type(sm)}")
            
            result = await self.pipeline.run(
                user_input=state["user_input"],
                user_id=state["user_id"],
                strategy=state["strategy"],
                plan=state["plan"],
                analytics_context=state.get("analytics_context", {}),
                quiz_context=state.get("quiz_context"),  # Phase 0: Pass quiz_context
                short_mem=short_mem_str  # Phase 0: Pass short_mem as string
            )
            return {
                "response": result.get("response"),
                "tools_used": result.get("tools_used", [])
            }
        except Exception:
            logger.exception(f"Pipeline execution failed for {state['user_id']}")
            return {"error": "execution_failed"}

    async def _reflect_node(self, state: AgentState) -> Dict[str, Any]:
        """Reflect on conversation and update weak/strong skills"""
        try:
            # Load current_topic_id from profile
            current_topic_id = await self._get_active_topic_id(state["db"], state["user_id"])
            
            reflection_result = await self.reflector.reflect_and_update(
                user_id=state["user_id"],
                user_input=state["user_input"],
                ai_response=state.get("response", ""),
                current_topic_id=current_topic_id,
                db=state["db"]
            )
            
            return {"reflection": reflection_result}
        except Exception:
            logger.exception(f"Reflection failed for {state['user_id']}")
            return {"error": "reflection_failed", "reflection": {}}
    
    async def _orchestrate_node(self, state: AgentState) -> Dict[str, Any]:
        """Phase 3: Orchestrate - suggest next actions based on state"""
        try:
            suggested_actions = self.orchestrator.suggest_next_action(
                learning_context=state.get("analytics_context", {}).get("learning_context"),
                analytics_context=state.get("analytics_context", {}),
                reflection=state.get("reflection", {}),
                strategy_mode=state.get("strategy", {}).get("mode"),
                quiz_context=state.get("quiz_context")
            )
            
            # Convert to dict for serialization
            actions_dict = [action.model_dump() for action in suggested_actions]
            
            logger.info(f"Orchestrator suggested {len(actions_dict)} actions for {state['user_id']}")
            
            return {"suggested_actions": actions_dict}
        except Exception:
            logger.exception(f"Orchestration failed for {state['user_id']}")
            return {"suggested_actions": []}

    async def _update_memory_node(self, state: AgentState) -> Dict[str, Any]:
        """Cập nhật memory sau khi có kết quả + Tự động lưu conversation + B2: Integrate reflection + NEW: Record chat activities"""
        try:
            # B2: Extract reflection insights for memory update
            reflection_result = state.get("reflection", {})
            analysis = None
            if reflection_result and reflection_result.get("updated"):
                # Build analysis dict from reflection for long-term memory
                analysis = {
                    "weak_skills": reflection_result.get("weak_skills", []),
                    "strong_skills": reflection_result.get("strong_skills", []),
                    "topics_discussed": reflection_result.get("topics_discussed", []),
                    "engagement": reflection_result.get("engagement", "medium"),
                }
                logger.info(f"🧠 B2: Passing reflection analysis to memory: {analysis}")
            
            # Update memory (short-term RAM + long-term profile)
            await self.memory.update(
                user_id=state["user_id"],
                user_input=state["user_input"],
                assistant_response=state.get("response", ""),
                intent=state["strategy"].get("mode", "general") if state.get("strategy") else "general",
                analysis=analysis,  # B2: Pass reflection results to memory
                db=state["db"]
            )
            
            # A4: AUTO-SAVE CONVERSATION to PostgreSQL
            await self._save_conversation_to_db(
                user_id=state["user_id"],
                user_input=state["user_input"],
                assistant_response=state.get("response", ""),
                session_id=state.get("session_id"),
                topic_id=state.get("current_topic_id"),
                learning_mode=state.get("learning_mode", "normal"),
                db=state["db"]
            )
            
            # NEW: Record chat learning activity
            from app.services.chat_learning_service import ChatLearningService
            chat_activity = reflection_result.get("chat_activity") if reflection_result else None
            if chat_activity:
                # Extract lesson_order from analytics_context if available
                lesson_order = None
                analytics_ctx = state.get("analytics_context", {})
                learning_ctx = analytics_ctx.get("learning_context", {})
                if learning_ctx and "current_lesson_order" in learning_ctx:
                    lesson_order = learning_ctx["current_lesson_order"]
                
                await ChatLearningService.record_activity(
                    db=state["db"],
                    user_id=UUID(state["user_id"]),
                    session_id=state.get("session_id", ""),
                    activity=chat_activity,
                    curriculum_topic_id=state.get("current_topic_id"),
                    lesson_order=lesson_order,
                )
            
            return {}
        except Exception:
            logger.exception(f"Memory update failed for {state['user_id']}")
            return {"error": "memory_update_failed"}

    # ========== Public API ==========
    async def _load_short_term_from_db(
        self,
        db: AsyncSession,
        user_id: str,
        session_id: Optional[str],
        limit: int = 15  # Increase from 10 to 15 for better context
    ) -> Optional[str]:
        """A5: Load short-term memory (last N messages) from PostgreSQL"""
        if not session_id:
            return None
        
        try:
            from sqlalchemy import select, desc
            from app.models.conversation import Conversation
            from uuid import UUID
            
            # Get last N messages from this session
            result = await db.execute(
                select(Conversation)
                .where(
                    Conversation.user_id == UUID(user_id),
                    Conversation.session_id == session_id
                )
                .order_by(desc(Conversation.created_at))
                .limit(limit)
            )
            messages = result.scalars().all()
            
            if not messages:
                return None
            
            # Build conversation history (reverse to chronological order)
            messages = list(reversed(messages))
            conversation_text = []
            
            for msg in messages:
                role = "User" if msg.role == "user" else "AI Tutor"
                # Don't truncate messages - keep full context for better memory
                conversation_text.append(f"{role}: {msg.message}")
            
            # Keep all messages for full context (was limited to 10)
            short_term = "\n".join(conversation_text)
            logger.info(f"✅ Loaded {len(messages)} messages from DB for session {session_id[:8]}... (total {len(short_term)} chars)")
            return short_term
            
        except Exception as e:
            logger.warning(f"Failed to load short-term from DB: {e}")
            return None

    async def _save_conversation_to_db(
        self,
        user_id: str,
        user_input: str,
        assistant_response: str,
        session_id: Optional[str],
        topic_id: Optional[Any],  # B1: Accept UUID or str
        learning_mode: str,
        db: AsyncSession
    ):
        """A4: Save conversation (user + assistant) to PostgreSQL automatically"""
        try:
            from app.services.conversation_service import ConversationService
            from uuid import UUID
            
            # Create session_id if not provided
            if not session_id:
                import uuid
                session_id = str(uuid.uuid4())
            
            # B1: Convert topic_id to string if UUID
            topic_id_str = str(topic_id) if topic_id else None
            
            conv_service = ConversationService(db)
            
            # Save user message
            await conv_service.save_message(
                user_id=UUID(user_id),
                session_id=session_id,
                role="user",
                message=user_input,
                topic_id=topic_id_str,
                learning_mode=learning_mode
            )
            
            # Save assistant message
            await conv_service.save_message(
                user_id=UUID(user_id),
                session_id=session_id,
                role="assistant",
                message=assistant_response,
                topic_id=topic_id_str,
                learning_mode=learning_mode
            )
            
            logger.info(f"✅ Saved conversation for {user_id} to DB (session: {session_id[:8]}...)")
            
        except Exception as e:
            logger.warning(f"Failed to save conversation to DB: {e}")
            # Don't fail the entire process if conversation saving fails

    async def _get_active_topic_id(self, db: AsyncSession, user_id: str) -> Optional[Any]:
        """Get active_topic_id from user profile"""
        try:
            from sqlalchemy import select
            from app.models.user_profile import UserProfile
            from uuid import UUID
            
            result = await db.execute(select(UserProfile).where(UserProfile.user_id == UUID(user_id)))
            profile = result.scalar_one_or_none()
            
            if profile and profile.active_topic_id:
                return profile.active_topic_id
            return None
        except Exception as e:
            logger.warning(f"Failed to get active_topic_id for {user_id}: {e}")
            return None

    async def _build_learning_context_dict(self, db: AsyncSession, user_id: str) -> Optional[Dict[str, Any]]:
        """Build learning context dict from active topic/lesson in profile"""
        try:
            from sqlalchemy import select, func
            from app.models.user_profile import UserProfile
            from app.models.topic import Topic
            from app.models.lesson import Lesson
            from app.models.user_topic_progress import UserTopicProgress
            from uuid import UUID
            
            # Get user profile
            result = await db.execute(select(UserProfile).where(UserProfile.user_id == UUID(user_id)))
            profile = result.scalar_one_or_none()
            
            if not profile or not profile.active_topic_id:
                return None  # No active topic
            
            # Get active topic
            topic_result = await db.execute(select(Topic).where(Topic.id == profile.active_topic_id))
            topic = topic_result.scalar_one_or_none()
            
            if not topic:
                return None
            
            context = {
                "topic_id": str(profile.active_topic_id),
                "topic_name": topic.name,
                "topic_name_vi": topic.name_vi,
                "level": topic.level,
                "grammar_focus": topic.grammar_focus or [],
            }
            
            # Get topic progress (lesson X/total, quiz_score, status)
            progress_result = await db.execute(
                select(UserTopicProgress).where(
                    UserTopicProgress.user_id == UUID(user_id),
                    UserTopicProgress.topic_id == profile.active_topic_id
                )
            )
            progress = progress_result.scalar_one_or_none()
            
            # Count total lessons in topic
            total_lessons_result = await db.execute(
                select(func.count(Lesson.id)).where(Lesson.topic_id == profile.active_topic_id)
            )
            total_lessons = total_lessons_result.scalar()
            
            if progress:
                context["lesson_completed"] = progress.lesson_completed
                context["total_lessons"] = total_lessons
                context["quiz_score"] = progress.quiz_score
                context["quiz_attempts"] = progress.quiz_attempts
                context["status"] = progress.status
                context["progress_percent"] = int((progress.lesson_completed / max(total_lessons, 1)) * 100)
            
            # Add current lesson info if available
            if profile.active_lesson_order:
                lesson_result = await db.execute(
                    select(Lesson).where(
                        Lesson.topic_id == profile.active_topic_id,
                        Lesson.order == profile.active_lesson_order
                    )
                )
                lesson = lesson_result.scalar_one_or_none()
                if lesson:
                    context["current_lesson_order"] = profile.active_lesson_order
                    context["lesson_title"] = lesson.title
                    context["lesson_type"] = lesson.lesson_type
                    
                    # Phase 1: Add lesson content for Agent to teach from
                    if lesson.content:
                        content = lesson.content
                        # Phase 1: Map fields correctly from topics_data.py structure
                        # vocabulary lessons use "words", grammar uses "explanation"
                        
                        # Prepare lesson content dict
                        lesson_content_dict = {}
                        
                        # Common fields
                        if "key_points" in content:
                            lesson_content_dict["key_points"] = content["key_points"][:5]
                        
                        if "examples" in content:
                            # Examples can be dict with en/vi or just strings
                            examples = content["examples"][:3]
                            formatted_examples = []
                            for ex in examples:
                                if isinstance(ex, dict):
                                    formatted_examples.append(f"{ex.get('en', '')} ({ex.get('vi', '')})")
                                else:
                                    formatted_examples.append(str(ex))
                            lesson_content_dict["examples"] = formatted_examples
                        
                        # Map vocabulary: "words" → "vocabulary"
                        if "words" in content:
                            vocab_list = []
                            for word_item in content["words"][:10]:
                                if isinstance(word_item, dict):
                                    vocab_list.append(f"{word_item.get('word', '')} - {word_item.get('meaning', '')}")
                                else:
                                    vocab_list.append(str(word_item))
                            lesson_content_dict["vocabulary"] = vocab_list
                        
                        # Map grammar: "explanation" → "grammar_rules"
                        if "explanation" in content:
                            explanation = content["explanation"]
                            if isinstance(explanation, list):
                                lesson_content_dict["grammar_rules"] = explanation[:3]
                            elif isinstance(explanation, str):
                                lesson_content_dict["grammar_rules"] = [explanation]
                        
                        # Additional explanation_vi
                        if "explanation_vi" in content:
                            if "grammar_rules" not in lesson_content_dict:
                                lesson_content_dict["grammar_rules"] = []
                            lesson_content_dict["grammar_rules"].append(f"[VI] {content['explanation_vi']}")
                        
                        # Notes/tips
                        if "notes" in content:
                            lesson_content_dict["tips"] = [content["notes"]]
                        elif "tips" in content:
                            lesson_content_dict["tips"] = content.get("tips", [])[:3]
                        
                        context["lesson_content"] = lesson_content_dict
            
            logger.info(f"Built learning context for {user_id}: {topic.name} ({context.get('lesson_completed', 0)}/{total_lessons} lessons)")
            return context
            
        except Exception as e:
            logger.warning(f"Failed to build learning context for {user_id}: {e}")
            return None

    async def _build_analytics_context_async(self, db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Build analytics context from quiz results and weak skills"""
        try:
            # Get skill breakdown
            skill_breakdown = await QuizAnalyticsService.get_skill_breakdown(db, user_id)
            
            # Find weak skills (< 60% accuracy)
            weak_skills = {
                skill: data["accuracy"]
                for skill, data in skill_breakdown.items()
                if data["accuracy"] < 0.6
            }
            
            # Get due reviews
            due_reviews = await QuizAnalyticsService.get_due_reviews(db, user_id)
            
            # Phase 4: Check level-up eligibility
            level_eligible = False
            current_level = "A1"
            try:
                from app.services.level_progress_service import LevelProgressService
                from app.models.user_profile import UserProfile
                
                # Get user's current level from UserProfile
                profile_result = await db.execute(select(UserProfile).where(UserProfile.user_id == UUID(user_id)))
                profile = profile_result.scalar_one_or_none()
                if profile:
                    current_level = profile.current_level or "A1"
                    
                    # Check eligibility
                    eligibility_service = LevelProgressService()
                    eligibility_result = await eligibility_service.check_eligibility(UUID(user_id), db)
                    level_eligible = eligibility_result.get("eligible", False)
                    
                    logger.info(f"Level-up eligibility for {user_id}: {level_eligible}")
            except Exception as e:
                logger.warning(f"Could not check level eligibility in analytics: {e}")
            
            # Build context summary
            context = {
                "weak_skills": weak_skills,
                "skill_breakdown": skill_breakdown,
                "due_reviews_count": len(due_reviews),
                "needs_review": len(due_reviews) > 0,
                "total_exercises": sum(s["total"] for s in skill_breakdown.values()),
                "overall_accuracy": sum(s["correct"] for s in skill_breakdown.values()) / max(sum(s["total"] for s in skill_breakdown.values()), 1),
                "level_eligible": level_eligible,  # Phase 4
                "current_level": current_level  # Phase 4
            }
            
            logger.info(f"Analytics context built for {user_id}: {len(weak_skills)} weak skills, {len(due_reviews)} due reviews, eligible={level_eligible}")

            return context
            
        except Exception as e:
            logger.warning(f"Failed to build analytics context for {user_id}: {e}")
            return {}

    async def process(
        self,
        user_input: str,
        user_id: str,
        db: AsyncSession,
        session_id: Optional[str] = None,
        quiz_wrong_answers: Optional[list] = None,
        quiz_topic_id: Optional[str] = None,
        target_lang: Optional[str] = None,
        explain_in: Optional[str] = None
    ) -> Dict[str, Any]:
        """Entry point chính cho AI Tutor"""
        if not user_input or not user_input.strip():
            return {
                "success": False,
                "response": "Vui lòng nhập nội dung câu hỏi.",
                "error": "empty_input"
            }
        
        # Generate session_id if not provided (A4: for conversation tracking)
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
        
        # Get current topic_id for conversation context (B1: Keep as UUID)
        current_topic_id = await self._get_active_topic_id(db, user_id)
        
        # A3: Determine learning mode based on quiz context
        learning_mode = "normal"
        if quiz_wrong_answers or quiz_topic_id:
            learning_mode = "quiz_review"
            logger.info(f"🎯 Quiz review mode for {user_id}: {len(quiz_wrong_answers or [])} wrong answers")

        # State ban đầu (A4: include session tracking + A3: quiz context)
        initial_state: AgentState = {
            "user_input": user_input,
            "user_id": user_id,
            "db": db,
            "session_id": session_id,
            "current_topic_id": current_topic_id,
            "learning_mode": learning_mode,
            "quiz_context": {
                "wrong_answers": quiz_wrong_answers or [],
                "topic_id": quiz_topic_id
            } if quiz_wrong_answers or quiz_topic_id else None,
            "long_mem": None,
            "short_mem": None,
            "analytics_context": None,
            "strategy": None,
            "plan": None,
            "response": None,
            "tools_used": [],
            "error": None,
        }

        try:
            final_state = await self.graph.ainvoke(initial_state)

            if final_state.get("error"):
                logger.error(f"Graph error for user {user_id}: {final_state['error']}")
                return {
                    "success": False,
                    "response": "Hệ thống gặp sự cố. Vui lòng thử lại sau.",
                    "error": "internal_error"
                }

            # B3: Build metadata with learning context
            from app.models.user_profile import UserProfile
            from app.models.topic import Topic
            from sqlalchemy import select
            
            metadata = {
                "strategy_mode": final_state.get("strategy", {}).get("mode"),
                "tools_used": final_state.get("tools_used", []),
                "session_id": session_id,
                "learning_mode": learning_mode,
                "suggested_actions": final_state.get("suggested_actions", [])  # Phase 3
            }
            
            # Add learning context to metadata
            try:
                profile_result = await db.execute(
                    select(UserProfile).where(UserProfile.user_id == UUID(user_id))
                )
                profile = profile_result.scalar_one_or_none()
                
                if profile:
                    metadata["current_level"] = profile.current_level
                    metadata["active_topic_id"] = str(profile.active_topic_id) if profile.active_topic_id else None
                    
                    if profile.active_topic_id:
                        topic_result = await db.execute(
                            select(Topic).where(Topic.id == profile.active_topic_id)
                        )
                        topic = topic_result.scalar_one_or_none()
                        if topic:
                            metadata["active_topic_name"] = topic.name_vi or topic.name
                            metadata["learning_context"] = final_state.get("analytics_context", {})
            except Exception as e:
                logger.warning(f"B3: Failed to add metadata: {e}")
            
            return {
                "success": True,
                "response": final_state.get("response", ""),
                "metadata": metadata
            }
        except Exception:
            logger.exception(f"LearningService.process failed for {user_id}")
            return {
                "success": False,
                "response": "Xin lỗi, mình đang gặp sự cố kỹ thuật. Bạn thử hỏi lại nhé!",
                "error": "internal_server_error"
            }