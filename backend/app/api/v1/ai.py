from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.ai_insight import AIInsight
from app.models.user import User
from app.models.goal import Goal
from app.models.task import Task
from app.models.feedback import Feedback
from app.models.review import PerformanceReview
from app.schemas.ai import AIInsightGenerateRequest, FlagInsightRequest, AIInsightRead
from app.analytics.engine import ScoringEngine
from app.ai.anonymizer import anonymize_context_bundle
from app.ai.client import AIClient
from app.api.dependencies import get_current_user
from app.core.exceptions import EntityNotFoundError

router = APIRouter(prefix="/ai", tags=["AI Intelligence & Explanations"])

@router.post("/insights/generate", response_model=AIInsightRead)
def generate_insight(data: AIInsightGenerateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    emp = db.query(User).filter_by(id=data.employee_id, is_active=True).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")
        
    # Auth boundary
    if current_user.role == "EMPLOYEE" and current_user.id != emp.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    if current_user.role == "MANAGER" and emp.manager_id != current_user.id and emp.id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Restricted to direct reports.")

    # 1. Deterministic metrics bundle
    metrics_bundle = ScoringEngine.calculate_employee_performance(db, data.employee_id, data.review_period_id)
    
    # 2. Evidence
    goals = db.query(Goal).filter_by(employee_id=data.employee_id, review_period_id=data.review_period_id).all()
    tasks = db.query(Task).filter_by(employee_id=data.employee_id).all()
    feedbacks = db.query(Feedback).filter_by(employee_id=data.employee_id, review_period_id=data.review_period_id).all()
    
    # Optional linked performance review
    review = db.query(PerformanceReview).filter_by(
        employee_id=data.employee_id,
        review_period_id=data.review_period_id
    ).first()

    # 3. PII Anonymization
    sanitized = anonymize_context_bundle(
        employee_data={"job_role_name": emp.job_role.name if emp.job_role else "Professional"},
        metrics_bundle=metrics_bundle,
        goals=goals,
        tasks=tasks,
        feedbacks=feedbacks
    )

    # 4. Generate structured insight
    ai_result = AIClient.generate_insight(sanitized)

    # 5. Save to database
    insight = AIInsight(
        employee_id=data.employee_id,
        performance_review_id=review.id if review else None,
        review_period_id=data.review_period_id,
        prompt_version=ai_result["prompt_version"],
        model_version=ai_result["model_version"],
        structured_output=ai_result["structured_output"],
        status="GENERATED"
    )
    db.add(insight)
    db.commit()
    db.refresh(insight)

    return insight

@router.get("/insights/{id}", response_model=AIInsightRead)
def get_insight(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    insight = db.query(AIInsight).filter_by(id=id).first()
    if not insight:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI insight not found.")
        
    if current_user.role == "EMPLOYEE" and insight.employee_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
        
    return insight

@router.post("/insights/{id}/flag", response_model=AIInsightRead)
def flag_insight(id: str, data: FlagInsightRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    insight = db.query(AIInsight).filter_by(id=id).first()
    if not insight:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI insight not found.")
        
    if current_user.role == "EMPLOYEE" and insight.employee_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    insight.status = "FLAGGED"
    insight.flag_reason = data.flag_reason
    insight.flagged_by_id = current_user.id
    db.commit()
    db.refresh(insight)
    return insight
