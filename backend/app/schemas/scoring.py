from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ScoringPreviewRequest(BaseModel):
    employee_id: str
    review_period_id: str

class MetricEvaluationRead(BaseModel):
    kpi_code: str
    kpi_name: str
    category: str
    unit: str
    default_weight: float
    applied_weight: float
    min_evidence_threshold: int
    raw_value: Optional[float] = None
    normalized_score: Optional[float] = None
    evidence_count: int
    is_sufficient: bool
    data_status: str

class WorkloadContextRead(BaseModel):
    active_tasks_count: int
    high_complexity_count: int
    medium_complexity_count: int
    low_complexity_count: int
    overdue_tasks_count: int
    blocked_tasks_count: int
    workload_status: str
    context_notes: str

class ScoreBreakdownResponse(BaseModel):
    employee_id: str
    employee_name: str
    review_period_id: str
    score_status: str
    calculated_score: Optional[float] = None
    data_coverage_percentage: float
    is_sufficient: bool
    workload_context: WorkloadContextRead
    metrics: List[MetricEvaluationRead]
