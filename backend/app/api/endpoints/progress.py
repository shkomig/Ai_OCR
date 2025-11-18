"""
Progress Tracking and Analytics Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime

from app.core import get_db
from app.models import UserProgress, LearningContent, User, Document
from app.schemas import ProgressSubmit, ProgressResponse, DashboardResponse
from app.services import ClaudeService

router = APIRouter()
claude_service = ClaudeService()


@router.post("/submit", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
async def submit_progress(
    progress_data: ProgressSubmit,
    db: Session = Depends(get_db)
):
    """
    Submit user's progress for a learning content
    """
    # Get current user (simplified)
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Get content
    content = db.query(LearningContent).filter(
        LearningContent.id == progress_data.content_id
    ).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Calculate score
    content_json = content.content_json
    questions = content_json.get("questions", [])

    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content has no questions"
        )

    # Process answers
    processed_answers = []
    correct_count = 0
    total_points = 0
    earned_points = 0

    for answer_submission in progress_data.answers:
        # Find the corresponding question
        question = next(
            (q for q in questions if q.get("id") == answer_submission.question_id),
            None
        )

        if not question:
            continue

        correct_answer = question.get("correct_answer", "")
        is_correct = answer_submission.user_answer.strip().lower() == correct_answer.strip().lower()

        if is_correct:
            correct_count += 1
            points = question.get("points", 10)
            earned_points += points

        total_points += question.get("points", 10)

        # Generate feedback using Claude
        feedback = await claude_service.provide_feedback(
            question=question.get("question", ""),
            user_answer=answer_submission.user_answer,
            correct_answer=correct_answer,
            is_correct=is_correct
        )

        processed_answers.append({
            "question_id": answer_submission.question_id,
            "user_answer": answer_submission.user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "time_spent_seconds": answer_submission.time_spent_seconds,
            "feedback": feedback
        })

    # Calculate final score
    final_score = (earned_points / total_points * 100) if total_points > 0 else 0

    # Create progress record
    progress = UserProgress(
        user_id=user.id,
        content_id=content.id,
        status="completed",
        score=final_score,
        time_spent_seconds=progress_data.total_time_spent,
        answers=processed_answers,
        feedback_provided={
            "overall_score": final_score,
            "correct_answers": correct_count,
            "total_questions": len(questions),
            "message": "Excellent work!" if final_score >= 90 else "Great job!" if final_score >= 70 else "Keep practicing!"
        },
        completed_at=datetime.utcnow()
    )

    db.add(progress)

    # Update content engagement metrics
    content.completions += 1
    current_avg = content.average_score
    content.average_score = (
        (current_avg * (content.completions - 1) + final_score) / content.completions
    )
    content.completion_rate = content.completions / max(content.views, 1)

    db.commit()
    db.refresh(progress)

    return progress


@router.get("/user/{user_id}", response_model=List[ProgressResponse])
async def get_user_progress(
    user_id: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get user's progress history
    """
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).order_by(UserProgress.created_at.desc()).offset(skip).limit(limit).all()

    return progress_records


@router.get("/user/{user_id}/dashboard", response_model=DashboardResponse)
async def get_user_dashboard(user_id: str, db: Session = Depends(get_db)):
    """
    Get aggregated dashboard data for a user
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Total documents
    total_documents = db.query(Document).filter(Document.user_id == user_id).count()

    # Total games and quizzes
    total_games = db.query(UserProgress).join(LearningContent).filter(
        UserProgress.user_id == user_id,
        LearningContent.content_type == "game"
    ).count()

    total_quizzes = db.query(UserProgress).join(LearningContent).filter(
        UserProgress.user_id == user_id,
        LearningContent.content_type == "quiz"
    ).count()

    # Average score
    avg_score_result = db.query(func.avg(UserProgress.score)).filter(
        UserProgress.user_id == user_id
    ).scalar()
    average_score = float(avg_score_result) if avg_score_result else 0.0

    # Total study time
    total_time_result = db.query(func.sum(UserProgress.time_spent_seconds)).filter(
        UserProgress.user_id == user_id
    ).scalar()
    total_study_time_minutes = int(total_time_result / 60) if total_time_result else 0

    # Recent activities
    recent_progress = db.query(UserProgress).join(LearningContent).filter(
        UserProgress.user_id == user_id
    ).order_by(UserProgress.created_at.desc()).limit(10).all()

    recent_activities = []
    for progress in recent_progress:
        recent_activities.append({
            "content_title": progress.content.title,
            "content_type": progress.content.content_type,
            "score": progress.score,
            "completed_at": progress.completed_at.isoformat() if progress.completed_at else None
        })

    # Subject breakdown
    subject_results = db.query(
        LearningContent.subject,
        func.count(UserProgress.id).label("count")
    ).join(UserProgress).filter(
        UserProgress.user_id == user_id
    ).group_by(LearningContent.subject).all()

    subject_breakdown = {subject: count for subject, count in subject_results}

    return {
        "total_documents": total_documents,
        "total_games_played": total_games,
        "total_quizzes_completed": total_quizzes,
        "average_score": average_score,
        "total_study_time_minutes": total_study_time_minutes,
        "recent_activities": recent_activities,
        "subject_breakdown": subject_breakdown
    }


@router.get("/content/{content_id}", response_model=List[ProgressResponse])
async def get_content_progress(
    content_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all progress records for a specific content
    """
    progress_records = db.query(UserProgress).filter(
        UserProgress.content_id == content_id
    ).order_by(UserProgress.created_at.desc()).all()

    return progress_records
