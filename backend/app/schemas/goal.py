from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class GoalCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = "PROJECT"
    target_metric: str = Field(..., min_length=2, max_length=100)
    start_value: Decimal = Decimal("0.00")
    target_value: Decimal = Field(..., gt=Decimal("0.00"))
    unit: Optional[str] = "percent"
    due_date: date
    review_period_id: str
    employee_id: Optional[str] = None # Defaults to current user if employee

class GoalUpdateProgress(BaseModel):
    current_value: Decimal = Field(..., ge=Decimal("0.00"))

class GoalApprovalAction(BaseModel):
    action: str = Field(..., pattern="^(APPROVE|REJECT)$")
    rejection_reason: Optional[str] = None

class GoalRead(BaseModel):
    id: str
    employee_id: str
    created_by_id: str
    review_period_id: str
    title: str
    description: Optional[str] = None
    category: str
    target_metric: str
    start_value: Decimal
    target_value: Decimal
    current_value: Decimal
    unit: str
    status: str
    approval_status: str
    approved_by_id: Optional[str] = None
    rejection_reason: Optional[str] = None
    due_date: date
    created_at: datetime
    progress_percentage: float = 0.0

    class Config:
        from_attributes = True
