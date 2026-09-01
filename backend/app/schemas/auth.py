from pydantic import BaseModel, EmailStr
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str | None = None

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthUserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    user: AuthUserResponse
    token: Token
