from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=20)
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentRead(DepartmentBase):
    id: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class JobRoleBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=30)
    description: Optional[str] = None

class JobRoleCreate(JobRoleBase):
    department_id: str

class JobRoleRead(JobRoleBase):
    id: str
    department_id: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    full_name: str = Field(..., min_length=2, max_length=150)
    role: str = Field(default="EMPLOYEE", pattern="^(EMPLOYEE|MANAGER|HR|ADMIN)$")
    department_id: Optional[str] = None
    job_role_id: Optional[str] = None
    manager_id: Optional[str] = None
    password: Optional[str] = "DefaultPass123!"

class EmployeeRead(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    department_id: Optional[str] = None
    job_role_id: Optional[str] = None
    manager_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ImportRowError(BaseModel):
    row_number: int
    email: Optional[str] = None
    error: str

class BatchImportResponse(BaseModel):
    batch_id: str
    file_name: str
    total_rows: int
    successful_rows: int
    failed_rows: int
    errors: List[ImportRowError]
