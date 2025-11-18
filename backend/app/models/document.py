"""
Document Model
"""
from sqlalchemy import Column, String, Enum, JSON, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class Subject(str, enum.Enum):
    MATHEMATICS = "mathematics"
    ENGLISH = "english"
    HEBREW = "hebrew"


class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class Document(BaseModel):
    """Document database model"""
    __tablename__ = "documents"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    subject = Column(Enum(Subject), nullable=False)

    # File storage
    raw_image_uri = Column(String(500), nullable=False)

    # OCR Data
    ocr_data = Column(JSON, default=dict)  # {raw_text, confidence_score, extraction_method}

    # Analysis Results
    analysis_results = Column(JSON, default=dict)  # {topics, difficulty_level, learning_objectives}

    # Generated Content References
    generated_content = Column(JSON, default=dict)  # {games: [], quizzes: [], review_materials: []}

    # Processing
    processing_status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING)
    error_message = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", backref="documents")

    def __repr__(self):
        return f"<Document(id='{self.id}', subject='{self.subject}', status='{self.processing_status}')>"
