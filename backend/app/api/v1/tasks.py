from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.schemas.task import TaskCreate, TaskStatusUpdate, TaskRead
from app.services.task_service import TaskService
from app.api.dependencies import get_current_user, require_employee
from app.core.exceptions import EntityNotFoundError, AuthorizationError, ValidationError
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Task Management"])

@router.get("", response_model=List[TaskRead])
def list_tasks(
    employee_id: Optional[str] = None,
    goal_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = TaskService.get_tasks(db, current_user, employee_id=employee_id, goal_id=goal_id, status=status)
    return [TaskRead.model_validate(t) for t in tasks]

@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(require_employee)):
    try:
        task = TaskService.create_task(db, data, current_user)
        return TaskRead.model_validate(task)
    except (EntityNotFoundError, AuthorizationError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.patch("/{id}/status", response_model=TaskRead)
def update_task_status(id: str, data: TaskStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_employee)):
    try:
        task = TaskService.update_status(db, id, data, current_user)
        return TaskRead.model_validate(task)
    except (EntityNotFoundError, AuthorizationError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
