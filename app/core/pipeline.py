# app/core/pipeline.py - LangGraph-based Pipeline (No RAG, Node-based Orchestration)
import asyncio
import time
from typing import Dict, Any
from loguru import logger
from langgraph.graph import StateGraph, END

from app.core.graph_state import AgentState
from app.core.validator import ResponseValidator
from app.llm.prompts import build_prompt, build_repair_prompt
from app.llm.llm_client import LLMClient
from app.tools.tool_registry import ToolRegistry


class Pipeline:
    """
    LangGraph-based Pipeline for AI Language Tutor Agent
    
    Node Flow:
    1. validate_input      → Guardrail check
    2. execute_tools       → Run tools in parallel
    3. generate_response   → LLM generation
    4. validate_output     → Response validation
    5. repair              → Fix response if invalid
    6. finalize            → Return result
    """

    def __init__(self):
        self.llm = LLMClient()
        # Phase 2: Use singleton tool_registry instead of creating new instance
        from app.tools.tool_registry import tool_registry
        self.tool_registry = tool_registry
        self.validator = ResponseValidator()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""
        graph = StateGraph(AgentState)

        # Add nodes
        graph.add_node("validate_input", self._validate_input_node)
        graph.add_node("execute_tools", self._execute_tools_node)
        graph.add_node("generate_response", self._generate_response_node)
        graph.add_node("validate_output", self._validate_output_node)
        #graph.add_node("repair", self._repair_node)
        graph.add_node("finalize", self._finalize_node)

        # Entry point
        graph.set_entry_point("validate_input")

        # Conditional routing
        graph.add_conditional_edges(
            "validate_input",
            self._after_validate_input,
            {"blocked": "finalize", "continue": "execute_tools"}
        )

        graph.add_edge("execute_tools", "generate_response")
        graph.add_edge("generate_response", "validate_output")




        graph.add_edge("validate_output", "finalize")

        #graph.add_conditional_edges(
        #    "validate_output",
        #    self._after_validate_output,
        #    {"valid": "finalize", "invalid": "repair"}
        #)

        #graph.add_conditional_edges(
        #    "repair",
        #    self._after_repair,
        #    {"valid": "finalize", "invalid": "finalize"}
        #)

        graph.add_edge("finalize", END)

        return graph.compile()

    # ===== ROUTING DECISIONS =====

    @staticmethod
    def _after_validate_input(state: AgentState) -> str:
        """Route after input validation"""
        return "blocked" if state.get("input_blocked") else "continue"

    @staticmethod
    def _after_validate_output(state: AgentState) -> str:
        """Route after output validation"""
        return "valid" if state.get("output_valid") else "invalid"

    @staticmethod
    def _after_repair(state: AgentState) -> str:
        """Route after repair attempt"""
        return "valid" if state.get("output_valid") else "invalid"

    # ===== NODES =====

    async def _validate_input_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 1: Validate user input (guardrail)"""
        user_input = state.get("user_input", "")
        
        input_allowed, input_reason = self.validator.validate_input(user_input)

        if not input_allowed:
            logger.warning(f"INPUT BLOCKED | Reason: {input_reason} | Input: {user_input[:120]}...")
            return {
                "input_blocked": True,
                "input_block_reason": input_reason,
                "response": (
                    "Xin lỗi, mình không hỗ trợ trả lời về các chủ đề tình dục, "
                    "tranh chấp lãnh thổ, xung đột chính trị, tôn giáo nhạy cảm "
                    "hoặc nội dung cực đoan.\n\n"
                    "Bạn có câu hỏi nào về ngữ pháp, từ vựng hoặc kỹ năng ngôn ngữ không?"
                ),
                "success": False,
                "blocked_by": "input_guardrail"
            }

        return {"input_blocked": False}

    async def _execute_tools_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 2: Execute tools in parallel"""
        plan = state.get("plan", {})
        user_input = state.get("user_input", "")
        strategy = state.get("strategy", {})
        user_id = state.get("user_id", "")
        
        tool_results: Dict[str, Any] = {}
        tools_used = []

        # Build parallel tasks for each tool
        tool_tasks = []
        for tool_name in plan.get("tools_to_use", []):
            tool = self.tool_registry.get_tool(tool_name)
            if tool:
                tool_tasks.append(
                    self._execute_tool(tool_name, tool, user_input, strategy, user_id)
                )

        # Execute all tools in parallel
        if tool_tasks:
            results = await asyncio.gather(*tool_tasks, return_exceptions=True)
            for tool_name, result in results:
                if isinstance(result, Exception):
                    tool_results[tool_name] = {"success": False, "error": str(result)}
                else:
                    tool_results[tool_name] = result
                    if result.get("success"):
                        tools_used.append(tool_name)

        logger.info(f"Tools executed: {tools_used}")

        return {
            "tool_results": tool_results,
            "tools_used": tools_used
        }

    async def _generate_response_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 3: Generate LLM response (NO RAG)"""
        user_input = state.get("user_input", "")
        strategy = state.get("strategy", {})
        plan = state.get("plan", {})
        analytics_context = state.get("analytics_context", {})
        quiz_context = state.get("quiz_context")
        tool_results = state.get("tool_results", {})  # P3: Get tool results from state
        
        # Phase 0: Extract short_mem from state
        short_mem_str = None
        sm = state.get("short_mem")
        if sm:
            if isinstance(sm, str):
                short_mem_str = sm
            elif hasattr(sm, "get_context_for_prompt"):
                short_mem_str = sm.get_context_for_prompt()

        # Build prompt WITHOUT RAG context (as per user requirement)
        # P3: Pass tool_results to build_prompt
        system_prompt = build_prompt(
            user_input=user_input,
            strategy=strategy,
            plan=plan,
            rag_context="",
            analytics_context=analytics_context,
            quiz_context=quiz_context,  # A3: Include quiz review context
            short_mem=short_mem_str,  # Phase 0: Include recent conversation
            tool_results=tool_results  # P3: Include tool results
        )
        
        # DEBUG: Log if learning context is in prompt
        if "ACTIVE LEARNING CONTEXT" in system_prompt:
            logger.info("✅ Learning context IS included in prompt")
            if analytics_context and "learning_context" in analytics_context:
                lc = analytics_context["learning_context"]
                logger.info(f"   Topic: {lc.get('topic_name_vi', 'N/A')}, Lesson: {lc.get('lesson_title', 'N/A')}")
        else:
            logger.warning("❌ Learning context NOT in prompt")
            logger.warning(f"   Analytics context keys: {list(analytics_context.keys()) if analytics_context else 'None'}")
            if analytics_context:
                logger.warning(f"   Has learning_context key: {'learning_context' in analytics_context}")
        
        # P3: Log tool results
        if tool_results:
            logger.info(f"🔧 Tool results included in prompt: {list(tool_results.keys())}")
        
        # A3: Log quiz review mode
        if quiz_context:
            logger.info(f"🎯 Quiz review mode: {len(quiz_context.get('wrong_answers', []))} wrong answers")

        # Generate response
        final_response = await self._safe_llm_generate(
            user_input=user_input,
            system_prompt=system_prompt,
            temperature=strategy.get("params", {}).get("temperature", 0.5),
            max_tokens=1500
        )

        logger.info(f"Response generated | Length: {len(final_response)}")

        return {"response": final_response}

    async def _validate_output_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 4: Validate LLM output"""
        response = state.get("response", "")
        user_input = state.get("user_input", "")
        strategy = state.get("strategy", {})
        plan = state.get("plan", {})
        tool_results = state.get("tool_results", {})

        context = {
            "user_input": user_input,
            "intent": plan.get("intent", "chat"),
            "strategy": strategy,
            "teaching_lang": strategy.get("explain_in", "Tiếng Việt"),
            "tool_results": tool_results
        }

        is_valid, reason = self.validator.validate(response, context)

        if is_valid:
            logger.info("✅ Output validation passed")
        else:
            logger.warning(f"❌ Output validation failed: {reason}")

        return {
            "output_valid": is_valid,
            "validation_reason": reason
        }

    async def _repair_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 5: Repair invalid output"""
        original_response = state.get("response", "")
        validation_reason = state.get("validation_reason", "Unknown")
        user_input = state.get("user_input", "")
        strategy = state.get("strategy", {})

        logger.info(f"🔧 Attempting to repair response...")

        repair_prompt = build_repair_prompt(
            original_response=original_response,
            feedback=validation_reason,
            user_input=user_input,
            strategy=strategy
        )

        repaired_response = await self._safe_llm_generate(
            user_input=user_input,
            system_prompt=repair_prompt,
            temperature=0.3,
            max_tokens=1200
        )

        # Re-validate repaired response
        plan = state.get("plan", {})
        tool_results = state.get("tool_results", {})
        context = {
            "user_input": user_input,
            "intent": plan.get("intent", "chat"),
            "strategy": strategy,
            "teaching_lang": strategy.get("explain_in", "Tiếng Việt"),
            "tool_results": tool_results
        }

        is_valid, reason = self.validator.validate(repaired_response, context)

        if is_valid:
            logger.success("✅ Repaired response is valid")
            return {
                "response": repaired_response,
                "output_valid": True
            }
        else:
            logger.warning("❌ Repaired response still invalid, using fallback")
            return {
                "response": "Xin lỗi, mình không thể trả lời yêu cầu này theo đúng nguyên tắc. Bạn thử hỏi theo cách khác nhé!",
                "output_valid": False,
                "used_fallback": True
            }

    async def _finalize_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 6: Finalize and prepare response"""
        if state.get("input_blocked"):
            return {
                "success": False,
                "blocked_by": "input_guardrail"
            }

        return {
            "success": True,
            "tools_used": state.get("tools_used", []),
            "strategy_mode": state.get("strategy", {}).get("mode"),
            "validated": state.get("output_valid", False),
            "used_fallback": state.get("used_fallback", False)
        }

    # ===== HELPER METHODS =====

    async def run(
        self,
        user_input: str,
        user_id: str,
        strategy: Dict,
        plan: Dict,
        analytics_context: Dict = None,
        quiz_context: Dict = None,
        short_mem: str = None
    ) -> Dict:
        """Execute pipeline via LangGraph"""
        start_time = time.time()

        try:
            # Build initial state - INCLUDE all context!
            state = AgentState(
                user_input=user_input,
                user_id=user_id,
                db=None,
                long_mem=None,
                short_mem=short_mem,  # Phase 0: Add short_mem
                analytics_context=analytics_context or {},
                quiz_context=quiz_context,  # Phase 0: Add quiz_context
                strategy=strategy,
                plan=plan,
                response=None,
                tools_used=[],
                error=None
            )

            # Execute graph (runs synchronously but called within async context)
            final_state = await self._run_graph_async(state)

            execution_time = time.time() - start_time

            return {
                "response": final_state.get("response", ""),
                "tools_used": final_state.get("tools_used", []),
                "strategy_mode": strategy.get("mode"),
                "validated": final_state.get("output_valid", False),
                "execution_time": round(execution_time, 3),
                "success": final_state.get("success", False),
                "error": final_state.get("error")
            }

        except Exception as e:
            logger.exception("Pipeline execution failed")
            return {
                "response": "Xin lỗi, hệ thống đang gặp sự cố kỹ thuật. Bạn thử lại sau nhé!",
                "success": False,
                "error": str(e)
            }

    async def _run_graph_async(self, state: AgentState) -> Dict[str, Any]:
        """
        Run LangGraph in async context
        LangGraph compiled graphs are sync, so we run in thread pool
        """
        return await self.graph.ainvoke(state)

    async def _execute_tool(
        self,
        tool_name: str,
        tool,
        user_input: str,
        strategy: Dict,
        user_id: str
    ):
        """Execute single tool with timeout"""
        try:
            result = await asyncio.wait_for(
                tool.execute(user_input, strategy, user_id),
                timeout=12.0
            )
            return tool_name, {"success": True, "data": result}
        except asyncio.TimeoutError:
            logger.error(f"Tool {tool_name} timeout")
            return tool_name, {"success": False, "error": "timeout"}
        except Exception as e:
            logger.error(f"Tool {tool_name} error: {e}")
            return tool_name, {"success": False, "error": str(e)}

    async def _safe_llm_generate(
        self,
        user_input: str,
        system_prompt: str,
        temperature: float,
        max_tokens: int,
        retries: int = 2
    ):
        """Generate LLM response with retries"""
        for attempt in range(retries):
            try:
                return await asyncio.wait_for(
                    self.llm.generate_async(
                        user_input=user_input,
                        system_prompt=system_prompt,
                        temperature=temperature,
                        max_tokens=max_tokens
                    ),
                    timeout=60
                )
            except Exception as e:
                logger.warning(f"LLM attempt {attempt+1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(1.5)
                else:
                    raise

