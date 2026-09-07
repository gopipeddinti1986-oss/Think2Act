from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    timezone: Optional[str] = "UTC"

class CareerPreferencesUpdate(BaseModel):
    target_role: Optional[str] = None
    target_companies: Optional[List[str]] = None
    experience_level: Optional[str] = "Entry"  # Options: Entry, Mid, Senior, Lead
    career_mode: Optional[str] = "ACTIVE_SEARCH"  # Options: ACTIVE_SEARCH, SKILL_BUILDING, PASSIVE

class IntegrationHandlesUpdate(BaseModel):
    github_handle: Optional[str] = None
    linkedin_profile_url: Optional[str] = None
    leetcode_username: Optional[str] = None

class UserSettingsResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    timezone: str
    target_role: Optional[str] = None
    target_companies: List[str] = []
    experience_level: str = "Entry"
    career_mode: str = "ACTIVE_SEARCH"
    github_handle: Optional[str] = None
    linkedin_profile_url: Optional[str] = None
    leetcode_username: Optional[str] = None