# app/memory/short_term_memory.py
from collections import deque
from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel


class Interaction(BaseModel):
    user_input: str
    assistant_response: str
    intent: str
    timestamp: str


class ShortTermMemory:
    def __init__(self, max_history: int = 20, max_session: int = 15):
        self.history: deque = deque(maxlen=max_history)
        self.current_session: deque = deque(maxlen=max_session)

    def add_interaction(self, user_input: str, assistant_response: str, intent: str = "general"):
        interaction = Interaction(
            user_input=user_input,
            assistant_response=assistant_response,
            intent=intent,
            timestamp=datetime.now().isoformat()
        )
        self.history.append(interaction)
        self.current_session.append(interaction)

    def get_recent(self, n: int = 10) -> List[Dict]:
        return [item.dict() for item in list(self.history)[-n:]]

    def get_session_summary(self) -> str:
        if not self.current_session:
            return ""
        lines = []
        for item in list(self.current_session)[-8:]:
            lines.append(f"User: {item.user_input}")
            lines.append(f"AI: {item.assistant_response[:180]}...")
            lines.append("---")
        return "\n".join(lines)

    def get_context_for_prompt(self) -> str:
        return self.get_session_summary()

    def clear_session(self):
        self.current_session.clear()