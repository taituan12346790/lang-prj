# app/models/topic.py
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from ..core.database import Base


class Topic(Base):
    """Chủ đề học tập theo từng level CEFR"""
    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Level & ordering
    level = Column(String(2), nullable=False, index=True)   # A1, A2, B1, B2, C1, C2
    order = Column(Integer, nullable=False)                  # Thứ tự học trong level

    # Names
    name = Column(String(100), nullable=False)               # "Personal Pronouns"
    name_vi = Column(String(100), nullable=False)            # "Đại từ nhân xưng"

    # Content info
    description = Column(Text, nullable=True)
    description_vi = Column(Text, nullable=True)
    grammar_focus = Column(MutableList.as_mutable(JSONB), default=list)   # ["to be", "pronouns"]
    vocabulary_tags = Column(MutableList.as_mutable(JSONB), default=list) # ["greeting", "identity"]
    estimated_minutes = Column(Integer, default=30)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    lessons = relationship("Lesson", back_populates="topic", order_by="Lesson.order", cascade="all, delete-orphan")
    user_progress = relationship("UserTopicProgress", back_populates="topic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Topic {self.level}-{self.order}: {self.name}>"
