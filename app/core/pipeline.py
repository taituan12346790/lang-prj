# app/core/pipeline.py - LangGraph-based Pipeline (No RAG, Node-based Orchestration)
import asyncio
import time
from typing import Dict, Any
from loguru import logger
from langgraph.graph import StateGraph, END

from app.core.graph_state import AgentState
from app.core.validator import ResponseValidator
from app.core.reflector_enhanced import ReflectorEnhanced  # CÁCH 3: Import reflector
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
        self.reflector = ReflectorEnhanced()  # CÁCH 3: Initialize reflector
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""
        graph = StateGraph(AgentState)

        # Add nodes
        graph.add_node("validate_input", self._validate_input_node)
        graph.add_node("analyze_memory", self._analyze_memory_node)  # CÁCH 2: Memory-driven
        graph.add_node("execute_tools", self._execute_tools_node)
        graph.add_node("generate_response", self._generate_response_node)
        graph.add_node("reflect", self._reflect_node)  # CÁCH 3: Self-reflection
        graph.add_node("validate_output", self._validate_output_node)
        #graph.add_node("repair", self._repair_node)
        graph.add_node("finalize", self._finalize_node)

        # Entry point
        graph.set_entry_point("validate_input")

        # Conditional routing
        graph.add_conditional_edges(
            "validate_input",
            self._after_validate_input,
            {"blocked": "finalize", "continue": "analyze_memory"}  # → Memory first
        )
        
        graph.add_edge("analyze_memory", "execute_tools")  # Memory → Tools

        graph.add_edge("execute_tools", "generate_response")
        graph.add_edge("generate_response", "reflect")  # CÁCH 3: Reflect before validate
        graph.add_edge("reflect", "validate_output")
        # CÁCH 1: Self-Correction - Repair invalid responses
        graph.add_node("repair", self._repair_node)


        # Route to repair if validation fails
        graph.add_conditional_edges(
            "validate_output",
            self._after_validate_output,
            {"valid": "finalize", "invalid": "repair"}
        )

        # Retry once after repair
        graph.add_conditional_edges(
            "repair",
            self._after_repair,
            {"valid": "finalize", "invalid": "finalize"}
        )

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
                "response": (
                    "Xin lỗi, mình không hỗ trợ trả lời về các chủ đề tình dục, "
                    "tranh chấp lãnh thổ, xung đột chính trị, tôn giáo nhạy cảm "
                    "hoặc nội dung cực đoan.\n\n"
                    "Bạn có câu hỏi nào về ngữ pháp, từ vựng hoặc kỹ năng ngôn ngữ không?"
                ),
                "error": "input_blocked"
            }

        # Return empty dict when validation passes (no state update needed)
        return {}
    
    async def _analyze_memory_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 1.5: Analyze memory to detect weak areas and preferences (CÁCH 2)"""
        analytics_context = state.get("analytics_context", {})
        short_mem = state.get("short_mem", "")
        
        memory_insights = {
            "repeated_errors": [],
            "weak_topics": [],
            "user_style": "detailed"
        }
        
        # Detect weak skills from analytics
        if analytics_context and "weak_skills" in analytics_context:
            weak = analytics_context.get("weak_skills", [])
            if weak:
                memory_insights["repeated_errors"] = [w.get("skill", "") for w in weak[:3]]
                logger.info(f"💡 Detected weak skills: {memory_insights['repeated_errors']}")
        
        # Detect user preference from conversation history
        if short_mem and isinstance(short_mem, str):
            short_lower = short_mem.lower()
            if any(word in short_lower for word in ["ngắn gọn", "tóm tắt", "brief", "short"]):
                memory_insights["user_style"] = "concise"
                logger.info("💡 User prefers concise answers")
            elif any(word in short_lower for word in ["chi tiết", "kỹ hơn", "không hiểu", "explain more"]):
                memory_insights["user_style"] = "very_detailed"
                logger.info("💡 User needs very detailed explanations")
        
        # Memory insights are used internally, not added to state
        # Just log and continue
        return {}

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
        tool_results = state.get("tool_results", {})
        memory_insights = state.get("memory_insights", {})  # CÁCH 2: Get memory insights
        
        # Phase 0: Extract short_mem from state
        short_mem_str = None
        sm = state.get("short_mem")
        if sm:
            if isinstance(sm, str):
                short_mem_str = sm
            elif hasattr(sm, "get_context_for_prompt"):
                short_mem_str = sm.get_context_for_prompt()

        # Build prompt WITH memory insights (CÁCH 2)
        system_prompt = build_prompt(
            user_input=user_input,
            strategy=strategy,
            plan=plan,
            rag_context="",
            analytics_context=analytics_context,
            quiz_context=quiz_context,
            short_mem=short_mem_str,
            tool_results=tool_results,
            memory_insights=memory_insights  # CÁCH 2: Pass memory insights!
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
    
    async def _reflect_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 3.5: Self-Reflection - Agent reviews its own response (CÁCH 3)"""
        response = state.get("response", "")
        user_input = state.get("user_input", "")
        strategy = state.get("strategy", {})
        
        # Quick reflection prompt
        reflection_prompt = f"""Review this AI tutor response for quality:

User asked: {user_input}
AI response: {response}

Evaluate:
1. Does it answer the user's question completely?
2. Is the language appropriate (Vietnamese for teaching)?
3. Are examples sufficient (if user asked for examples)?
4. Is explanation clear and well-structured?

Rate quality: 1-10
If score < 6, suggest improvements.

Response format:
SCORE: [number]
ISSUES: [list issues if any]
IMPROVEMENTS: [list 1-3 specific improvements]
"""
        
        try:
            reflection_text = await asyncio.wait_for(
                self.llm.generate_async(
                    user_input=reflection_prompt,
                    system_prompt="You are a quality reviewer for AI tutor responses. Be critical but constructive.",
                    temperature=0.3,
                    max_tokens=300
                ),
                timeout=10
            )
            
            # Parse score
            score = 7.0  # default
            issues = []
            improvements = []
            
            for line in reflection_text.split('\n'):
                if 'SCORE:' in line.upper():
                    try:
                        score = float(line.split(':')[1].strip())
                    except:
                        pass
                elif 'ISSUES:' in line.upper():
                    issues_text = line.split(':', 1)[1].strip()
                    if issues_text and issues_text != 'None':
                        issues.append(issues_text)
                elif 'IMPROVEMENTS:' in line.upper():
                    improvements_text = line.split(':', 1)[1].strip()
                    if improvements_text and improvements_text != 'None':
                        improvements.append(improvements_text)
            
            logger.info(f"🤔 Reflection score: {score}/10")
            
            # If quality is low, try to improve
            if score < 6.0 and improvements:
                logger.warning(f"⚠️ Response quality low ({score}/10), improving...")
                
                improve_prompt = f"""Improve this response based on feedback:

Original response:
{response}

Issues: {', '.join(issues) if issues else 'Quality too low'}
Improvements needed:
{chr(10).join(f'- {imp}' for imp in improvements[:3])}

Generate improved version (keep same language):"""
                
                improved_response = await asyncio.wait_for(
                    self.llm.generate_async(
                        user_input=improve_prompt,
                        system_prompt="You are improving an AI tutor response. Keep it clear and helpful.",
                        temperature=0.4,
                        max_tokens=1500
                    ),
                    timeout=15
                )
                
                logger.success(f"✅ Response improved (score was {score}/10)")
                return {
                    "response": improved_response,
                    "reflection_score": score,
                    "was_improved": True
                }
            
            return {"reflection_score": score, "was_improved": False}
            
        except Exception as e:
            logger.warning(f"Reflection failed: {e}, continuing without improvement")
            return {"reflection_score": 7.0, "was_improved": False}

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
            return {}  # No state update needed when valid
        else:
            logger.warning(f"❌ Output validation failed: {reason}")
            # Set error to trigger repair flow
            return {"error": f"output_validation_failed: {reason}"}

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
        # No state updates needed - just pass through
        # Success/failure is determined by presence of error in state
        return {}

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

