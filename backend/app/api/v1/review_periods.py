from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.review_period import ReviewPeriod
from app.schemas.review_period import ReviewPeriodCreate, ReviewPeriodRead
from app.api.dependencies import require_employee, require_hr
from app.core.exceptions import ConflictError

router = APIRouter(prefix="/review-periods", tags=["Review Periods"])

@router.get("", response_model=List[ReviewPeriodRead])
def list_review_periods(status: Optional[str] = None, db: Session = Depends(get_db), current_user = Depends(require_employee)):
    query = db.query(ReviewPeriod)
    if status:
        query = query.filter(ReviewPeriod.status == status)
    return query.order_by(ReviewPeriod.start_date.desc()).all()

@router.get("/active", response_model=ReviewPeriodRead)
def get_active_period(db: Session = Depends(get_db), current_user = Depends(require_employee)):
    period = db.query(ReviewPeriod).filter(ReviewPeriod.status == "ACTIVE").first()
    if not period:
        # Fallback to latest
        period = db.query(ReviewPeriod).order_by(ReviewPeriod.start_date.desc()).first()
    if not period:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active review period configured.")
    return period

@router.post("", response_model=ReviewPeriodRead, status_code=status.HTTP_201_CREATED)
def create_review_period(data: ReviewPeriodCreate, db: Session = Depends(get_db), current_user = Depends(require_hr)):
    if data.end_date < data.start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end_date must be greater than or equal to start_date.")
    existing = db.query(ReviewPeriod).filter_by(review_month=data.review_month).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Review period for month '{data.review_month}' already exists.")
    period = ReviewPeriod(**data.model_dump())
    db.add(period)
    db.commit()
    db.refresh(period)
    return period
