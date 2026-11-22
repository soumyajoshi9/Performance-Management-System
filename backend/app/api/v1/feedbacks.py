from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.feedback import Feedback
from app.models.user import User
from app.models.review_period import ReviewPeriod
from app.schemas.feedback import FeedbackCreate, FeedbackRead
from app.api.dependencies import get_current_user, require_employee
from app.core.exceptions import EntityNotFoundError, AuthorizationError

router = APIRouter(prefix="/feedbacks", tags=["Qualitative Feedback & Self-Assessment"])

@router.post("", response_model=FeedbackRead, status_code=status.HTTP_201_CREATED)
def create_feedback(data: FeedbackCreate, db: Session = Depends(get_db), current_user: User = Depends(require_employee)):
    # Auth boundaries (DB-5):
    if data.feedback_type == "SELF_ASSESSMENT":
        if current_user.id != data.employee_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot submit self-assessment for another employee.")
    elif data.feedback_type == "MANAGER_TO_EMPLOYEE":
        if current_user.role not in ("MANAGER", "HR", "ADMIN"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only managers or HR can submit managerial feedback.")
        target_emp = db.query(User).filter_by(id=data.employee_id).first()
        if not target_emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target employee not found.")
        if current_user.role == "MANAGER" and target_emp.manager_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Managers can only submit feedback for direct reports.")

    fb = Feedback(
        employee_id=data.employee_id,
        author_id=current_user.id,
        review_period_id=data.review_period_id,
        feedback_type=data.feedback_type,
        content=data.content,
        strengths=data.strengths,
        growth_areas=data.growth_areas
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb

@router.get("", response_model=List[FeedbackRead])
def get_feedbacks(
    employee_id: Optional[str] = None,
    review_period_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Feedback)
    
    if current_user.role == "EMPLOYEE":
        query = query.filter(Feedback.employee_id == current_user.id)
    elif current_user.role == "MANAGER":
        if employee_id:
            query = query.filter(Feedback.employee_id == employee_id)
        else:
            report_ids = [u.id for u in db.query(User.id).filter(User.manager_id == current_user.id).all()]
            report_ids.append(current_user.id)
            query = query.filter(Feedback.employee_id.in_(report_ids))
    else:
        if employee_id:
            query = query.filter(Feedback.employee_id == employee_id)
            
    if review_period_id:
        query = query.filter(Feedback.review_period_id == review_period_id)
        
    return query.order_by(Feedback.created_at.desc()).all()
