import logging
from datetime import datetime, date, timezone, timedelta
from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.models import (
    Department, JobRole, User, ReviewPeriod, KPIDefinition, 
    RoleKPIConfig, Goal, Task, Feedback, PerformanceReview, 
    DevelopmentPlan, AuditLog
)
from app.core.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_db")

def init_db(target_engine=None, target_session_factory=None):
    use_engine = target_engine or engine
    use_session_factory = target_session_factory or SessionLocal
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=use_engine)
    logger.info("Database tables verified.")

    db = use_session_factory()
    try:
        # 1. Departments
        eng_dept = db.query(Department).filter_by(code="ENG").first()
        if not eng_dept:
            eng_dept = Department(
                name="Engineering",
                code="ENG",
                description="Software engineering, infrastructure and QA"
            )
            sales_dept = Department(
                name="Sales & Growth",
                code="SALES",
                description="Enterprise client acquisition and revenue operations"
            )
            hr_dept = Department(
                name="People Operations",
                code="HR",
                description="Human resources, talent development, and culture"
            )
            db.add_all([eng_dept, sales_dept, hr_dept])
            db.commit()
            db.refresh(eng_dept)
            db.refresh(sales_dept)
            db.refresh(hr_dept)
            logger.info("Created default departments.")
        else:
            sales_dept = db.query(Department).filter_by(code="SALES").first()
            hr_dept = db.query(Department).filter_by(code="HR").first()

        # 2. Job Roles
        sr_dev_role = db.query(JobRole).filter_by(code="SWE_SR_BACKEND").first()
        if not sr_dev_role:
            sr_dev_role = JobRole(
                department_id=eng_dept.id,
                name="Senior Backend Engineer",
                code="SWE_SR_BACKEND",
                description="Distributed architecture and core backend services"
            )
            qa_role = JobRole(
                department_id=eng_dept.id,
                name="QA Automation Engineer",
                code="SWE_QA",
                description="Test automation and reliability engineering"
            )
            hr_role = JobRole(
                department_id=hr_dept.id,
                name="HR People Specialist",
                code="HR_SPEC",
                description="People operations and talent growth"
            )
            db.add_all([sr_dev_role, qa_role, hr_role])
            db.commit()
            db.refresh(sr_dev_role)
            logger.info("Created default job roles.")

        # 3. KPI Definitions
        kpis = {
            "KPI_TASK_COMPLETION": ("Task Completion Rate", "TASK", "Proportion of scheduled tasks completed in period", "percentage"),
            "KPI_GOAL_ACHIEVEMENT": ("Goal Achievement Rate", "GOAL", "Average milestone progress on active goals", "percentage"),
            "KPI_DEADLINE_ADHERENCE": ("On-Time Delivery Rate", "DEADLINE", "Completed on or before due date with blocker grace period", "percentage"),
            "KPI_QUALITY_INDEX": ("Output Quality Index", "QUALITY", "Role-appropriate quality, code review or defect metric", "score"),
            "KPI_CONSISTENCY": ("Operational Consistency", "CONSISTENCY", "Stability of task completion cadence across the cycle", "score")
        }
        kpi_objs = {}
        for code, (name, cat, desc, unit) in kpis.items():
            kpi = db.query(KPIDefinition).filter_by(code=code).first()
            if not kpi:
                kpi = KPIDefinition(code=code, name=name, category=cat, description=desc, unit=unit)
                db.add(kpi)
                db.commit()
                db.refresh(kpi)
            kpi_objs[code] = kpi
        logger.info("Created KPI definitions.")

        # 4. Role KPI Configs for Senior Backend Engineer
        role_configs = [
            (sr_dev_role.id, kpi_objs["KPI_GOAL_ACHIEVEMENT"].id, 30.00, 1),
            (sr_dev_role.id, kpi_objs["KPI_TASK_COMPLETION"].id, 25.00, 5),
            (sr_dev_role.id, kpi_objs["KPI_DEADLINE_ADHERENCE"].id, 20.00, 5),
            (sr_dev_role.id, kpi_objs["KPI_QUALITY_INDEX"].id, 15.00, 3),
            (sr_dev_role.id, kpi_objs["KPI_CONSISTENCY"].id, 10.00, 8),
        ]
        for role_id, kpi_id, weight, threshold in role_configs:
            cfg = db.query(RoleKPIConfig).filter_by(job_role_id=role_id, kpi_definition_id=kpi_id).first()
            if not cfg:
                cfg = RoleKPIConfig(
                    job_role_id=role_id,
                    kpi_definition_id=kpi_id,
                    default_weight=weight,
                    min_evidence_threshold=threshold,
                    is_mandatory=True
                )
                db.add(cfg)
        db.commit()
        logger.info("Created role-specific KPI templates.")

        # 5. Default Review Period
        current_period = db.query(ReviewPeriod).filter_by(review_month="2026-11").first()
        if not current_period:
            current_period = ReviewPeriod(
                name="November 2026 Review Period",
                start_date=date(2026, 11, 1),
                end_date=date(2026, 11, 30),
                review_month="2026-11",
                status="ACTIVE"
            )
            db.add(current_period)
            db.commit()
            db.refresh(current_period)
            logger.info("Created active review period.")

        # 6. Default Demo Users for all 4 Roles
        admin_user = db.query(User).filter_by(email="admin@vyora.local").first()
        if not admin_user:
            admin_user = User(
                email="admin@vyora.local",
                password_hash=hash_password("AdminPass123!"),
                full_name="System Administrator",
                role="ADMIN",
                is_active=True
            )
            hr_user = User(
                email="hr@vyora.local",
                password_hash=hash_password("HrPass123!"),
                full_name="Elena Vance",
                role="HR",
                department_id=hr_dept.id,
                is_active=True
            )
            manager_user = User(
                email="manager@vyora.local",
                password_hash=hash_password("ManagerPass123!"),
                full_name="David Miller",
                role="MANAGER",
                department_id=eng_dept.id,
                is_active=True
            )
            db.add_all([admin_user, hr_user, manager_user])
            db.commit()
            db.refresh(manager_user)

            # Employee reporting to Manager
            employee_user = User(
                email="employee@vyora.local",
                password_hash=hash_password("EmployeePass123!"),
                full_name="Sarah Chen",
                role="EMPLOYEE",
                department_id=eng_dept.id,
                job_role_id=sr_dev_role.id,
                manager_id=manager_user.id,
                is_active=True
            )
            db.add(employee_user)
            db.commit()
            db.refresh(employee_user)
            logger.info("Created all 4 demo users with passwords: AdminPass123!, HrPass123!, ManagerPass123!, EmployeePass123!")

            # 7. Seed Sample Goals & Tasks for Sarah Chen
            g1 = Goal(
                employee_id=employee_user.id,
                created_by_id=manager_user.id,
                review_period_id=current_period.id,
                title="Migrate Core Auth to Stateless JWT & Argon2",
                description="Improve security posture and reduce token latency",
                target_metric="Security Audit Score",
                start_value=60.00,
                target_value=100.00,
                current_value=90.00,
                unit="percent",
                status="ACTIVE",
                approval_status="APPROVED",
                due_date=date(2026, 11, 28)
            )
            g2 = Goal(
                employee_id=employee_user.id,
                created_by_id=employee_user.id,
                review_period_id=current_period.id,
                title="Refactor Deterministic Scoring Engine for Sub-50ms Latency",
                description="Vectorize metric computations in pure Python",
                target_metric="Latency p95",
                start_value=0.00,
                target_value=100.00,
                current_value=80.00,
                unit="percent",
                status="ACTIVE",
                approval_status="APPROVED",
                due_date=date(2026, 11, 30)
            )
            db.add_all([g1, g2])
            db.commit()
            db.refresh(g1)
            db.refresh(g2)

            now = datetime.now(timezone.utc)
            tasks = [
                Task(
                    employee_id=employee_user.id,
                    assigned_by_id=manager_user.id,
                    goal_id=g1.id,
                    title="Implement Argon2 password hashing utility",
                    status="COMPLETED",
                    priority="HIGH",
                    complexity="MEDIUM",
                    due_date=now - timedelta(days=10),
                    completed_at=now - timedelta(days=11)
                ),
                Task(
                    employee_id=employee_user.id,
                    assigned_by_id=manager_user.id,
                    goal_id=g1.id,
                    title="Setup JWT access and refresh token rotation",
                    status="COMPLETED",
                    priority="HIGH",
                    complexity="HIGH",
                    due_date=now - timedelta(days=5),
                    completed_at=now - timedelta(days=5)
                ),
                Task(
                    employee_id=employee_user.id,
                    assigned_by_id=employee_user.id,
                    goal_id=g2.id,
                    title="Benchmark bounded linear normalization algorithms",
                    status="COMPLETED",
                    priority="MEDIUM",
                    complexity="MEDIUM",
                    due_date=now - timedelta(days=2),
                    completed_at=now - timedelta(days=2)
                ),
                Task(
                    employee_id=employee_user.id,
                    assigned_by_id=employee_user.id,
                    goal_id=g2.id,
                    title="Implement data coverage and insufficient evidence check",
                    status="COMPLETED",
                    priority="MEDIUM",
                    complexity="MEDIUM",
                    due_date=now + timedelta(days=3),
                    completed_at=now - timedelta(days=1)
                ),
                Task(
                    employee_id=employee_user.id,
                    assigned_by_id=manager_user.id,
                    goal_id=g1.id,
                    title="Audit RBAC dependencies across all v1 API routers",
                    status="COMPLETED",
                    priority="URGENT",
                    complexity="HIGH",
                    due_date=now + timedelta(days=1),
                    completed_at=now
                ),
                Task(
                    employee_id=employee_user.id,
                    assigned_by_id=employee_user.id,
                    title="Draft OpenAPI contracts and Swagger documentation",
                    status="IN_PROGRESS",
                    priority="MEDIUM",
                    complexity="LOW",
                    due_date=now + timedelta(days=5)
                )
            ]
            db.add_all(tasks)

            # Sample Feedback
            fb = Feedback(
                employee_id=employee_user.id,
                author_id=manager_user.id,
                review_period_id=current_period.id,
                feedback_type="MANAGER_TO_EMPLOYEE",
                content="Sarah has demonstrated stellar technical leadership during the security migration sprint.",
                strengths="High attention to detail, proactive blocker resolution, and strong peer mentorship.",
                growth_areas="Continue documenting API error contracts for team juniors."
            )
            self_fb = Feedback(
                employee_id=employee_user.id,
                author_id=employee_user.id,
                review_period_id=current_period.id,
                feedback_type="SELF_ASSESSMENT",
                content="Successfully migrated core security without any downtime. Focused on clean architecture.",
                strengths="Delivered both high-priority security goals ahead of schedule.",
                growth_areas="Need to dedicate more time to automated integration test coverage."
            )
            db.add_all([fb, self_fb])
            db.commit()
            logger.info("Seeded initial goals, tasks, and feedback for demo employee.")

    finally:
        db.close()

if __name__ == "__main__":
    init_db()
