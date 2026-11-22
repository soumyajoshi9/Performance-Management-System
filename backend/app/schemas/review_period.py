from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class ReviewPeriodCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    start_date: date
    end_date: date
    review_month: str = Field(..., pattern="^[0-9]{4}-[0-9]{2}$") # e.g. '2026-11'
    status: Optional[str] = "UPCOMING"

class ReviewPeriodRead(BaseModel):
    id: str
    name: str
    start_date: date
    end_date: date
    review_month: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
