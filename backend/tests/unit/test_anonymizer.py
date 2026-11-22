import json
from app.ai.anonymizer import anonymize_context_bundle
from app.ai.validator import validate_ai_output
from app.ai.grounding_audit import audit_evidence_citations

def test_anonymize_context_bundle_strips_pii():
    emp_data = {"job_role_name": "Senior Backend Engineer", "name": "Sarah Chen", "email": "sarah@company.com"}
    metrics = {
        "score_status": "CALCULATED",
        "calculated_score": 88.5,
        "data_coverage_percentage": 100.0,
        "metrics": [{"kpi_code": "KPI_TASK_COMPLETION", "raw_value": 90.0}]
    }
    
    class DummyObj:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    goals = [DummyObj(title="Goal 1", target_metric="Metric A", current_value=80, target_value=100, unit="percent", status="ACTIVE")]
    tasks = [DummyObj(title="Task 1", status="COMPLETED", priority="HIGH", complexity="MEDIUM", is_reopened=False, blocked_reason=None)]
    feedbacks = [DummyObj(feedback_type="MANAGER_TO_EMPLOYEE", content="Great performance", strengths="Fast", growth_areas="None")]

    bundle = anonymize_context_bundle(emp_data, metrics, goals, tasks, feedbacks)

    # Verify PII is stripped
    assert bundle["subject_pseudonym"] == "SUBJECT_A"
    assert "Sarah Chen" not in str(bundle)
    assert "sarah@company.com" not in str(bundle)
    assert bundle["job_role"] == "Senior Backend Engineer"
    assert len(bundle["goals_evidence"]) == 1
    assert len(bundle["tasks_evidence"]) == 1

def test_validate_ai_output_success():
    valid_json = json.dumps({
        "summary": "Employee achieved strong completion rates.",
        "strengths": ["Consistent delivery"],
        "improvement_areas": ["Document API contracts"],
        "observed_patterns": ["High velocity"],
        "contributing_factors": ["Normal workload"],
        "recommendations": ["Conduct weekly 1-on-1s"],
        "development_suggestions": ["Learn OpenTelemetry"],
        "limitations": ["Small sample size"],
        "evidence_references": ["KPI_TASK_COMPLETION"]
    })
    is_valid, parsed, err = validate_ai_output(valid_json)
    assert is_valid is True
    assert err == ""
    assert parsed["summary"] == "Employee achieved strong completion rates."
    assert "KPI_TASK_COMPLETION" in parsed["evidence_references"]

def test_validate_ai_output_invalid_json():
    invalid_text = "Here is my evaluation: {invalid json}"
    is_valid, parsed, err = validate_ai_output(invalid_text)
    assert is_valid is False
    assert "JSON Decode Error" in err

def test_audit_evidence_citations():
    available = [{"kpi_code": "KPI_TASK_COMPLETION"}, {"kpi_code": "KPI_DEADLINE_ADHERENCE"}]
    
    # Valid citation
    is_grounded, invalid = audit_evidence_citations(["KPI_TASK_COMPLETION"], available)
    assert is_grounded is True
    assert len(invalid) == 0

    # Fictional citation
    is_grounded, invalid = audit_evidence_citations(["KPI_FICTIONAL_METRIC"], available)
    assert is_grounded is False
    assert "KPI_FICTIONAL_METRIC" in invalid
