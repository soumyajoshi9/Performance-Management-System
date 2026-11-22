from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.organizations import router as org_router
from app.api.v1.users import router as users_router
from app.api.v1.review_periods import router as review_periods_router
from app.api.v1.goals import router as goals_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.kpis import router as kpis_router
from app.api.v1.scoring import router as scoring_router
from app.api.v1.feedbacks import router as feedbacks_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.ai import router as ai_router
from app.api.v1.development_plans import router as dev_plans_router
from app.api.v1.audit import router as audit_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(org_router)
api_router.include_router(users_router)
api_router.include_router(review_periods_router)
api_router.include_router(goals_router)
api_router.include_router(tasks_router)
api_router.include_router(kpis_router)
api_router.include_router(scoring_router)
api_router.include_router(feedbacks_router)
api_router.include_router(reviews_router)
api_router.include_router(ai_router)
api_router.include_router(dev_plans_router)
api_router.include_router(audit_router)
