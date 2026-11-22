from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.base import Base

class ReviewPeriod(Base):
    __tablename__ = "review_periods"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    review_month = Column(String(7), nullable=False, unique=True) # e.g. '2026-11'
    status = Column(String(30), nullable=False, default="UPCOMING", index=True) # UPCOMING, ACTIVE, UNDER_REVIEW, COMPLETED, ARCHIVED
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    goals = relationship("Goal", back_populates="review_period")
    reviews = relationship("PerformanceReview", back_populates="review_period")
    feedbacks = relationship("Feedback", back_populates="review_period")
