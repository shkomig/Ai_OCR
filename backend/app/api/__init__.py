"""
API Routes
"""
from fastapi import APIRouter
from .endpoints import auth, documents, content, progress

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(content.router, prefix="/content", tags=["Learning Content"])
api_router.include_router(progress.router, prefix="/progress", tags=["Progress & Analytics"])
