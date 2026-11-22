from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    role = Column(String(30), nullable=False, index=True) # EMPLOYEE, MANAGER, HR, ADMIN
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    job_role_id = Column(String(36), ForeignKey("job_roles.id", ondelete="SET NULL"), nullable=True)
    manager_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    department = relationship("Department", back_populates="users")
    job_role = relationship("JobRole", back_populates="users")
    manager = relationship("User", remote_side=[id], backref="direct_reports")
    
    goals = relationship("Goal", foreign_keys="[Goal.employee_id]", back_populates="employee")
    assigned_tasks = relationship("Task", foreign_keys="[Task.employee_id]", back_populates="employee")
    performance_reviews = relationship("PerformanceReview", foreign_keys="[PerformanceReview.employee_id]", back_populates="employee")
    feedbacks_received = relationship("Feedback", foreign_keys="[Feedback.employee_id]", back_populates="employee")
    development_plans = relationship("DevelopmentPlan", foreign_keys="[DevelopmentPlan.employee_id]", back_populates="employee")
