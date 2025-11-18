"""
Learning Content Schemas
"""
from typing import Dict, List
from pydantic import BaseModel
from datetime import datetime


class ContentResponse(BaseModel):
    id: str
    document_id: str
    user_id: str
    content_type: str
    subject: str
    title: str
    description: str
    content_json: Dict
    metadata: Dict
    views: int
    completions: int
    average_score: float
    completion_rate: float
    created_at: datetime

    class Config:
        from_attributes = True


class GameGenerate(BaseModel):
    game_type: str = "auto"


class QuizGenerate(BaseModel):
    difficulty: str = "medium"


class ReviewGenerate(BaseModel):
    topics: List[str] = []
