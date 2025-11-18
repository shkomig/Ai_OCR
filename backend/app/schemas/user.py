"""
User Schemas
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    grade_level: str = Field(..., pattern="^(elementary|middle_school|high_school)$")
    native_language: str = Field(..., pattern="^(hebrew|english|bilingual)$")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    subjects: List[str] = Field(default_factory=list)


class UserUpdate(BaseModel):
    grade_level: Optional[str] = None
    subjects: Optional[List[str]] = None
    preferences: Optional[Dict] = None


class UserResponse(UserBase):
    id: str
    subjects: List[str]
    preferences: Dict
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
