from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.scoring import ScoringPreviewRequest, ScoreBreakdownResponse
from app.analytics.engine import ScoringEngine
from app.api.dependencies import get_current_user
from app.core.exceptions import EntityNotFoundError
from app.models.user import User

router = APIRouter(prefix="/scoring", tags=["Performance Scoring & Analytics Engine"])

@router.post("/preview", response_model=ScoreBreakdownResponse)
def preview_score(request: ScoringPreviewRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Computes deterministic performance metrics, data coverage %, and score breakdown.
    Enforces authorization: employees can preview self; managers can preview team.
    """
    if current_user.role == "EMPLOYEE" and current_user.id != request.employee_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to other employee scores.")
        
    try:
        breakdown = ScoringEngine.calculate_employee_performance(db, request.employee_id, request.review_period_id)
        return ScoreBreakdownResponse(**breakdown)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
