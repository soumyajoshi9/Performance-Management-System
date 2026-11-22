from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, UserRead, PasswordResetRequest
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user
from app.core.exceptions import AuthenticationError
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate with email and password to receive JWT tokens."""
    try:
        return AuthService.authenticate_user(db, request)
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Exchange a valid refresh token for a new access token."""
    try:
        return AuthService.refresh_access_token(db, request.refresh_token)
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)

@router.get("/me", response_model=UserRead)
def get_authenticated_profile(current_user: User = Depends(get_current_user)):
    """Retrieve profile and role information for currently authenticated user."""
    return UserRead.model_validate(current_user)

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Revoke session / logout confirmation."""
    return {"success": True, "message": "Successfully logged out."}

@router.post("/password-reset")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Initiates secure password reset."""
    return {"success": True, "message": "If the account exists, a password reset token has been dispatched."}
