"""
Progress Schemas
"""
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime


class AnswerSubmission(BaseModel):
    question_id: str
    user_answer: str
    time_spent_seconds: int = 0


class ProgressSubmit(BaseModel):
    content_id: str
    answers: List[AnswerSubmission]
    total_time_spent: int


class ProgressResponse(BaseModel):
    id: str
    user_id: str
    content_id: str
    status: str
    score: float
    time_spent_seconds: int
    answers: List[Dict]
    feedback_provided: Dict
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    total_documents: int
    total_games_played: int
    total_quizzes_completed: int
    average_score: float
    total_study_time_minutes: int
    recent_activities: List[Dict]
    subject_breakdown: Dict
