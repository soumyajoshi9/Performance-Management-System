from sqlalchemy import Column, String, Text, Boolean, Integer, Numeric, DateTime, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.base import Base

class PerformanceReview(Base):
    __tablename__ = "performance_reviews"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    reviewer_id = Column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    review_period_id = Column(String(36), ForeignKey("review_periods.id", ondelete="RESTRICT"), nullable=False)
    
    status = Column(String(30), nullable=False, default="DRAFT", index=True) # DRAFT, SUBMITTED, FINALIZED
    score_status = Column(String(30), nullable=False, default="CALCULATED") # CALCULATED, INSUFFICIENT_DATA
    calculated_score = Column(Numeric(5, 2), nullable=True)
    final_score = Column(Numeric(5, 2), nullable=True)
    data_coverage_percentage = Column(Numeric(5, 2), nullable=False, default=0.00)
    
    manager_summary = Column(Text, nullable=True)
    employee_remarks = Column(Text, nullable=True)
    finalized_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("employee_id", "review_period_id", name="uq_performance_reviews_emp_period"),
    )

    employee = relationship("User", foreign_keys=[employee_id], back_populates="performance_reviews")
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    review_period = relationship("ReviewPeriod", back_populates="reviews")
    metric_snapshots = relationship("ReviewMetricSnapshot", back_populates="performance_review", cascade="all, delete-orphan")
    ai_insights = relationship("AIInsight", back_populates="performance_review")

class ReviewMetricSnapshot(Base):
    __tablename__ = "review_metric_snapshots"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    performance_review_id = Column(String(36), ForeignKey("performance_reviews.id", ondelete="CASCADE"), nullable=False, index=True)
    kpi_code = Column(String(50), nullable=False, index=True)
    kpi_name = Column(String(150), nullable=False)
    category = Column(String(30), nullable=False)
    raw_value = Column(Numeric(10, 2), nullable=True)
    normalized_score = Column(Numeric(5, 2), nullable=True)
    applied_weight = Column(Numeric(5, 2), nullable=False)
    evidence_count = Column(Integer, nullable=False)
    is_sufficient = Column(Boolean, nullable=False)
    data_status = Column(String(20), nullable=False) # AVAILABLE, NOT_AVAILABLE, INSUFFICIENT
    snapshot_data = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    performance_review = relationship("PerformanceReview", back_populates="metric_snapshots")
