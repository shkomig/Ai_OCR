"""
Document Upload and Processing Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import os
from datetime import datetime

from app.core import get_db, settings
from app.models import Document, User
from app.schemas import DocumentResponse, DocumentStatus
from app.services import OCRService, ClaudeService

router = APIRouter()
ocr_service = OCRService()
claude_service = ClaudeService()


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    subject: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload a homework document image
    """
    # Get current user (simplified - in production, get from token)
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    # Read file content
    file_content = await file.read()

    # Validate file size
    if len(file_content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
        )

    # Save file temporarily (in production, upload to cloud storage)
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_extension = file.filename.split('.')[-1] if file.filename else 'jpg'
    file_path = f"{upload_dir}/{file_id}.{file_extension}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    # Create document record
    document = Document(
        user_id=user.id,
        subject=subject,
        raw_image_uri=file_path,
        processing_status="pending",
        ocr_data={},
        analysis_results={},
        generated_content={"games": [], "quizzes": [], "review_materials": []}
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Start processing asynchronously (in production, use background tasks or queue)
    try:
        # Update status to processing
        document.processing_status = "processing"
        db.commit()

        # Process OCR
        ocr_result = await ocr_service.process_document(file_content)
        document.ocr_data = ocr_result["ocr_data"]

        # Analyze content with Claude
        analysis = await claude_service.analyze_homework_content(
            ocr_text=ocr_result["ocr_data"].get("raw_text", ""),
            subject=subject
        )
        document.analysis_results = analysis

        # Mark as completed
        document.processing_status = "completed"
        db.commit()
        db.refresh(document)

    except Exception as e:
        document.processing_status = "error"
        document.error_message = str(e)
        db.commit()

    return document


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, db: Session = Depends(get_db)):
    """
    Get document details by ID
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/{document_id}/status", response_model=DocumentStatus)
async def get_document_status(document_id: str, db: Session = Depends(get_db)):
    """
    Get processing status of a document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    progress = 0
    if document.processing_status == "pending":
        progress = 0
    elif document.processing_status == "processing":
        progress = 50
    elif document.processing_status == "completed":
        progress = 100
    elif document.processing_status == "error":
        progress = 0

    return {
        "status": document.processing_status,
        "progress_percentage": progress,
        "estimated_time_seconds": 10 if progress < 100 else 0,
        "error_message": document.error_message
    }


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str, db: Session = Depends(get_db)):
    """
    Delete a document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete file from storage
    if os.path.exists(document.raw_image_uri):
        os.remove(document.raw_image_uri)

    db.delete(document)
    db.commit()
    return None


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    List user's documents
    """
    # Get current user (simplified)
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    documents = db.query(Document).filter(
        Document.user_id == user.id
    ).offset(skip).limit(limit).all()

    return documents
