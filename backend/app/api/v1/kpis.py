from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.kpi import KPIDefinition, RoleKPIConfig
from app.schemas.kpi import KPIDefinitionRead, RoleKPIConfigRead, RoleKPIConfigUpdate
from app.api.dependencies import require_employee, require_hr
from app.core.exceptions import EntityNotFoundError

router = APIRouter(prefix="/kpis", tags=["KPIs & Role Templates"])

@router.get("/definitions", response_model=List[KPIDefinitionRead])
def list_kpi_definitions(db: Session = Depends(get_db), current_user = Depends(require_employee)):
    return db.query(KPIDefinition).filter_by(is_active=True).all()

@router.get("/role-configs/{job_role_id}", response_model=List[RoleKPIConfigRead])
def get_role_kpi_configs(job_role_id: str, db: Session = Depends(get_db), current_user = Depends(require_employee)):
    return db.query(RoleKPIConfig).filter_by(job_role_id=job_role_id).all()

@router.put("/role-configs/{id}", response_model=RoleKPIConfigRead)
def update_role_kpi_config(id: str, data: RoleKPIConfigUpdate, db: Session = Depends(get_db), current_user = Depends(require_hr)):
    cfg = db.query(RoleKPIConfig).filter_by(id=id).first()
    if not cfg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role KPI Config not found.")
    cfg.default_weight = data.default_weight
    cfg.min_evidence_threshold = data.min_evidence_threshold
    db.commit()
    db.refresh(cfg)
    return cfg
