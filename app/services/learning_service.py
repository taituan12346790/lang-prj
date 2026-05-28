from typing import Dict, Any
from loguru import logger
from langgraph.graph import StateGraph, END
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.graph_state import AgentState
from app.core.strategy import StrategySelector
from app.core.planner import ReActPlanner
from app.core.pipeline import Pipeline
from app.memory.memory_service import MemoryService


class LearningService:
    """Learning Service sử dụng LangGraph - production ready"""

    def __init__(self):
        self.memory = MemoryService()
        self.strategy_selector = StrategySelector()
        self.planner = ReActPlanner()
        self.pipeline = Pipeline()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(AgentState)

        # Nodes
        graph.add_node("load_memory", self._load_memory_node)
        graph.add_node("strategy", self._strategy_node)
        graph.add_node("planner", self._planner_node)
        graph.add_node("execute", self._execute_node)
        graph.add_node("update_memory", self._update_memory_node)

        # Entry point
        graph.set_entry_point("load_memory")

        # Conditional edges
        graph.add_conditional_edges(
            "load_memory",
            self._after_load_memory,
            {"continue": "strategy", "error": END}
        )
        graph.add_conditional_edges(
            "strategy",
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
            {"continue": "update_memory", "error": END}
        )
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
        """Load long-term và short-term memory"""
        try:
            short_mem, long_mem = await self.memory.load(state["user_id"], state["db"])
            return {"short_mem": short_mem, "long_mem": long_mem}
        except Exception:
            logger.exception(f"Load memory failed for {state['user_id']}")
            return {"error": "memory_load_failed"}

    async def _strategy_node(self, state: AgentState) -> Dict[str, Any]:
        """Quyết định chiến lược học tập"""
        try:
            strategy = await self.strategy_selector.decide(
                user_id=state["user_id"],
                user_input=state["user_input"],
                long_mem=state["long_mem"]
            )
            return {"strategy": strategy}
        except Exception:
            logger.exception(f"Strategy failed for {state['user_id']}")
            return {"error": "strategy_failed"}

    async def _planner_node(self, state: AgentState) -> Dict[str, Any]:
        """Tạo kế hoạch học tập"""
        try:
            plan_obj = await self.planner.create_plan(
                user_input=state["user_input"],
                user_id=state["user_id"],
                strategy=state["strategy"],
                long_mem=state["long_mem"]
            )
            # Chuyển sang dict để pipeline dễ xử lý
            return {"plan": plan_obj.model_dump()}
        except Exception:
            logger.exception(f"Planner failed for {state['user_id']}")
            return {"error": "planner_failed"}

    async def _execute_node(self, state: AgentState) -> Dict[str, Any]:
        """Thực thi pipeline"""
        try:
            result = await self.pipeline.run(
                user_input=state["user_input"],
                user_id=state["user_id"],
                strategy=state["strategy"],
                plan=state["plan"]   # đã là dict
            )
            return {
                "response": result.get("response"),
                "tools_used": result.get("tools_used", [])
            }
        except Exception:
            logger.exception(f"Pipeline execution failed for {state['user_id']}")
            return {"error": "execution_failed"}

    async def _update_memory_node(self, state: AgentState) -> Dict[str, Any]:
        """Cập nhật memory sau khi có kết quả"""
        try:
            await self.memory.update(
                user_id=state["user_id"],
                user_input=state["user_input"],
                assistant_response=state.get("response", ""),
                intent=state["strategy"].get("mode", "general") if state.get("strategy") else "general",
                analysis=None,
                db=state["db"]
            )
            return {}
        except Exception:
            logger.exception(f"Memory update failed for {state['user_id']}")
            return {"error": "memory_update_failed"}

    # ========== Public API ==========
    async def process(
        self,
        user_input: str,
        user_id: str,
        db: AsyncSession,
        target_lang: Optional[str] = None,   # thêm
        explain_in: Optional[str] = None     # thêm
    ) -> Dict[str, Any]:
        """Entry point chính cho AI Tutor"""
        if not user_input or not user_input.strip():
            return {
                "success": False,
                "response": "Vui lòng nhập nội dung câu hỏi.",
                "error": "empty_input"
            }

        # State ban đầu
        initial_state: AgentState = {
            "user_input": user_input,
            "user_id": user_id,
            "db": db,
            "long_mem": None,
            "short_mem": None,
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

            return {
                "success": True,
                "response": final_state.get("response", ""),
                "metadata": {
                    "strategy_mode": final_state.get("strategy", {}).get("mode"),
                    "tools_used": final_state.get("tools_used", [])
                }
            }
        except Exception:
            logger.exception(f"LearningService.process failed for {user_id}")
            return {
                "success": False,
                "response": "Xin lỗi, mình đang gặp sự cố kỹ thuật. Bạn thử hỏi lại nhé!",
                "error": "internal_server_error"
            }