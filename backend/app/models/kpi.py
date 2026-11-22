from sqlalchemy import Column, String, Text, Boolean, Integer, Numeric, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.base import Base

class KPIDefinition(Base):
    __tablename__ = "kpi_definitions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(30), nullable=False, index=True) # TASK, GOAL, QUALITY, CONSISTENCY, DEADLINE
    unit = Column(String(30), nullable=False, default="percentage")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    role_configs = relationship("RoleKPIConfig", back_populates="kpi_definition", cascade="all, delete-orphan")

class RoleKPIConfig(Base):
    __tablename__ = "role_kpi_configs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_role_id = Column(String(36), ForeignKey("job_roles.id", ondelete="CASCADE"), nullable=False, index=True)
    kpi_definition_id = Column(String(36), ForeignKey("kpi_definitions.id", ondelete="RESTRICT"), nullable=False)
    default_weight = Column(Numeric(5, 2), nullable=False)
    min_evidence_threshold = Column(Integer, nullable=False, default=3)
    is_mandatory = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("job_role_id", "kpi_definition_id", name="uq_role_kpi_configs"),
    )

    job_role = relationship("JobRole", back_populates="role_kpi_configs")
    kpi_definition = relationship("KPIDefinition", back_populates="role_configs")
