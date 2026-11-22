from sqlalchemy import Column, String, Text, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.base import Base

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_id = Column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    review_period_id = Column(String(36), ForeignKey("review_periods.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False, default="PROJECT")
    target_metric = Column(String(100), nullable=False)
    start_value = Column(Numeric(10, 2), nullable=False, default=0.00)
    target_value = Column(Numeric(10, 2), nullable=False)
    current_value = Column(Numeric(10, 2), nullable=False, default=0.00)
    unit = Column(String(30), nullable=False, default="percent")
    
    status = Column(String(30), nullable=False, default="ACTIVE") # DRAFT, PENDING_APPROVAL, ACTIVE, COMPLETED, CANCELLED
    approval_status = Column(String(30), nullable=False, default="APPROVED") # PENDING, APPROVED, REJECTED
    approved_by_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    due_date = Column(Date, nullable=False)
    
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    employee = relationship("User", foreign_keys=[employee_id], back_populates="goals")
    created_by = relationship("User", foreign_keys=[created_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])
    review_period = relationship("ReviewPeriod", back_populates="goals")
    tasks = relationship("Task", back_populates="goal")
