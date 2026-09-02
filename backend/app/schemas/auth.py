from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthUserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AuthResponse(BaseModel):
    user: AuthUserResponse
    token: Token
