from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.review import PerformanceReview, ReviewMetricSnapshot
from app.models.user import User
from app.models.review_period import ReviewPeriod
from app.analytics.engine import ScoringEngine
from app.schemas.review import ReviewFinalizeRequest, PerformanceReviewRead
from app.core.exceptions import EntityNotFoundError, ConflictError, AuthorizationError

class ReviewService:
    @staticmethod
    def get_or_create_draft(db: Session, employee_id: str, review_period_id: str, reviewer: User) -> PerformanceReview:
        emp = db.query(User).filter_by(id=employee_id, is_active=True).first()
        if not emp:
            raise EntityNotFoundError("Employee", employee_id)
            
        period = db.query(ReviewPeriod).filter_by(id=review_period_id).first()
        if not period:
            raise EntityNotFoundError("ReviewPeriod", review_period_id)

        # Check existing review
        review = db.query(PerformanceReview).filter_by(
            employee_id=employee_id,
            review_period_id=review_period_id
        ).first()

        if not review:
            review = PerformanceReview(
                employee_id=employee_id,
                reviewer_id=reviewer.id,
                review_period_id=review_period_id,
                status="DRAFT",
                data_coverage_percentage=0.00
            )
            db.add(review)
            db.commit()
            db.refresh(review)

        # If not finalized, update preview analytics
        if review.status != "FINALIZED":
            scoring = ScoringEngine.calculate_employee_performance(db, employee_id, review_period_id)
            review.calculated_score = scoring["calculated_score"]
            review.score_status = scoring["score_status"]
            review.data_coverage_percentage = scoring["data_coverage_percentage"]
            db.commit()
            db.refresh(review)

        return review

    @staticmethod
    def finalize_review(db: Session, review_id: str, data: ReviewFinalizeRequest, reviewer: User) -> PerformanceReview:
        review = db.query(PerformanceReview).filter_by(id=review_id).first()
        if not review:
            raise EntityNotFoundError("PerformanceReview", review_id)

        if review.status == "FINALIZED":
            raise ConflictError("Performance review is already finalized and cannot be modified (DB-7).")

        # Auth check
        emp = db.query(User).filter_by(id=review.employee_id).first()
        if reviewer.role == "MANAGER" and emp.manager_id != reviewer.id and reviewer.role != "ADMIN":
            raise AuthorizationError("Only the assigned manager or HR can finalize this review.")

        # Compute deterministic final scores
        scoring = ScoringEngine.calculate_employee_performance(db, review.employee_id, review.review_period_id)
        now = datetime.now(timezone.utc)

        review.status = "FINALIZED"
        review.score_status = scoring["score_status"]
        review.calculated_score = scoring["calculated_score"]
        review.final_score = scoring["calculated_score"]
        review.data_coverage_percentage = scoring["data_coverage_percentage"]
        review.manager_summary = data.manager_summary
        if data.employee_remarks:
            review.employee_remarks = data.employee_remarks
        review.finalized_at = now

        # Create immutable historical snapshots for all metrics (DB-7)
        # Clear any prior draft snapshots
        db.query(ReviewMetricSnapshot).filter_by(performance_review_id=review.id).delete()

        for m in scoring["metrics"]:
            snapshot = ReviewMetricSnapshot(
                performance_review_id=review.id,
                kpi_code=m["kpi_code"],
                kpi_name=m["kpi_name"],
                category=m["category"],
                raw_value=m["raw_value"],
                normalized_score=m["normalized_score"],
                applied_weight=m["applied_weight"],
                evidence_count=m["evidence_count"],
                is_sufficient=m["is_sufficient"],
                data_status=m["data_status"],
                snapshot_data={
                    "min_evidence_threshold": m["min_evidence_threshold"],
                    "default_weight": m["default_weight"],
                    "unit": m["unit"],
                    "finalized_at": now.isoformat()
                }
            )
            db.add(snapshot)

        db.commit()
        db.refresh(review)
        return review
