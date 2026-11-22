from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.goal import Goal
from app.models.user import User
from app.models.review_period import ReviewPeriod
from app.schemas.goal import GoalCreate, GoalUpdateProgress, GoalApprovalAction, GoalRead
from app.core.exceptions import EntityNotFoundError, AuthorizationError, ValidationError

class GoalService:
    @staticmethod
    def calculate_progress(start: float, target: float, current: float) -> float:
        if target <= start:
            return 100.0 if current >= target else 0.0
        pct = ((current - start) / (target - start)) * 100.0
        return round(min(100.0, max(0.0, pct)), 2)

    @staticmethod
    def enrich_goal(goal: Goal) -> GoalRead:
        dto = GoalRead.model_validate(goal)
        dto.progress_percentage = GoalService.calculate_progress(
            float(goal.start_value),
            float(goal.target_value),
            float(goal.current_value)
        )
        return dto

    @staticmethod
    def create_goal(db: Session, data: GoalCreate, creator: User) -> GoalRead:
        target_employee_id = data.employee_id or creator.id
        
        # Verify review period
        period = db.query(ReviewPeriod).filter_by(id=data.review_period_id).first()
        if not period:
            raise EntityNotFoundError("ReviewPeriod", data.review_period_id)
            
        # Target employee
        emp = db.query(User).filter_by(id=target_employee_id, is_active=True).first()
        if not emp:
            raise EntityNotFoundError("Employee", target_employee_id)
            
        # Authorization check:
        if creator.role == "EMPLOYEE" and target_employee_id != creator.id:
            raise AuthorizationError("Employees can only propose personal goals.")
        if creator.role == "MANAGER" and emp.manager_id != creator.id and emp.id != creator.id and creator.role != "ADMIN":
            raise AuthorizationError("Managers can only assign goals to their direct reports.")
            
        # Approval logic (DB-3):
        is_self_proposed = (creator.id == target_employee_id and creator.role == "EMPLOYEE")
        status = "PENDING_APPROVAL" if is_self_proposed else "ACTIVE"
        approval_status = "PENDING" if is_self_proposed else "APPROVED"
        approved_by = None if is_self_proposed else creator.id
        
        goal = Goal(
            employee_id=target_employee_id,
            created_by_id=creator.id,
            review_period_id=data.review_period_id,
            title=data.title,
            description=data.description,
            category=data.category,
            target_metric=data.target_metric,
            start_value=data.start_value,
            target_value=data.target_value,
            current_value=data.start_value,
            unit=data.unit,
            status=status,
            approval_status=approval_status,
            approved_by_id=approved_by,
            due_date=data.due_date
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        return GoalService.enrich_goal(goal)

    @staticmethod
    def get_goals(
        db: Session,
        current_user: User,
        employee_id: Optional[str] = None,
        review_period_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[GoalRead]:
        query = db.query(Goal)
        
        if current_user.role == "EMPLOYEE":
            query = query.filter(Goal.employee_id == current_user.id)
        elif current_user.role == "MANAGER":
            if employee_id:
                query = query.filter(Goal.employee_id == employee_id)
            else:
                # Direct reports plus own goals
                report_ids = [u.id for u in db.query(User.id).filter(User.manager_id == current_user.id).all()]
                report_ids.append(current_user.id)
                query = query.filter(Goal.employee_id.in_(report_ids))
        else:
            if employee_id:
                query = query.filter(Goal.employee_id == employee_id)
                
        if review_period_id:
            query = query.filter(Goal.review_period_id == review_period_id)
        if status:
            query = query.filter(Goal.status == status)
            
        goals = query.order_by(Goal.due_date.asc()).all()
        return [GoalService.enrich_goal(g) for g in goals]

    @staticmethod
    def update_progress(db: Session, goal_id: str, data: GoalUpdateProgress, current_user: User) -> GoalRead:
        goal = db.query(Goal).filter_by(id=goal_id).first()
        if not goal:
            raise EntityNotFoundError("Goal", goal_id)
            
        # Auth check
        if current_user.role == "EMPLOYEE" and goal.employee_id != current_user.id:
            raise AuthorizationError("Cannot update other employees' goals.")
            
        goal.current_value = data.current_value
        if goal.current_value >= goal.target_value and goal.status == "ACTIVE":
            goal.status = "COMPLETED"
            
        db.commit()
        db.refresh(goal)
        return GoalService.enrich_goal(goal)

    @staticmethod
    def process_approval(db: Session, goal_id: str, action: GoalApprovalAction, manager: User) -> GoalRead:
        goal = db.query(Goal).filter_by(id=goal_id).first()
        if not goal:
            raise EntityNotFoundError("Goal", goal_id)
            
        emp = db.query(User).filter_by(id=goal.employee_id).first()
        if manager.role not in ("MANAGER", "HR", "ADMIN") or (manager.role == "MANAGER" and emp.manager_id != manager.id):
            raise AuthorizationError("Only the assigned manager or HR can approve this goal.")
            
        if action.action == "APPROVE":
            goal.approval_status = "APPROVED"
            goal.status = "ACTIVE"
            goal.approved_by_id = manager.id
            goal.rejection_reason = None
        else:
            if not action.rejection_reason:
                raise ValidationError("Rejection reason is required when rejecting a proposed goal.")
            goal.approval_status = "REJECTED"
            goal.status = "CANCELLED"
            goal.rejection_reason = action.rejection_reason
            
        db.commit()
        db.refresh(goal)
        return GoalService.enrich_goal(goal)
