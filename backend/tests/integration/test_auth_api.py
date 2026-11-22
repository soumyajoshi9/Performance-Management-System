import pytest
from fastapi import HTTPException
from app.schemas.auth import LoginRequest
from app.api.v1 import auth

def test_login_success_and_profile_access(db_session):
    # 1. Login with demo employee
    resp = auth.login(LoginRequest(
        email="employee@vyora.local",
        password="EmployeePass123!"
    ), db_session)
    assert resp.access_token is not None
    assert resp.user.email == "employee@vyora.local"
    assert resp.user.role == "EMPLOYEE"

    # 2. Access /auth/me with user profile
    from app.models.user import User
    current_user = db_session.query(User).filter_by(email="employee@vyora.local").first()
    profile = auth.get_authenticated_profile(current_user)
    assert profile.email == "employee@vyora.local"
    assert profile.role == "EMPLOYEE"

def test_login_invalid_password(db_session):
    with pytest.raises(HTTPException) as exc_info:
        auth.login(LoginRequest(
            email="employee@vyora.local",
            password="WrongPassword!"
        ), db_session)
    assert exc_info.value.status_code == 401
    assert "Invalid email or password" in exc_info.value.detail
