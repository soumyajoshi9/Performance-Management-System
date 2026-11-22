from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.user import User
from app.schemas.development_plan import (
    DevelopmentPlanCreate, DevelopmentPlanAgreementRequest,
    ActionItemToggleRequest, DevelopmentPlanRead
)
from app.services.development_service import DevelopmentService
from app.api.dependencies import get_current_user, require_manager, require_employee
from app.core.exceptions import EntityNotFoundError, AuthorizationError, ValidationError

router = APIRouter(prefix="/development-plans", tags=["Collaborative Development Plans"])

@router.get("", response_model=List[DevelopmentPlanRead])
def list_development_plans(
    employee_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plans = DevelopmentService.list_plans(db, current_user, employee_id=employee_id)
    return [DevelopmentPlanRead.model_validate(p) for p in plans]

@router.post("", response_model=DevelopmentPlanRead, status_code=status.HTTP_201_CREATED)
def create_development_plan(data: DevelopmentPlanCreate, db: Session = Depends(get_db), current_user: User = Depends(require_manager)):
    try:
        plan = DevelopmentService.create_plan(db, data, current_user)
        return DevelopmentPlanRead.model_validate(plan)
    except (EntityNotFoundError, AuthorizationError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.post("/{id}/agreement", response_model=DevelopmentPlanRead)
def record_plan_agreement(id: str, data: DevelopmentPlanAgreementRequest, db: Session = Depends(get_db), current_user: User = Depends(require_employee)):
    try:
        plan = DevelopmentService.record_agreement(db, id, data, current_user)
        return DevelopmentPlanRead.model_validate(plan)
    except (EntityNotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.patch("/{id}/action-items/{item_id}", response_model=DevelopmentPlanRead)
def toggle_action_item(id: str, item_id: str, data: ActionItemToggleRequest, db: Session = Depends(get_db), current_user: User = Depends(require_employee)):
    try:
        plan = DevelopmentService.toggle_action_item(db, id, item_id, data, current_user)
        return DevelopmentPlanRead.model_validate(plan)
    except (EntityNotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
