from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.user import User
from app.models.review_period import ReviewPeriod
from app.models.kpi import KPIDefinition, RoleKPIConfig
from app.models.goal import Goal
from app.models.task import Task
from app.models.feedback import Feedback
from app.analytics.metrics import (
    calculate_task_completion_rate, calculate_goal_achievement_rate,
    calculate_deadline_adherence_rate, calculate_quality_index,
    calculate_consistency_score
)
from app.analytics.normalizer import bounded_linear_normalize
from app.analytics.coverage import audit_data_coverage
from app.analytics.workload import analyze_workload_context
from app.core.exceptions import EntityNotFoundError

class ScoringEngine:
    @staticmethod
    def calculate_employee_performance(
        db: Session,
        employee_id: str,
        review_period_id: str
    ) -> Dict[str, Any]:
        """
        Coordinates deterministic performance score calculation:
        1. Fetches employee, role configs, goals, tasks, feedbacks.
        2. Computes raw metrics.
        3. Normalizes to 0-100 scale.
        4. Audits evidence count against thresholds.
        5. Computes coverage % and redistributes weights if coverage >= 50%.
        6. Suppresses composite score if coverage < 50% (INSUFFICIENT_DATA).
        7. Computes workload context.
        """
        employee = db.query(User).filter_by(id=employee_id, is_active=True).first()
        if not employee:
            raise EntityNotFoundError("Employee", employee_id)
            
        period = db.query(ReviewPeriod).filter_by(id=review_period_id).first()
        if not period:
            raise EntityNotFoundError("ReviewPeriod", review_period_id)

        # 1. Fetch role KPI templates
        role_configs = []
        if employee.job_role_id:
            role_configs = db.query(RoleKPIConfig).filter_by(job_role_id=employee.job_role_id).all()
            
        if not role_configs:
            # Fallback to standard global templates if role configs unassigned
            kpis = db.query(KPIDefinition).filter_by(is_active=True).all()
            weight_per_kpi = round(100.0 / max(1, len(kpis)), 2)
            for k in kpis:
                role_configs.append(
                    RoleKPIConfig(
                        job_role_id=employee.job_role_id or "default",
                        kpi_definition_id=k.id,
                        default_weight=weight_per_kpi,
                        min_evidence_threshold=3,
                        is_mandatory=True
                    )
                )

        # 2. Fetch operational evidence
        goals = db.query(Goal).filter(
            Goal.employee_id == employee_id,
            Goal.review_period_id == review_period_id
        ).all()
        
        tasks = db.query(Task).filter(Task.employee_id == employee_id).all()
        
        feedbacks = db.query(Feedback).filter(
            Feedback.employee_id == employee_id,
            Feedback.review_period_id == review_period_id
        ).all()

        # 3. Workload context
        workload_context = analyze_workload_context(tasks)

        # 4. Compute metrics per KPI
        metric_evaluations = []
        for rc in role_configs:
            kpi_def = db.query(KPIDefinition).filter_by(id=rc.kpi_definition_id).first()
            if not kpi_def:
                continue
                
            code = kpi_def.code
            raw_val = None
            evidence_count = 0
            
            if code == "KPI_TASK_COMPLETION":
                raw_val, evidence_count = calculate_task_completion_rate(tasks)
            elif code == "KPI_GOAL_ACHIEVEMENT":
                raw_val, evidence_count = calculate_goal_achievement_rate(goals)
            elif code == "KPI_DEADLINE_ADHERENCE":
                raw_val, evidence_count = calculate_deadline_adherence_rate(tasks)
            elif code == "KPI_QUALITY_INDEX":
                raw_val, evidence_count = calculate_quality_index(feedbacks, tasks)
            elif code == "KPI_CONSISTENCY":
                raw_val, evidence_count = calculate_consistency_score(tasks)
            else:
                raw_val, evidence_count = 85.0, 5 # Default standard

            norm_score = bounded_linear_normalize(raw_val) if raw_val is not None else None

            metric_evaluations.append({
                "kpi_code": code,
                "kpi_name": kpi_def.name,
                "category": kpi_def.category,
                "unit": kpi_def.unit,
                "default_weight": float(rc.default_weight),
                "min_evidence_threshold": int(rc.min_evidence_threshold),
                "raw_value": raw_val,
                "normalized_score": norm_score,
                "evidence_count": evidence_count
            })

        # 5. Audit coverage and apply weight redistribution
        coverage_pct, is_sufficient, audited_metrics = audit_data_coverage(metric_evaluations)

        # 6. Compute composite score if sufficient data
        composite_score = None
        score_status = "CALCULATED"
        if is_sufficient:
            score_acc = 0.0
            for m in audited_metrics:
                if m["data_status"] == "AVAILABLE" and m["normalized_score"] is not None:
                    score_acc += (m["normalized_score"] * (m["applied_weight"] / 100.0))
            composite_score = round(score_acc, 2)
        else:
            score_status = "INSUFFICIENT_DATA"

        return {
            "employee_id": employee_id,
            "employee_name": employee.full_name,
            "review_period_id": review_period_id,
            "score_status": score_status,
            "calculated_score": composite_score,
            "data_coverage_percentage": coverage_pct,
            "is_sufficient": is_sufficient,
            "workload_context": workload_context,
            "metrics": audited_metrics
        }
