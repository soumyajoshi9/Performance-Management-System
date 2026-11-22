from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class AIInsightOutputSchema(BaseModel):
    summary: str = Field(..., description="Summary grounded strictly in supplied performance data")
    strengths: List[str] = Field(default_factory=list, description="Demonstrated strengths backed by evidence")
    improvement_areas: List[str] = Field(default_factory=list, description="Opportunities for growth backed by evidence")
    observed_patterns: List[str] = Field(default_factory=list, description="Validated operational patterns")
    contributing_factors: List[str] = Field(default_factory=list, description="Contextual factors (e.g. workload, blockers)")
    recommendations: List[str] = Field(default_factory=list, description="Constructive actions for manager support")
    development_suggestions: List[str] = Field(default_factory=list, description="Concrete skill development suggestions")
    limitations: List[str] = Field(default_factory=list, description="Data limitations or uncertainty notes")
    evidence_references: List[str] = Field(default_factory=list, description="List of cited metric codes, e.g. KPI_TASK_COMPLETION")

class AIInsightGenerateRequest(BaseModel):
    employee_id: str
    review_period_id: str

class FlagInsightRequest(BaseModel):
    flag_reason: str = Field(..., min_length=5)

class AIInsightRead(BaseModel):
    id: str
    employee_id: str
    performance_review_id: Optional[str] = None
    review_period_id: str
    prompt_version: str
    model_version: str
    structured_output: AIInsightOutputSchema
    status: str
    flag_reason: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
