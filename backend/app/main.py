from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.exceptions import VyoraBaseException
from app.api.router import api_router
from datetime import datetime, timezone
import uuid

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="Smart Performance Management & Employee Development Intelligence Platform",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler for domain exceptions
@app.exception_handler(VyoraBaseException)
async def domain_exception_handler(request: Request, exc: VyoraBaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    if exc.code == "AUTHENTICATION_FAILED":
        status_code = status.HTTP_401_UNAUTHORIZED
    elif exc.code == "PERMISSION_DENIED":
        status_code = status.HTTP_403_FORBIDDEN
    elif exc.code == "ENTITY_NOT_FOUND":
        status_code = status.HTTP_404_NOT_FOUND
    elif exc.code == "CONFLICT":
        status_code = status.HTTP_409_CONFLICT
        
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            },
            "meta": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": str(uuid.uuid4())
            }
        }
    )

# Register API router
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} initialized in {settings.ENVIRONMENT} mode.")

@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "ONLINE",
        "docs_url": "/docs",
        "api_v1_health": "/api/v1/audit/health"
    }
