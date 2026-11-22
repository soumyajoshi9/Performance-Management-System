from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.schemas.goal import GoalCreate, GoalUpdateProgress, GoalApprovalAction, GoalRead
from app.services.goal_service import GoalService
from app.api.dependencies import get_current_user, require_employee, require_manager
from app.core.exceptions import EntityNotFoundError, AuthorizationError, ValidationError
from app.models.user import User

router = APIRouter(prefix="/goals", tags=["Goals Management"])

@router.get("", response_model=List[GoalRead])
def list_goals(
    employee_id: Optional[str] = None,
    review_period_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return GoalService.get_goals(
        db, current_user, employee_id=employee_id, review_period_id=review_period_id, status=status
    )

@router.post("", response_model=GoalRead, status_code=status.HTTP_201_CREATED)
def create_goal(data: GoalCreate, db: Session = Depends(get_db), current_user: User = Depends(require_employee)):
    try:
        return GoalService.create_goal(db, data, current_user)
    except (EntityNotFoundError, AuthorizationError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.patch("/{id}/progress", response_model=GoalRead)
def update_goal_progress(id: str, data: GoalUpdateProgress, db: Session = Depends(get_db), current_user: User = Depends(require_employee)):
    try:
        return GoalService.update_progress(db, id, data, current_user)
    except (EntityNotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.post("/{id}/approval", response_model=GoalRead)
def approve_or_reject_goal(id: str, action: GoalApprovalAction, db: Session = Depends(get_db), current_user: User = Depends(require_manager)):
    try:
        return GoalService.process_approval(db, id, action, current_user)
    except (EntityNotFoundError, AuthorizationError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
