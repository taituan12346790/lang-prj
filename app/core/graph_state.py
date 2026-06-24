from typing import TypedDict, Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession


class AgentState(TypedDict):
    user_input: str
    user_id: str
    db: AsyncSession

    # Memory (sẽ được load trong graph)
    long_mem: Optional[Any]
    short_mem: Optional[Any]
    
    # Analytics context (quiz results, weak skills)
    analytics_context: Optional[Dict[str, Any]]
    
    # Conversation tracking (A4: for auto-save)
    session_id: Optional[str]
    current_topic_id: Optional[str]
    learning_mode: Optional[str]
    
    # A3: Quiz review context
    quiz_context: Optional[Dict[str, Any]]

    # Kết quả từ các node
    strategy: Optional[Dict[str, Any]]
    plan: Optional[Dict[str, Any]]          # LearningPlan dạng dict cho pipeline
    tool_results: Optional[Dict[str, Any]]  # Results from tool execution
    response: Optional[str]
    tools_used: List[str]
    
    # Phase 3: Orchestrator results
    reflection: Optional[Dict[str, Any]]
    suggested_actions: Optional[List[Dict[str, Any]]]

    # Lỗi
    error: Optional[str]