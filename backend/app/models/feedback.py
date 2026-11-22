from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.base import Base

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    review_period_id = Column(String(36), ForeignKey("review_periods.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    feedback_type = Column(String(30), nullable=False) # MANAGER_TO_EMPLOYEE, SELF_ASSESSMENT
    content = Column(Text, nullable=False)
    strengths = Column(Text, nullable=True)
    growth_areas = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    employee = relationship("User", foreign_keys=[employee_id], back_populates="feedbacks_received")
    author = relationship("User", foreign_keys=[author_id])
    review_period = relationship("ReviewPeriod", back_populates="feedbacks")
