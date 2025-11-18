"""
Learning Content Model
"""
from sqlalchemy import Column, String, Enum, JSON, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class ContentType(str, enum.Enum):
    GAME = "game"
    QUIZ = "quiz"
    REVIEW = "review"


class LearningContent(BaseModel):
    """Learning content database model"""
    __tablename__ = "learning_contents"

    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    content_type = Column(Enum(ContentType), nullable=False)
    subject = Column(String(50), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Full content as JSON
    content_json = Column(JSON, nullable=False)

    # Metadata
    metadata = Column(JSON, default=dict)  # {estimated_duration_minutes, learning_objectives, topics}

    # Engagement metrics
    views = Column(Integer, default=0)
    completions = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    completion_rate = Column(Float, default=0.0)

    # Relationships
    document = relationship("Document", backref="learning_contents")
    user = relationship("User", backref="learning_contents")

    def __repr__(self):
        return f"<LearningContent(title='{self.title}', type='{self.content_type}')>"
