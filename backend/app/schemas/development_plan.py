from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime

class ActionItemSchema(BaseModel):
    id: str = Field(..., description="Unique action item milestone ID")
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    target_date: Optional[date] = None
    is_completed: bool = False

class DevelopmentPlanCreate(BaseModel):
    employee_id: str
    review_period_id: Optional[str] = None
    ai_insight_id: Optional[str] = None
    title: str = Field(..., min_length=3, max_length=255)
    objective: str = Field(..., min_length=5)
    start_date: date
    target_completion_date: date
    action_items: List[ActionItemSchema] = []

class DevelopmentPlanAgreementRequest(BaseModel):
    agreed: bool

class ActionItemToggleRequest(BaseModel):
    is_completed: bool

class DevelopmentPlanRead(BaseModel):
    id: str
    employee_id: str
    manager_id: str
    review_period_id: Optional[str] = None
    ai_insight_id: Optional[str] = None
    title: str
    objective: str
    status: str
    employee_agreed: bool
    manager_agreed: bool
    action_items: List[ActionItemSchema]
    start_date: date
    target_completion_date: date
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
