import pytest
from fastapi import HTTPException
from app.models.user import User
from app.models.review_period import ReviewPeriod
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalApprovalAction
from app.schemas.review import ReviewFinalizeRequest
from app.api.v1 import goals, reviews
from decimal import Decimal
from datetime import date

def test_rbac_unauthorized_goal_approval(db_session):
    """Verify that an Employee cannot approve their own or anyone else's goals."""
    employee = db_session.query(User).filter_by(email="employee@vyora.local").first()
    active_period = db_session.query(ReviewPeriod).filter_by(status="ACTIVE").first()

    # Employee creates goal
    goal = goals.create_goal(
        GoalCreate(
            title="RBAC Verification Goal",
            category="PROJECT",
            target_metric="Security Coverage",
            start_value=Decimal("0.0"),
            target_value=Decimal("100.0"),
            due_date=date(2026, 11, 30),
            review_period_id=active_period.id
        ),
        db_session,
        employee
    )
    assert goal.status == "PENDING_APPROVAL"

    # Employee attempts to approve their own goal -> raises 400/403
    with pytest.raises(HTTPException) as exc_info:
        goals.approve_or_reject_goal(
            goal.id,
            GoalApprovalAction(action="APPROVE"),
            db_session,
            employee
        )
    assert exc_info.value.status_code in [400, 403]
    assert "Only the assigned manager or HR can approve this goal" in exc_info.value.detail

def test_rbac_manager_subordinate_boundary(db_session):
    """Verify that a manager cannot approve a goal for an employee not under their supervision."""
    manager = db_session.query(User).filter_by(email="manager@vyora.local").first()
    active_period = db_session.query(ReviewPeriod).filter_by(status="ACTIVE").first()

    # Create an unassigned employee
    unrelated_emp = User(
        email="unrelated@vyora.local",
        password_hash="fakehash",
        full_name="Unrelated Worker",
        role="EMPLOYEE",
        manager_id=None
    )
    db_session.add(unrelated_emp)
    db_session.commit()

    unrelated_goal = Goal(
        employee_id=unrelated_emp.id,
        created_by_id=unrelated_emp.id,
        review_period_id=active_period.id,
        title="Unrelated Project Goal",
        category="PROJECT",
        target_metric="KPI",
        start_value=Decimal("0.0"),
        target_value=Decimal("100.0"),
        current_value=Decimal("0.0"),
        due_date=date(2026, 11, 30),
        status="PENDING_APPROVAL",
        approval_status="PENDING"
    )
    db_session.add(unrelated_goal)
    db_session.commit()

    # Manager attempts to approve goal of non-subordinate -> raises 400/403
    with pytest.raises(HTTPException) as exc_info:
        goals.approve_or_reject_goal(
            unrelated_goal.id,
            GoalApprovalAction(action="APPROVE"),
            db_session,
            manager
        )
    assert exc_info.value.status_code in [400, 403]
    assert "Only the assigned manager or HR can approve this goal" in exc_info.value.detail

def test_finalized_review_immutability(db_session):
    """Verify that once a performance review is finalized, it cannot be re-finalized."""
    manager = db_session.query(User).filter_by(email="manager@vyora.local").first()
    employee = db_session.query(User).filter_by(email="employee@vyora.local").first()
    active_period = db_session.query(ReviewPeriod).filter_by(status="ACTIVE").first()

    from app.schemas.review import ReviewDraftRequest
    draft = reviews.get_or_create_draft(
        ReviewDraftRequest(
            employee_id=employee.id,
            review_period_id=active_period.id
        ),
        db_session,
        manager
    )

    if draft.status == "DRAFT":
        finalized = reviews.finalize_review(
            draft.id,
            ReviewFinalizeRequest(manager_summary="Initial finalization."),
            db_session,
            manager
        )
    else:
        finalized = draft
    assert finalized.status == "FINALIZED"

    # Attempt to re-finalize an already finalized review -> raises 400 Bad Request
    with pytest.raises(HTTPException) as exc_info:
        reviews.finalize_review(
            finalized.id,
            ReviewFinalizeRequest(manager_summary="Attempted overwrite."),
            db_session,
            manager
        )
    assert exc_info.value.status_code == 400
    assert "already finalized" in exc_info.value.detail.lower()
