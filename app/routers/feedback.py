from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import Feedback, User
from ..schemas import FeedbackCreate, FeedbackOut
from ..security import get_current_user

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=FeedbackOut, status_code=201)
def submit_feedback(
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    feedback = Feedback(
        user_id=current_user.id if current_user else None,
        user_name=current_user.name if current_user else "Anonymous",
        rating=payload.rating,
        category=payload.category,
        message=payload.message,
        last_meal=payload.last_meal,
        salads_purchased=payload.salads_purchased,
        points=payload.points,
        approved=False,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/approved", response_model=List[FeedbackOut])
def get_approved_feedback(db: Session = Depends(get_db)):
    """Public endpoint — returns only admin-approved feedback for the reviews section."""
    return (
        db.query(Feedback)
        .filter(Feedback.approved == True)
        .order_by(Feedback.created_at.desc())
        .limit(20)
        .all()
    )
