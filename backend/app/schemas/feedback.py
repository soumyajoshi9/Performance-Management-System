from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    employee_id: str
    review_period_id: str
    feedback_type: str = Field(..., pattern="^(MANAGER_TO_EMPLOYEE|SELF_ASSESSMENT)$")
    content: str = Field(..., min_length=5)
    strengths: Optional[str] = None
    growth_areas: Optional[str] = None

class FeedbackRead(BaseModel):
    id: str
    employee_id: str
    author_id: str
    review_period_id: str
    feedback_type: str
    content: str
    strengths: Optional[str] = None
    growth_areas: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
