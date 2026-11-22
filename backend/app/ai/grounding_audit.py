from typing import List, Dict, Any

def audit_evidence_citations(
    cited_evidence_keys: List[str],
    available_metrics: List[Dict[str, Any]]
) -> tuple[bool, List[str]]:
    """
    Verifies that all metric codes cited in AI output exist in the supplied context.
    Returns (is_grounded, invalid_citations).
    """
    valid_codes = {m["kpi_code"] for m in available_metrics}
    invalid = [code for code in cited_evidence_keys if code not in valid_codes]
    return (len(invalid) == 0, invalid)
