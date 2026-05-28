from typing import TypedDict, Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession


class AgentState(TypedDict):
    user_input: str
    user_id: str
    db: AsyncSession

    # Memory (sẽ được load trong graph)
    long_mem: Optional[Any]
    short_mem: Optional[Any]

    # Kết quả từ các node
    strategy: Optional[Dict[str, Any]]
    plan: Optional[Dict[str, Any]]          # LearningPlan dạng dict cho pipeline
    response: Optional[str]
    tools_used: List[str]

    # Lỗi
    error: Optional[str]