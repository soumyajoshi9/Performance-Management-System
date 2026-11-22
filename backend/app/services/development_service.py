from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.development_plan import DevelopmentPlan
from app.models.user import User
from app.schemas.development_plan import (
    DevelopmentPlanCreate, DevelopmentPlanAgreementRequest, 
    ActionItemToggleRequest, DevelopmentPlanRead
)
from app.core.exceptions import EntityNotFoundError, AuthorizationError, ValidationError

class DevelopmentService:
    @staticmethod
    def create_plan(db: Session, data: DevelopmentPlanCreate, manager: User) -> DevelopmentPlan:
        emp = db.query(User).filter_by(id=data.employee_id, is_active=True).first()
        if not emp:
            raise EntityNotFoundError("Employee", data.employee_id)
            
        if manager.role == "MANAGER" and emp.manager_id != manager.id and manager.role != "ADMIN":
            raise AuthorizationError("Managers can only propose development plans for direct reports.")

        plan = DevelopmentPlan(
            employee_id=data.employee_id,
            manager_id=manager.id,
            review_period_id=data.review_period_id,
            ai_insight_id=data.ai_insight_id,
            title=data.title,
            objective=data.objective,
            status="PROPOSED",
            manager_agreed=True,
            employee_agreed=False,
            action_items=[item.model_dump(mode="json") for item in data.action_items],
            start_date=data.start_date,
            target_completion_date=data.target_completion_date
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def record_agreement(db: Session, plan_id: str, data: DevelopmentPlanAgreementRequest, current_user: User) -> DevelopmentPlan:
        """
        Bilateral digital agreement logic (BR-010):
        Plan becomes active ('IN_PROGRESS') only when BOTH employee and manager agree.
        """
        plan = db.query(DevelopmentPlan).filter_by(id=plan_id).first()
        if not plan:
            raise EntityNotFoundError("DevelopmentPlan", plan_id)

        if current_user.id == plan.employee_id:
            plan.employee_agreed = data.agreed
        elif current_user.id == plan.manager_id or current_user.role == "ADMIN":
            plan.manager_agreed = data.agreed
        else:
            raise AuthorizationError("Only the participating employee or manager can record agreement.")

        if plan.employee_agreed and plan.manager_agreed:
            plan.status = "IN_PROGRESS"
        elif not data.agreed:
            plan.status = "REJECTED"

        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def toggle_action_item(db: Session, plan_id: str, item_id: str, data: ActionItemToggleRequest, current_user: User) -> DevelopmentPlan:
        plan = db.query(DevelopmentPlan).filter_by(id=plan_id).first()
        if not plan:
            raise EntityNotFoundError("DevelopmentPlan", plan_id)

        if current_user.id not in (plan.employee_id, plan.manager_id) and current_user.role != "ADMIN":
            raise AuthorizationError("Access denied.")

        items = list(plan.action_items or [])
        found = False
        all_completed = True
        
        for item in items:
            if item.get("id") == item_id:
                item["is_completed"] = data.is_completed
                found = True
            if not item.get("is_completed", False):
                all_completed = False

        if not found:
            raise EntityNotFoundError("ActionItem", item_id)

        from sqlalchemy.orm.attributes import flag_modified
        plan.action_items = [dict(it) for it in items]
        flag_modified(plan, "action_items")
        if all_completed and len(items) > 0 and plan.status == "IN_PROGRESS":
            plan.status = "COMPLETED"
            plan.completed_at = datetime.now(timezone.utc)
            
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def list_plans(db: Session, current_user: User, employee_id: Optional[str] = None) -> List[DevelopmentPlan]:
        query = db.query(DevelopmentPlan)
        if current_user.role == "EMPLOYEE":
            query = query.filter(DevelopmentPlan.employee_id == current_user.id)
        elif current_user.role == "MANAGER":
            if employee_id:
                query = query.filter(DevelopmentPlan.employee_id == employee_id)
            else:
                report_ids = [u.id for u in db.query(User.id).filter(User.manager_id == current_user.id).all()]
                report_ids.append(current_user.id)
                query = query.filter(DevelopmentPlan.employee_id.in_(report_ids))
        else:
            if employee_id:
                query = query.filter(DevelopmentPlan.employee_id == employee_id)
                
        return query.order_by(DevelopmentPlan.created_at.desc()).all()
