from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class ReviewDraftRequest(BaseModel):
    employee_id: str
    review_period_id: str

class ReviewFinalizeRequest(BaseModel):
    manager_summary: str = Field(..., min_length=5)
    employee_remarks: Optional[str] = None

class MetricSnapshotRead(BaseModel):
    id: str
    kpi_code: str
    kpi_name: str
    category: str
    raw_value: Optional[Decimal] = None
    normalized_score: Optional[Decimal] = None
    applied_weight: Decimal
    evidence_count: int
    is_sufficient: bool
    data_status: str
    snapshot_data: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PerformanceReviewRead(BaseModel):
    id: str
    employee_id: str
    reviewer_id: str
    review_period_id: str
    status: str
    score_status: str
    calculated_score: Optional[Decimal] = None
    final_score: Optional[Decimal] = None
    data_coverage_percentage: Decimal
    manager_summary: Optional[str] = None
    employee_remarks: Optional[str] = None
    finalized_at: Optional[datetime] = None
    created_at: datetime
    metric_snapshots: Optional[List[MetricSnapshotRead]] = []

    class Config:
        from_attributes = True
