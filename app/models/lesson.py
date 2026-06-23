# app/models/lesson.py
from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from ..core.database import Base


class Lesson(Base):
    """Bài học cụ thể trong từng chủ đề (4 bài/chủ đề)"""
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    topic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Ordering & type
    order = Column(Integer, nullable=False)      # 1=grammar, 2=vocabulary, 3=practice, 4=quiz
    lesson_type = Column(String(20), nullable=False)  # grammar / vocabulary / practice / quiz

    # Content
    title = Column(String(200), nullable=False)
    title_vi = Column(String(200), nullable=True)

    # Flexible JSON content:
    # grammar: {explanation, examples, notes, key_points}
    # vocabulary: {words: [{word, meaning, example, pronunciation}]}
    # practice: {exercises: [{type, question, options, answer, explanation}]}
    # quiz: {questions: [{id, question, options, correct, explanation}]}
    content = Column(MutableDict.as_mutable(JSONB), nullable=False, default=dict)

    # Relationships
    topic = relationship("Topic", back_populates="lessons")

    def __repr__(self):
        return f"<Lesson {self.lesson_type} (order={self.order}) in topic {self.topic_id}>"
