"""
Learning Content Generation Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core import get_db
from app.models import Document, LearningContent, User
from app.schemas import ContentResponse, GameGenerate, QuizGenerate, ReviewGenerate
from app.services import GameService

router = APIRouter()
game_service = GameService()


@router.post("/{document_id}/games", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def generate_game(
    document_id: str,
    game_request: GameGenerate,
    db: Session = Depends(get_db)
):
    """
    Generate an interactive game based on document content
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.processing_status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document processing not completed"
        )

    # Generate game using Claude
    homework_content = document.ocr_data.get("raw_text", "")
    game_data = await game_service.generate_game(
        homework_content=homework_content,
        subject=document.subject,
        analysis_results=document.analysis_results,
        game_type=game_request.game_type
    )

    # Save to database
    content = LearningContent(
        document_id=document.id,
        user_id=document.user_id,
        content_type="game",
        subject=document.subject,
        title=game_data.get("title", "Interactive Game"),
        description=game_data.get("description", ""),
        content_json=game_data,
        metadata={
            "estimated_duration_minutes": 10,
            "learning_objectives": document.analysis_results.get("learning_objectives", []),
            "topics": document.analysis_results.get("topics", [])
        }
    )

    db.add(content)

    # Update document's generated content
    generated = document.generated_content
    if "games" not in generated:
        generated["games"] = []
    generated["games"].append(content.id)
    document.generated_content = generated

    db.commit()
    db.refresh(content)

    return content


@router.post("/{document_id}/quizzes", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def generate_quiz(
    document_id: str,
    quiz_request: QuizGenerate,
    db: Session = Depends(get_db)
):
    """
    Generate a quiz based on document content
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.processing_status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document processing not completed"
        )

    # Generate quiz using Claude
    homework_content = document.ocr_data.get("raw_text", "")
    quiz_data = await game_service.generate_quiz(
        homework_content=homework_content,
        subject=document.subject,
        analysis_results=document.analysis_results,
        difficulty=quiz_request.difficulty
    )

    # Save to database
    content = LearningContent(
        document_id=document.id,
        user_id=document.user_id,
        content_type="quiz",
        subject=document.subject,
        title=quiz_data.get("title", "Practice Quiz"),
        description="Test your knowledge with this interactive quiz",
        content_json=quiz_data,
        metadata={
            "estimated_duration_minutes": quiz_data.get("estimated_duration_minutes", 10),
            "learning_objectives": document.analysis_results.get("learning_objectives", []),
            "topics": document.analysis_results.get("topics", [])
        }
    )

    db.add(content)

    # Update document's generated content
    generated = document.generated_content
    if "quizzes" not in generated:
        generated["quizzes"] = []
    generated["quizzes"].append(content.id)
    document.generated_content = generated

    db.commit()
    db.refresh(content)

    return content


@router.post("/{document_id}/review-materials", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def generate_review_material(
    document_id: str,
    review_request: ReviewGenerate,
    db: Session = Depends(get_db)
):
    """
    Generate review/study material based on document content
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.processing_status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document processing not completed"
        )

    # Generate review material using Claude
    homework_content = document.ocr_data.get("raw_text", "")
    topics = review_request.topics if review_request.topics else document.analysis_results.get("topics", [])

    review_data = await game_service.generate_review_material(
        homework_content=homework_content,
        subject=document.subject,
        topics=topics
    )

    # Save to database
    content = LearningContent(
        document_id=document.id,
        user_id=document.user_id,
        content_type="review",
        subject=document.subject,
        title=review_data.get("title", "Study Guide"),
        description="Comprehensive study guide for review",
        content_json=review_data,
        metadata={
            "estimated_duration_minutes": review_data.get("estimated_study_time_minutes", 15),
            "learning_objectives": document.analysis_results.get("learning_objectives", []),
            "topics": topics
        }
    )

    db.add(content)

    # Update document's generated content
    generated = document.generated_content
    if "review_materials" not in generated:
        generated["review_materials"] = []
    generated["review_materials"].append(content.id)
    document.generated_content = generated

    db.commit()
    db.refresh(content)

    return content


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: str, db: Session = Depends(get_db)):
    """
    Get learning content by ID
    """
    content = db.query(LearningContent).filter(LearningContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Increment view count
    content.views += 1
    db.commit()

    return content


@router.get("/document/{document_id}/all", response_model=List[ContentResponse])
async def list_document_content(document_id: str, db: Session = Depends(get_db)):
    """
    List all generated content for a document
    """
    contents = db.query(LearningContent).filter(
        LearningContent.document_id == document_id
    ).all()

    return contents
