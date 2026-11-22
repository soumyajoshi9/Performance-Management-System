import pytest
from app.models.user import User
from app.models.review_period import ReviewPeriod
from app.schemas.auth import LoginRequest
from app.schemas.goal import GoalCreate, GoalApprovalAction, GoalUpdateProgress
from app.schemas.task import TaskCreate, TaskStatusUpdate
from app.schemas.feedback import FeedbackCreate
from app.schemas.scoring import ScoringPreviewRequest
from app.schemas.review import ReviewDraftRequest, ReviewFinalizeRequest
from app.schemas.ai import AIInsightGenerateRequest
from app.schemas.development_plan import (
    DevelopmentPlanCreate, ActionItemSchema, 
    DevelopmentPlanAgreementRequest, ActionItemToggleRequest
)
from app.api.v1 import auth, goals, tasks, feedbacks, scoring, reviews, ai, development_plans
from datetime import datetime, timezone, date
from decimal import Decimal

def test_complete_end_to_end_evaluation_and_growth_cycle(db_session):
    db = db_session
    # 1. Authentication for Employee and Manager
    emp_login = auth.login(LoginRequest(email="employee@vyora.local", password="EmployeePass123!"), db)
    assert emp_login.user.email == "employee@vyora.local"
    assert emp_login.user.role == "EMPLOYEE"
    
    mgr_login = auth.login(LoginRequest(email="manager@vyora.local", password="ManagerPass123!"), db)
    assert mgr_login.user.role == "MANAGER"

    employee_user = db.query(User).filter_by(id=emp_login.user.id).first()
    manager_user = db.query(User).filter_by(id=mgr_login.user.id).first()
    active_period = db.query(ReviewPeriod).filter_by(status="ACTIVE").first()

    # 2. Goal Creation & Approval Workflow (DB-3)
    goal_dto = GoalCreate(
        title="Scalable Event Logging Pipeline",
        category="PROJECT",
        target_metric="P99 Latency Reduction",
        start_value=Decimal("0.0"),
        target_value=Decimal("100.0"),
        due_date=date(2026, 11, 30),
        review_period_id=active_period.id
    )
    proposed_goal = goals.create_goal(goal_dto, db, employee_user)
    assert proposed_goal.status == "PENDING_APPROVAL"
    assert proposed_goal.approval_status == "PENDING"

    # Manager approves goal
    approved_goal = goals.approve_or_reject_goal(
        proposed_goal.id,
        GoalApprovalAction(action="APPROVE"),
        db,
        manager_user
    )
    assert approved_goal.status == "ACTIVE"
    assert approved_goal.approval_status == "APPROVED"

    # Update progress
    prog_goal = goals.update_goal_progress(
        approved_goal.id,
        GoalUpdateProgress(current_value=Decimal("75.0")),
        db,
        employee_user
    )
    assert prog_goal.progress_percentage == 75.0

    # 3. Task Management (DB-4, PS-4)
    now = datetime.now(timezone.utc)
    task_dto = TaskCreate(
        title="Benchmarking event log persistence",
        employee_id=employee_user.id,
        priority="HIGH",
        complexity="HIGH",
        due_date=now,
        goal_id=approved_goal.id
    )
    created_task = tasks.create_task(task_dto, db, manager_user)
    assert created_task.status == "TODO"
    assert created_task.complexity == "HIGH"
    assert created_task.employee_id == employee_user.id

    # Complete task
    completed_task = tasks.update_task_status(
        created_task.id,
        TaskStatusUpdate(status="COMPLETED"),
        db,
        employee_user
    )
    assert completed_task.status == "COMPLETED"
    assert completed_task.completed_at is not None

    # 4. Qualitative Feedback Loop (DB-5)
    self_fb = feedbacks.create_feedback(
        FeedbackCreate(
            employee_id=employee_user.id,
            review_period_id=active_period.id,
            feedback_type="SELF_ASSESSMENT",
            content="Delivered high concurrency benchmarks ahead of schedule.",
            strengths="Architecture planning, test automation.",
            growth_areas="Public documentation."
        ),
        db,
        employee_user
    )
    assert self_fb.feedback_type == "SELF_ASSESSMENT"

    mgr_fb = feedbacks.create_feedback(
        FeedbackCreate(
            employee_id=employee_user.id,
            review_period_id=active_period.id,
            feedback_type="MANAGER_TO_EMPLOYEE",
            content="Outstanding execution on the streaming log subsystem.",
            strengths="Thoroughness and high code quality.",
            growth_areas="Lead cross-team architecture sharing."
        ),
        db,
        manager_user
    )
    assert mgr_fb.feedback_type == "MANAGER_TO_EMPLOYEE"

    # 5. Deterministic Scoring Engine Verification (PS-1, PS-2, PS-5)
    score_preview = scoring.preview_score(
        ScoringPreviewRequest(
            employee_id=employee_user.id,
            review_period_id=active_period.id
        ),
        db,
        manager_user
    )
    assert score_preview.score_status in ["CALCULATED", "INSUFFICIENT_DATA"]
    assert score_preview.data_coverage_percentage > 0.0
    assert len(score_preview.metrics) >= 3

    # 6. AI Insight Generation & Citation Verification (AI-1, AI-4)
    ai_insight = ai.generate_insight(
        AIInsightGenerateRequest(
            employee_id=employee_user.id,
            review_period_id=active_period.id
        ),
        db,
        manager_user
    )
    assert ai_insight.status == "GENERATED"
    assert len(ai_insight.structured_output["strengths"]) > 0
    assert len(ai_insight.structured_output["evidence_references"]) > 0

    # 7. Performance Review Finalization & Immutable Snapshot (DB-6, DB-7)
    draft = reviews.get_or_create_draft(
        ReviewDraftRequest(
            employee_id=employee_user.id,
            review_period_id=active_period.id
        ),
        db,
        manager_user
    )
    assert draft.status == "DRAFT"

    finalized = reviews.finalize_review(
        draft.id,
        ReviewFinalizeRequest(
            manager_summary="Superb engineering discipline and architecture quality."
        ),
        db,
        manager_user
    )
    assert finalized.status == "FINALIZED"
    assert finalized.final_score is not None
    assert finalized.finalized_at is not None

    # Verify frozen snapshots exist in DB
    review_with_snapshots = reviews.get_review(finalized.id, db, manager_user)
    assert len(review_with_snapshots.metric_snapshots) > 0
    snapshot_1 = review_with_snapshots.metric_snapshots[0]
    assert snapshot_1.applied_weight > 0
    assert snapshot_1.kpi_code is not None

    # 8. Collaborative Development Plan (AI-6, BR-010)
    dev_plan_dto = DevelopmentPlanCreate(
        employee_id=employee_user.id,
        review_period_id=active_period.id,
        title="Distributed Systems Engineering Mastery",
        objective="Advance from module ownership to multi-service orchestration.",
        start_date=date(2026, 12, 1),
        target_completion_date=date(2027, 1, 31),
        action_items=[
            ActionItemSchema(
                id="item-1",
                title="Complete distributed tracing specification",
                description="Distributed tracing specification across services",
                target_date=date(2026, 12, 15),
                is_completed=False
            ),
            ActionItemSchema(
                id="item-2",
                title="Lead deep-dive architecture presentation to senior staff",
                description="Lead deep-dive architecture presentation",
                target_date=date(2026, 12, 20),
                is_completed=False
            )
        ]
    )
    created_plan = development_plans.create_development_plan(dev_plan_dto, db, manager_user)
    assert created_plan.status == "PROPOSED"
    assert created_plan.manager_agreed is True
    assert created_plan.employee_agreed is False

    # Employee agrees to plan -> status transitions to IN_PROGRESS
    active_plan = development_plans.record_plan_agreement(
        created_plan.id,
        DevelopmentPlanAgreementRequest(agreed=True),
        db,
        employee_user
    )
    assert active_plan.status == "IN_PROGRESS"
    assert active_plan.employee_agreed is True

    # Toggle milestone
    updated_plan = development_plans.toggle_action_item(
        active_plan.id,
        "item-1",
        ActionItemToggleRequest(is_completed=True),
        db,
        employee_user
    )
    assert updated_plan.action_items[0].is_completed is True
