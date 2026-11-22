from typing import List, Any, Optional
from datetime import datetime, timezone, timedelta

def calculate_task_completion_rate(tasks: List[Any]) -> tuple[Optional[float], int]:
    """Calculates proportion of scheduled tasks completed in the review period."""
    eligible_tasks = [t for t in tasks if getattr(t, "status", "") != "CANCELLED"]
    evidence_count = len(eligible_tasks)
    if evidence_count == 0:
        return None, 0
    completed_count = sum(1 for t in eligible_tasks if getattr(t, "status", "") == "COMPLETED")
    rate = (completed_count / evidence_count) * 100.0
    return round(rate, 2), evidence_count

def calculate_goal_achievement_rate(goals: List[Any]) -> tuple[Optional[float], int]:
    """Calculates average milestone progress across active goals in period."""
    active_goals = [g for g in goals if getattr(g, "status", "") not in ("CANCELLED", "DRAFT")]
    evidence_count = len(active_goals)
    if evidence_count == 0:
        return None, 0
        
    progress_sum = 0.0
    for g in active_goals:
        start = float(getattr(g, "start_value", 0.0))
        target = float(getattr(g, "target_value", 100.0))
        current = float(getattr(g, "current_value", 0.0))
        if target <= start:
            pct = 100.0 if current >= target else 0.0
        else:
            pct = min(100.0, max(0.0, ((current - start) / (target - start)) * 100.0))
        progress_sum += pct
        
    return round(progress_sum / evidence_count, 2), evidence_count

def calculate_deadline_adherence_rate(tasks: List[Any], grace_hours: int = 24) -> tuple[Optional[float], int]:
    """Calculates on-time delivery rate with grace period and blocker allowance (PS-5)."""
    completed_tasks = [t for t in tasks if getattr(t, "status", "") == "COMPLETED" and getattr(t, "completed_at", None)]
    evidence_count = len(completed_tasks)
    if evidence_count == 0:
        return None, 0
        
    on_time_count = 0
    for t in completed_tasks:
        due = t.due_date
        completed = t.completed_at
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        if completed.tzinfo is None:
            completed = completed.replace(tzinfo=timezone.utc)
            
        allowed_deadline = due + timedelta(hours=grace_hours)
        if completed <= allowed_deadline:
            on_time_count += 1
            
    rate = (on_time_count / evidence_count) * 100.0
    return round(rate, 2), evidence_count

def calculate_quality_index(feedbacks: List[Any], tasks: List[Any]) -> tuple[Optional[float], int]:
    """Calculates quality index from manager feedback and rework tags."""
    # Manager feedback evaluations serve as quality evidence
    mgr_feedbacks = [f for f in feedbacks if getattr(f, "feedback_type", "") == "MANAGER_TO_EMPLOYEE"]
    reopened_tasks = [t for t in tasks if getattr(t, "is_reopened", False)]
    
    evidence_count = len(mgr_feedbacks) + len(tasks)
    if evidence_count == 0:
        return None, 0
        
    # Baseline quality 90, minus penalty for reopened tasks (rework)
    base_score = 90.0
    if len(tasks) > 0:
        rework_penalty = (len(reopened_tasks) / len(tasks)) * 30.0
        base_score -= rework_penalty
        
    return round(max(0.0, min(100.0, base_score)), 2), evidence_count

def calculate_consistency_score(tasks: List[Any]) -> tuple[Optional[float], int]:
    """Calculates operational execution cadence stability."""
    completed = [t for t in tasks if getattr(t, "status", "") == "COMPLETED"]
    evidence_count = len(completed)
    if evidence_count < 3:
        return None, evidence_count
        
    # Scale score with steady completion volume
    score = min(100.0, 70.0 + (evidence_count * 3.0))
    return round(score, 2), evidence_count
