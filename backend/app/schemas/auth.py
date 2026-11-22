from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserRead"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)

class UserRead(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    department_id: Optional[str] = None
    job_role_id: Optional[str] = None
    manager_id: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

TokenResponse.model_rebuild()
