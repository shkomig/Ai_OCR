"""
Document Schemas
"""
from typing import Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentUpload(BaseModel):
    subject: str = Field(..., pattern="^(mathematics|english|hebrew)$")


class DocumentResponse(BaseModel):
    id: str
    user_id: str
    subject: str
    raw_image_uri: str
    processing_status: str
    ocr_data: Dict
    analysis_results: Dict
    generated_content: Dict
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentStatus(BaseModel):
    status: str
    progress_percentage: int = 0
    estimated_time_seconds: Optional[int] = None
    error_message: Optional[str] = None


class OCRResult(BaseModel):
    raw_text: str
    confidence_score: float
    extraction_method: str
    language_hints: list
