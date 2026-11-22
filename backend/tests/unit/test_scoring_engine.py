import pytest
from datetime import datetime, timezone, timedelta
from app.analytics.normalizer import bounded_linear_normalize
from app.analytics.coverage import audit_data_coverage
from app.analytics.workload import analyze_workload_context
from app.analytics.metrics import (
    calculate_task_completion_rate,
    calculate_goal_achievement_rate,
    calculate_deadline_adherence_rate
)

class MockTask:
    def __init__(self, status="COMPLETED", complexity="MEDIUM", due_date=None, completed_at=None, is_reopened=False, blocked_reason=None):
        now = datetime.now(timezone.utc)
        self.status = status
        self.complexity = complexity
        self.due_date = due_date or (now + timedelta(days=2))
        self.completed_at = completed_at or (now + timedelta(days=1))
        self.is_reopened = is_reopened
        self.blocked_reason = blocked_reason

class MockGoal:
    def __init__(self, start=0.0, target=100.0, current=80.0, status="ACTIVE"):
        self.start_value = start
        self.target_value = target
        self.current_value = current
        self.status = status

def test_bounded_linear_normalize_standard():
    assert bounded_linear_normalize(50.0, 0.0, 100.0) == 50.0
    assert bounded_linear_normalize(120.0, 0.0, 100.0) == 100.0
    assert bounded_linear_normalize(-10.0, 0.0, 100.0) == 0.0
    assert bounded_linear_normalize(None) == 0.0

def test_bounded_linear_normalize_inverted():
    # Lower is better: min 0, max 20 defect rate
    assert bounded_linear_normalize(0.0, 20.0, 0.0) == 100.0
    assert bounded_linear_normalize(10.0, 20.0, 0.0) == 50.0
    assert bounded_linear_normalize(20.0, 20.0, 0.0) == 0.0

def test_coverage_audit_sufficient_data():
    metrics = [
        {"kpi_code": "KPI_A", "default_weight": 50.0, "min_evidence_threshold": 3, "evidence_count": 5, "raw_value": 90.0},
        {"kpi_code": "KPI_B", "default_weight": 50.0, "min_evidence_threshold": 3, "evidence_count": 4, "raw_value": 80.0},
    ]
    cov, is_suff, audited = audit_data_coverage(metrics)
    assert cov == 100.0
    assert is_suff is True
    assert audited[0]["applied_weight"] == 50.0
    assert audited[1]["applied_weight"] == 50.0

def test_coverage_audit_partial_weight_redistribution():
    # KPI_B has insufficient evidence (count 1 < threshold 3)
    metrics = [
        {"kpi_code": "KPI_A", "default_weight": 60.0, "min_evidence_threshold": 3, "evidence_count": 5, "raw_value": 90.0},
        {"kpi_code": "KPI_B", "default_weight": 40.0, "min_evidence_threshold": 3, "evidence_count": 1, "raw_value": 80.0},
    ]
    cov, is_suff, audited = audit_data_coverage(metrics)
    assert cov == 60.0  # >= 50% threshold
    assert is_suff is True
    assert audited[0]["data_status"] == "AVAILABLE"
    assert audited[0]["applied_weight"] == 100.0 # Redistributed to 100%
    assert audited[1]["data_status"] == "NOT_AVAILABLE"
    assert audited[1]["applied_weight"] == 0.0

def test_coverage_audit_insufficient_data():
    # Coverage below 50%
    metrics = [
        {"kpi_code": "KPI_A", "default_weight": 30.0, "min_evidence_threshold": 5, "evidence_count": 6, "raw_value": 90.0},
        {"kpi_code": "KPI_B", "default_weight": 70.0, "min_evidence_threshold": 5, "evidence_count": 2, "raw_value": 80.0},
    ]
    cov, is_suff, audited = audit_data_coverage(metrics)
    assert cov == 30.0
    assert is_suff is False

def test_workload_context_analysis():
    now = datetime.now(timezone.utc)
    tasks = [
        MockTask(status="IN_PROGRESS", complexity="HIGH"),
        MockTask(status="IN_PROGRESS", complexity="HIGH"),
        MockTask(status="IN_PROGRESS", complexity="HIGH"),
        MockTask(status="BLOCKED", complexity="MEDIUM", blocked_reason="Waiting on API"),
    ]
    ctx = analyze_workload_context(tasks)
    assert ctx["active_tasks_count"] == 4
    assert ctx["high_complexity_count"] == 3
    assert ctx["blocked_tasks_count"] == 1
    assert ctx["workload_status"] in ("NORMAL", "HIGH_WORKLOAD", "OVERLOADED")

def test_metric_calculations():
    now = datetime.now(timezone.utc)
    tasks = [
        MockTask(status="COMPLETED", due_date=now + timedelta(days=2), completed_at=now + timedelta(days=1)),
        MockTask(status="COMPLETED", due_date=now - timedelta(days=1), completed_at=now - timedelta(days=2)),
        MockTask(status="IN_PROGRESS", due_date=now + timedelta(days=3)),
    ]
    comp_rate, count = calculate_task_completion_rate(tasks)
    assert comp_rate == round((2 / 3) * 100, 2)
    assert count == 3

    on_time, count_ot = calculate_deadline_adherence_rate(tasks)
    assert on_time == 100.0
    assert count_ot == 2

    goals = [
        MockGoal(start=0, target=100, current=80),
        MockGoal(start=50, target=100, current=75),
    ]
    goal_rate, count_g = calculate_goal_achievement_rate(goals)
    # Goal 1: 80%, Goal 2: 50% -> avg 65%
    assert goal_rate == 65.0
    assert count_g == 2
