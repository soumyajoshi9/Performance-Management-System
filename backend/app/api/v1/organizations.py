from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.schemas.organization import (
    DepartmentCreate, DepartmentRead, JobRoleCreate, JobRoleRead, BatchImportResponse
)
from app.services.organization_service import OrganizationService
from app.api.dependencies import require_hr, require_employee, get_current_user
from app.core.exceptions import EntityNotFoundError, ConflictError, ValidationError
from app.models.user import User

router = APIRouter(prefix="/organizations", tags=["Organizations & Departments"])

@router.get("/departments", response_model=List[DepartmentRead])
def list_departments(db: Session = Depends(get_db), current_user: User = Depends(require_employee)):
    return OrganizationService.get_departments(db)

@router.post("/departments", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_hr)):
    try:
        return OrganizationService.create_department(db, data)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

@router.get("/job-roles", response_model=List[JobRoleRead])
def list_job_roles(department_id: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(require_employee)):
    return OrganizationService.get_job_roles(db, department_id=department_id)

@router.post("/job-roles", response_model=JobRoleRead, status_code=status.HTTP_201_CREATED)
def create_job_role(data: JobRoleCreate, db: Session = Depends(get_db), current_user: User = Depends(require_hr)):
    try:
        return OrganizationService.create_job_role(db, data)
    except (EntityNotFoundError, ConflictError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.post("/import/employees", response_model=BatchImportResponse)
async def import_employees(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(require_hr)):
    if not file.filename.endswith((".csv", ".txt")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only UTF-8 CSV files supported.")
    content = await file.read()
    try:
        return OrganizationService.import_employees_csv(db, content, file.filename, current_user.id)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
