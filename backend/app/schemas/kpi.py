from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class KPIDefinitionRead(BaseModel):
    id: str
    code: str
    name: str
    description: str
    category: str
    unit: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoleKPIConfigRead(BaseModel):
    id: str
    job_role_id: str
    kpi_definition_id: str
    default_weight: Decimal
    min_evidence_threshold: int
    is_mandatory: bool
    
    class Config:
        from_attributes = True

class RoleKPIConfigUpdate(BaseModel):
    default_weight: Decimal = Field(..., ge=Decimal("0.0"), le=Decimal("100.0"))
    min_evidence_threshold: int = Field(..., ge=1)
