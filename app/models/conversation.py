# app/models/conversation.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from enum import Enum
from sqlalchemy import Enum as SQLEnum

from app.core.database import Base


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    
    session_id = Column(String, index=True, nullable=False)
    
    role = Column(
        SQLEnum(MessageRole, name="message_role"), 
        nullable=False
    )
    
    message = Column(Text, nullable=False)
    
    tokens = Column(Integer, default=0)                    # Tổng tokens (prompt + completion)
    model_used = Column(String, nullable=False)            # Bắt buộc phải ghi model

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    # Relationship
    user = relationship("User", back_populates="conversations")

    # Composite Index - Rất quan trọng cho query lịch sử chat
    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
    )

    def __repr__(self):
        return f"<Conversation {self.session_id[:8]}... - {self.role}>"