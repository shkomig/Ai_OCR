"""
User Progress Model
"""
from sqlalchemy import Column, String, Enum, JSON, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class ProgressStatus(str, enum.Enum):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class UserProgress(BaseModel):
    """User progress tracking model"""
    __tablename__ = "user_progress"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    content_id = Column(String(36), ForeignKey("learning_contents.id"), nullable=False, index=True)

    status = Column(Enum(ProgressStatus), default=ProgressStatus.STARTED)
    score = Column(Float, default=0.0)
    time_spent_seconds = Column(Integer, default=0)

    # Detailed answers
    answers = Column(JSON, default=list)  # [{question_id, user_answer, correct_answer, is_correct, time_spent}]

    # AI-generated feedback
    feedback_provided = Column(JSON, default=dict)

    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", backref="progress_records")
    content = relationship("LearningContent", backref="progress_records")

    def __repr__(self):
        return f"<UserProgress(user_id='{self.user_id}', status='{self.status}', score={self.score})>"
