from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.base import Base

class AIInsight(Base):
    __tablename__ = "ai_insights"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    performance_review_id = Column(String(36), ForeignKey("performance_reviews.id", ondelete="SET NULL"), nullable=True)
    review_period_id = Column(String(36), ForeignKey("review_periods.id", ondelete="RESTRICT"), nullable=False)
    
    prompt_version = Column(String(50), nullable=False)
    model_version = Column(String(50), nullable=False)
    structured_output = Column(JSON, nullable=False)
    status = Column(String(30), nullable=False, default="GENERATED") # GENERATED, FLAGGED, REVIEWED
    flag_reason = Column(Text, nullable=True)
    flagged_by_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    employee = relationship("User", foreign_keys=[employee_id])
    performance_review = relationship("PerformanceReview", back_populates="ai_insights")
    flagged_by = relationship("User", foreign_keys=[flagged_by_id])
