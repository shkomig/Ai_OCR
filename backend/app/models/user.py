"""
User Model
"""
from sqlalchemy import Column, String, Enum, JSON
import enum
from .base import BaseModel


class GradeLevel(str, enum.Enum):
    ELEMENTARY = "elementary"
    MIDDLE = "middle_school"
    HIGH_SCHOOL = "high_school"


class Language(str, enum.Enum):
    HEBREW = "hebrew"
    ENGLISH = "english"
    BILINGUAL = "bilingual"


class User(BaseModel):
    """User database model"""
    __tablename__ = "users"

    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    grade_level = Column(Enum(GradeLevel), nullable=False)
    native_language = Column(Enum(Language), nullable=False)

    # JSON field for subjects array and preferences
    subjects = Column(JSON, default=list)  # ["mathematics", "english", "hebrew"]
    preferences = Column(JSON, default=dict)  # {game_difficulty, learning_style, etc.}

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
