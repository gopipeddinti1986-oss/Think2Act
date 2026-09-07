from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserProfile
from app.models.goal import Goal
from app.models.task import Task
from app.models.skill import UserSkill, Skill, Evidence
from app.models.decision import Decision

router = APIRouter()

@router.get("", response_model=Dict[str, Any])
async def get_settings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalars().first()

    return {
        "user_id": str(current_user.id),
        "name": current_user.name,
        "email": current_user.email,
        "user_mode": profile.user_mode if profile else "student",
        "timezone": profile.timezone if profile else "UTC",
        "bio": profile.bio if profile else "",
        "location": profile.location if profile else "",
        "organization": profile.organization if profile else "",
        "education": profile.education if profile else "",
        "experience": profile.experience if profile else "",
        "career_goal": profile.career_goal if profile else "",
        "target_role": getattr(profile, "target_role", None) or "",
        "target_companies": getattr(profile, "target_companies", None) or [],
        "career_mode": getattr(profile, "career_mode", None) or "ACTIVE_SEARCH",
        "experience_level": getattr(profile, "experience_level", None) or "Entry",
        "github_handle": getattr(profile, "github_handle", None) or "",
        "linkedin_profile_url": getattr(profile, "linkedin_profile_url", None) or "",
        "leetcode_username": getattr(profile, "leetcode_username", None) or "",
        "work_start_time": getattr(profile, "work_start_time", "09:00") or "09:00",
        "work_end_time": getattr(profile, "work_end_time", "18:00") or "18:00",
        "preferred_sprint_minutes": getattr(profile, "preferred_sprint_minutes", 45) or 45,
        "notification_preferences": getattr(profile, "notification_preferences", {}) or {},
    }

@router.put("/profile")
async def update_profile(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if "name" in payload and payload["name"]:
        current_user.name = payload["name"]

    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalars().first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    for field in [
        "bio", "location", "organization", "education", "experience",
        "user_mode", "timezone", "career_goal", "experience_level"
    ]:
        if field in payload and payload[field] is not None:
            setattr(profile, field, payload[field])

    await db.commit()
    return {"message": "Profile updated successfully."}

@router.put("/career")
async def update_career_settings(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalars().first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    if "target_role" in payload:
        profile.target_role = payload["target_role"]
    if "target_companies" in payload:
        profile.target_companies = payload["target_companies"]
    if "career_mode" in payload:
        profile.career_mode = payload["career_mode"]
    if "experience_level" in payload:
        profile.experience_level = payload["experience_level"]
    if "experience" in payload:
        profile.experience = payload["experience"]

    await db.commit()
    return {"message": "Career preferences updated successfully."}

@router.put("/availability")
async def update_availability(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalars().first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    if "work_start_time" in payload:
        profile.work_start_time = payload["work_start_time"]
    if "work_end_time" in payload:
        profile.work_end_time = payload["work_end_time"]
    if "preferred_sprint_minutes" in payload:
        profile.preferred_sprint_minutes = int(payload["preferred_sprint_minutes"])

    await db.commit()
    return {"message": "Work availability updated successfully."}

@router.put("/notifications")
async def update_notifications(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalars().first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    profile.notification_preferences = payload
    await db.commit()
    return {"message": "Notification preferences updated successfully."}

@router.put("/integrations")
async def update_integrations(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalars().first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    if "github_handle" in payload:
        profile.github_handle = payload["github_handle"]
    if "linkedin_profile_url" in payload:
        profile.linkedin_profile_url = payload["linkedin_profile_url"]
    if "leetcode_username" in payload:
        profile.leetcode_username = payload["leetcode_username"]

    await db.commit()
    return {"message": "Integrations updated successfully."}

@router.get("/export")
async def export_user_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    goals_res = await db.execute(select(Goal).where(Goal.user_id == current_user.id))
    goals = goals_res.scalars().all()

    tasks_res = await db.execute(select(Task).where(Task.user_id == current_user.id))
    tasks = tasks_res.scalars().all()

    skills_res = await db.execute(select(UserSkill).where(UserSkill.user_id == current_user.id))
    skills = skills_res.scalars().all()

    evidence_res = await db.execute(select(Evidence).where(Evidence.user_id == current_user.id))
    evidence_items = evidence_res.scalars().all()

    decisions_res = await db.execute(select(Decision).where(Decision.user_id == current_user.id))
    decisions = decisions_res.scalars().all()

    return {
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "user": {
            "id": str(current_user.id),
            "name": current_user.name,
            "email": current_user.email
        },
        "goals": [{"id": str(g.id), "title": g.title, "priority": g.priority, "status": g.status} for g in goals],
        "tasks": [{"id": str(t.id), "title": t.title, "status": t.status, "estimated_minutes": t.estimated_minutes, "actual_minutes": t.actual_minutes} for t in tasks],
        "skills": [{"skill_id": str(s.skill_id), "level": float(s.level), "confidence": float(s.confidence)} for s in skills],
        "evidence": [{"id": str(e.id), "source_type": e.source_type, "strength": float(e.strength), "description": e.description} for e in evidence_items],
        "decisions": [{"id": str(d.id), "title": d.title, "status": d.status} for d in decisions],
    }

@router.delete("/account", status_code=status.HTTP_200_OK)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.delete(current_user)
    await db.commit()
    return {"message": "Account deleted successfully."}
