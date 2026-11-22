from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.goal import Goal
from app.models.user import User
from app.schemas.task import TaskCreate, TaskStatusUpdate, TaskRead
from app.core.exceptions import EntityNotFoundError, AuthorizationError, ValidationError

class TaskService:
    @staticmethod
    def create_task(db: Session, data: TaskCreate, creator: User) -> Task:
        target_employee_id = data.employee_id or creator.id
        
        emp = db.query(User).filter_by(id=target_employee_id, is_active=True).first()
        if not emp:
            raise EntityNotFoundError("Employee", target_employee_id)
            
        # Role boundary
        if creator.role == "EMPLOYEE" and target_employee_id != creator.id:
            raise AuthorizationError("Employees can only create self-assigned tasks.")
        if creator.role == "MANAGER" and emp.manager_id != creator.id and emp.id != creator.id and creator.role != "ADMIN":
            raise AuthorizationError("Managers can only assign tasks to their direct reports.")
            
        # Verify goal if provided
        if data.goal_id:
            goal = db.query(Goal).filter_by(id=data.goal_id).first()
            if not goal:
                raise EntityNotFoundError("Goal", data.goal_id)
            if goal.employee_id != target_employee_id:
                raise ValidationError("Linked goal does not belong to the target employee.")

        task = Task(
            employee_id=target_employee_id,
            assigned_by_id=creator.id,
            goal_id=data.goal_id,
            title=data.title,
            description=data.description,
            priority=data.priority or "MEDIUM",
            complexity=data.complexity or "MEDIUM",
            due_date=data.due_date,
            status="TODO"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_tasks(
        db: Session,
        current_user: User,
        employee_id: Optional[str] = None,
        goal_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Task]:
        query = db.query(Task)
        
        if current_user.role == "EMPLOYEE":
            query = query.filter(Task.employee_id == current_user.id)
        elif current_user.role == "MANAGER":
            if employee_id:
                query = query.filter(Task.employee_id == employee_id)
            else:
                report_ids = [u.id for u in db.query(User.id).filter(User.manager_id == current_user.id).all()]
                report_ids.append(current_user.id)
                query = query.filter(Task.employee_id.in_(report_ids))
        else:
            if employee_id:
                query = query.filter(Task.employee_id == employee_id)
                
        if goal_id:
            query = query.filter(Task.goal_id == goal_id)
        if status:
            query = query.filter(Task.status == status)
            
        return query.order_by(Task.due_date.asc()).all()

    @staticmethod
    def update_status(db: Session, task_id: str, data: TaskStatusUpdate, current_user: User) -> Task:
        task = db.query(Task).filter_by(id=task_id).first()
        if not task:
            raise EntityNotFoundError("Task", task_id)
            
        # Auth check
        if current_user.role == "EMPLOYEE" and task.employee_id != current_user.id:
            raise AuthorizationError("Cannot update other employees' tasks.")
            
        # Blocker validation (FR-018)
        if data.status == "BLOCKED" and not data.blocked_reason:
            raise ValidationError("A mandatory explanation is required whenever a task is marked BLOCKED.")
            
        now = datetime.now(timezone.utc)
        
        # Reopening tracking (FR-020)
        if task.status == "COMPLETED" and data.status in ("TODO", "IN_PROGRESS"):
            task.is_reopened = True
            
        # Completion timestamp (FR-019)
        if data.status == "COMPLETED":
            task.completed_at = now
            task.blocked_reason = None
        elif data.status != "COMPLETED":
            task.completed_at = None

        if data.status == "BLOCKED":
            task.blocked_reason = data.blocked_reason
        elif data.status != "BLOCKED":
            task.blocked_reason = None

        task.status = data.status
        db.commit()
        db.refresh(task)
        return task
