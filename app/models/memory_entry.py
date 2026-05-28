# app/models/memory_entry.py
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from app.core.database import Base


class MemoryEntry(Base):
    __tablename__ = "memory_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), 
                     nullable=False, index=True)
    
    skill_type = Column(String, nullable=False, index=True)      # strong / weak
    skill_name = Column(String, nullable=False, index=True)
    
    frequency = Column(Integer, default=1)
    confidence_score = Column(Float, default=0.0)                # Đổi thành Float
    
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    extra_data = Column(JSONB, default=dict)

    user = relationship("User", back_populates="memories")

    __table_args__ = (
        UniqueConstraint("user_id", "skill_name", name="uq_user_skill"),
    )

    def __repr__(self):
        return f"<MemoryEntry {self.skill_type}:{self.skill_name}>"