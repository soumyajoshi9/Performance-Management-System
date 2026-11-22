from typing import List, Dict, Any
from datetime import datetime, timezone

def analyze_workload_context(tasks: List[Any]) -> Dict[str, Any]:
    """
    Computes workload indicators and task complexity distribution.
    Workload indicators provide context to interpret performance without
    directly applying arbitrary bonuses or penalties to official scores (PS-4).
    """
    now = datetime.now(timezone.utc)
    
    active_tasks = [t for t in tasks if getattr(t, "status", "") in ("TODO", "IN_PROGRESS", "BLOCKED")]
    active_count = len(active_tasks)
    
    high_comp = sum(1 for t in active_tasks if getattr(t, "complexity", "") == "HIGH")
    med_comp = sum(1 for t in active_tasks if getattr(t, "complexity", "") == "MEDIUM")
    low_comp = sum(1 for t in active_tasks if getattr(t, "complexity", "") == "LOW")
    
    blocked_count = sum(1 for t in active_tasks if getattr(t, "status", "") == "BLOCKED")
    
    overdue_count = 0
    for t in active_tasks:
        due = getattr(t, "due_date", None)
        if due:
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
            if due < now:
                overdue_count += 1

    # Workload classification
    if active_count > 10 or (active_count >= 7 and high_comp >= 4) or blocked_count >= 3:
        status = "OVERLOADED"
        note = "Employee is managing an unusually heavy concurrent task load with multiple complex or blocked items."
    elif active_count >= 6 or high_comp >= 3:
        status = "HIGH_WORKLOAD"
        note = "Above-average task load with notable complexity; requires monitoring for bottlenecks."
    else:
        status = "NORMAL"
        note = "Task distribution is balanced within standard operational capacity."

    return {
        "active_tasks_count": active_count,
        "high_complexity_count": high_comp,
        "medium_complexity_count": med_comp,
        "low_complexity_count": low_comp,
        "overdue_tasks_count": overdue_count,
        "blocked_tasks_count": blocked_count,
        "workload_status": status,
        "context_notes": note
    }
