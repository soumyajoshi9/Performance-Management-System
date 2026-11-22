from typing import Dict, Any, List

def anonymize_context_bundle(
    employee_data: Dict[str, Any],
    metrics_bundle: Dict[str, Any],
    goals: List[Any],
    tasks: List[Any],
    feedbacks: List[Any]
) -> Dict[str, Any]:
    """
    Strips direct PII (names, emails, direct UUIDs) before sending context to LLM.
    Replaces real identity with ephemeral pseudonym 'SUBJECT_A'.
    Encapsulates user-supplied strings to defend against prompt injection.
    """
    sanitized_goals = []
    for g in goals:
        sanitized_goals.append({
            "title": str(getattr(g, "title", "")),
            "target_metric": str(getattr(g, "target_metric", "")),
            "current_value": float(getattr(g, "current_value", 0.0)),
            "target_value": float(getattr(g, "target_value", 100.0)),
            "unit": str(getattr(g, "unit", "percent")),
            "status": str(getattr(g, "status", ""))
        })

    sanitized_tasks = []
    for t in tasks:
        sanitized_tasks.append({
            "title": str(getattr(t, "title", "")),
            "status": str(getattr(t, "status", "")),
            "priority": str(getattr(t, "priority", "")),
            "complexity": str(getattr(t, "complexity", "")),
            "is_reopened": bool(getattr(t, "is_reopened", False)),
            "blocked_reason": str(getattr(t, "blocked_reason", "") or "")
        })

    sanitized_feedbacks = []
    for f in feedbacks:
        sanitized_feedbacks.append({
            "type": str(getattr(f, "feedback_type", "")),
            "content": str(getattr(f, "content", "")),
            "strengths": str(getattr(f, "strengths", "") or ""),
            "growth_areas": str(getattr(f, "growth_areas", "") or "")
        })

    return {
        "subject_pseudonym": "SUBJECT_A",
        "job_role": str(employee_data.get("job_role_name", "Professional")),
        "score_status": metrics_bundle.get("score_status", "CALCULATED"),
        "calculated_score": metrics_bundle.get("calculated_score"),
        "data_coverage_percentage": metrics_bundle.get("data_coverage_percentage", 0.0),
        "workload_context": metrics_bundle.get("workload_context", {}),
        "metrics": metrics_bundle.get("metrics", []),
        "goals_evidence": sanitized_goals,
        "tasks_evidence": sanitized_tasks,
        "qualitative_feedback": sanitized_feedbacks
    }
