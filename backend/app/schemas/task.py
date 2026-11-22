from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = Field(default="MEDIUM", pattern="^(LOW|MEDIUM|HIGH|URGENT)$")
    complexity: Optional[str] = Field(default="MEDIUM", pattern="^(LOW|MEDIUM|HIGH)$")
    due_date: datetime
    goal_id: Optional[str] = None
    employee_id: Optional[str] = None # Defaults to current user if employee

class TaskStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(TODO|IN_PROGRESS|BLOCKED|COMPLETED|CANCELLED)$")
    blocked_reason: Optional[str] = None

class TaskRead(BaseModel):
    id: str
    employee_id: str
    assigned_by_id: str
    goal_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    complexity: str
    due_date: datetime
    completed_at: Optional[datetime] = None
    is_reopened: bool
    blocked_reason: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
