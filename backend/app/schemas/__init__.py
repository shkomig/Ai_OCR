"""
Pydantic Schemas
"""
from .user import UserCreate, UserUpdate, UserResponse, UserLogin, Token, TokenData
from .document import DocumentUpload, DocumentResponse, DocumentStatus, OCRResult
from .content import ContentResponse, GameGenerate, QuizGenerate, ReviewGenerate
from .progress import ProgressSubmit, ProgressResponse, DashboardResponse, AnswerSubmission

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    "DocumentUpload",
    "DocumentResponse",
    "DocumentStatus",
    "OCRResult",
    "ContentResponse",
    "GameGenerate",
    "QuizGenerate",
    "ReviewGenerate",
    "ProgressSubmit",
    "ProgressResponse",
    "DashboardResponse",
    "AnswerSubmission",
]
