from typing import List, Dict, Any, Tuple

def audit_data_coverage(
    metric_results: List[Dict[str, Any]],
    coverage_threshold_pct: float = 50.0
) -> Tuple[float, bool, List[Dict[str, Any]]]:
    """
    Audits evidence sufficiency for role KPIs.
    - If evidence_count < min_evidence_threshold: marks data_status as 'NOT_AVAILABLE'.
    - Computes coverage percentage based on configured default weights.
    - If coverage >= 50%: redistributes weights proportionally across available metrics.
    - If coverage < 50%: score status is 'INSUFFICIENT_DATA'.
    """
    total_configured_weight = sum(float(m.get("default_weight", 0.0)) for m in metric_results)
    if total_configured_weight <= 0.0:
        total_configured_weight = 100.0

    valid_weight_sum = 0.0
    audited_metrics = []

    for m in metric_results:
        weight = float(m.get("default_weight", 0.0))
        evidence_count = int(m.get("evidence_count", 0))
        min_threshold = int(m.get("min_evidence_threshold", 1))
        
        is_sufficient = evidence_count >= min_threshold
        if is_sufficient and m.get("raw_value") is not None:
            data_status = "AVAILABLE"
            valid_weight_sum += weight
        else:
            data_status = "NOT_AVAILABLE"

        m_copy = dict(m)
        m_copy["is_sufficient"] = is_sufficient
        m_copy["data_status"] = data_status
        audited_metrics.append(m_copy)

    coverage_pct = round((valid_weight_sum / total_configured_weight) * 100.0, 2)
    is_overall_sufficient = coverage_pct >= coverage_threshold_pct

    # Proportional weight redistribution across available metrics
    for m in audited_metrics:
        if m["data_status"] == "AVAILABLE" and valid_weight_sum > 0:
            m["applied_weight"] = round((float(m["default_weight"]) / valid_weight_sum) * 100.0, 2)
        else:
            m["applied_weight"] = 0.0

    return coverage_pct, is_overall_sufficient, audited_metrics
