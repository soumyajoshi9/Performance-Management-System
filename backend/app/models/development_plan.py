from sqlalchemy import Column, String, Text, Boolean, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.base import Base

class DevelopmentPlan(Base):
    __tablename__ = "development_plans"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    manager_id = Column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    review_period_id = Column(String(36), ForeignKey("review_periods.id", ondelete="SET NULL"), nullable=True)
    ai_insight_id = Column(String(36), ForeignKey("ai_insights.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String(255), nullable=False)
    objective = Column(Text, nullable=False)
    status = Column(String(30), nullable=False, default="DRAFT", index=True) # DRAFT, PROPOSED, IN_PROGRESS, COMPLETED, REJECTED
    employee_agreed = Column(Boolean, nullable=False, default=False)
    manager_agreed = Column(Boolean, nullable=False, default=False)
    action_items = Column(JSON, nullable=False, default=list) # List of milestones
    
    start_date = Column(Date, nullable=False)
    target_completion_date = Column(Date, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    employee = relationship("User", foreign_keys=[employee_id], back_populates="development_plans")
    manager = relationship("User", foreign_keys=[manager_id])
    review_period = relationship("ReviewPeriod")
    ai_insight = relationship("AIInsight")
