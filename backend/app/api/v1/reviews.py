from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.review import PerformanceReview
from app.models.user import User
from app.schemas.review import ReviewDraftRequest, ReviewFinalizeRequest, PerformanceReviewRead
from app.services.review_service import ReviewService
from app.api.dependencies import get_current_user, require_manager, require_employee
from app.core.exceptions import EntityNotFoundError, ConflictError, AuthorizationError

router = APIRouter(prefix="/reviews", tags=["Performance Reviews & Snapshots"])

@router.get("", response_model=List[PerformanceReviewRead])
def list_reviews(
    employee_id: Optional[str] = None,
    review_period_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(PerformanceReview)
    
    if current_user.role == "EMPLOYEE":
        query = query.filter(PerformanceReview.employee_id == current_user.id)
    elif current_user.role == "MANAGER":
        if employee_id:
            query = query.filter(PerformanceReview.employee_id == employee_id)
        else:
            report_ids = [u.id for u in db.query(User.id).filter(User.manager_id == current_user.id).all()]
            report_ids.append(current_user.id)
            query = query.filter(PerformanceReview.employee_id.in_(report_ids))
    else:
        if employee_id:
            query = query.filter(PerformanceReview.employee_id == employee_id)
            
    if review_period_id:
        query = query.filter(PerformanceReview.review_period_id == review_period_id)
    if status:
        query = query.filter(PerformanceReview.status == status)
        
    reviews = query.order_by(PerformanceReview.created_at.desc()).all()
    return [PerformanceReviewRead.model_validate(r) for r in reviews]

@router.get("/{id}", response_model=PerformanceReviewRead)
def get_review(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = db.query(PerformanceReview).filter_by(id=id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Performance review not found.")
        
    if current_user.role == "EMPLOYEE" and review.employee_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    if current_user.role == "MANAGER":
        emp = db.query(User).filter_by(id=review.employee_id).first()
        if emp.manager_id != current_user.id and emp.id != current_user.id and current_user.role != "ADMIN":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access restricted to direct reports.")
            
    return PerformanceReviewRead.model_validate(review)

@router.post("/draft", response_model=PerformanceReviewRead)
def get_or_create_draft(data: ReviewDraftRequest, db: Session = Depends(get_db), current_user: User = Depends(require_manager)):
    try:
        review = ReviewService.get_or_create_draft(db, data.employee_id, data.review_period_id, current_user)
        return PerformanceReviewRead.model_validate(review)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

@router.post("/{id}/finalize", response_model=PerformanceReviewRead)
def finalize_review(id: str, data: ReviewFinalizeRequest, db: Session = Depends(get_db), current_user: User = Depends(require_manager)):
    try:
        review = ReviewService.finalize_review(db, id, data, current_user)
        return PerformanceReviewRead.model_validate(review)
    except (EntityNotFoundError, ConflictError, AuthorizationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
