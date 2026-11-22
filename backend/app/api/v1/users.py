from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.schemas.organization import EmployeeCreate, EmployeeRead
from app.services.organization_service import OrganizationService
from app.api.dependencies import get_current_user, require_manager, require_hr
from app.core.exceptions import EntityNotFoundError, ConflictError
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users & Directory"])

@router.get("", response_model=List[EmployeeRead])
def list_employees(
    department_id: Optional[str] = None,
    manager_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(User).filter(User.is_active == True)
    
    # RBAC boundary enforcement:
    if current_user.role == "EMPLOYEE":
        # Employees only see colleagues in their department or self
        query = query.filter(User.department_id == current_user.department_id)
    elif current_user.role == "MANAGER":
        # Managers view team members reporting to them or their department
        query = query.filter((User.manager_id == current_user.id) | (User.department_id == current_user.department_id))
    # HR & Admin can see all

    if department_id:
        query = query.filter(User.department_id == department_id)
    if manager_id:
        query = query.filter(User.manager_id == manager_id)
        
    return query.offset(skip).limit(limit).all()

@router.get("/{id}", response_model=EmployeeRead)
def get_employee(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        
    # Boundary check:
    if current_user.role == "EMPLOYEE" and current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to other employee records.")
    if current_user.role == "MANAGER" and user.manager_id != current_user.id and user.department_id != current_user.department_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access restricted to direct reports.")
        
    return user

@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db), current_user: User = Depends(require_hr)):
    try:
        return OrganizationService.create_employee(db, data)
    except (ConflictError, EntityNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
