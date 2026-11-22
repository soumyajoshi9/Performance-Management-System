from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.base import Base

class ImportBatch(Base):
    __tablename__ = "import_batches"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    imported_by_id = Column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False, default="EMPLOYEE")
    file_name = Column(String(255), nullable=False)
    total_rows = Column(Integer, nullable=False)
    successful_rows = Column(Integer, nullable=False)
    failed_rows = Column(Integer, nullable=False)
    error_log = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    imported_by = relationship("User", foreign_keys=[imported_by_id])

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(36), nullable=True)
    ip_address = Column(String(45), nullable=True)
    changes = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", foreign_keys=[user_id])
