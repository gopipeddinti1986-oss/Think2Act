from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserProfileBase(BaseModel):
    bio: Optional[str] = None
    location: Optional[str] = None
    organization: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    user_mode: str = "student"
    career_goal: Optional[str] = None
    timezone: str = "UTC"

class UserProfileUpdate(BaseModel):
    bio: Optional[str] = None
    location: Optional[str] = None
    organization: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    user_mode: Optional[str] = None
    career_goal: Optional[str] = None
    timezone: Optional[str] = None

class UserProfileResponse(UserProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDetailResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime
    profile: Optional[UserProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)
