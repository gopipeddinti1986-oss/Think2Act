import re
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.resume import Resume, ResumeSuggestion

def compute_ats_metrics(parsed_sections: dict, target_role: str) -> Tuple[float, List[dict]]:
    keywords_by_role = {
        "backend": ["python", "fastapi", "sql", "postgresql", "docker", "aws", "redis", "rest", "microservices", "asyncio", "kubernetes", "ci/cd"],
        "frontend": ["react", "typescript", "javascript", "tailwind", "vite", "html", "css", "state management", "rest", "graphql"],
        "fullstack": ["python", "fastapi", "react", "typescript", "postgresql", "docker", "aws", "redis", "rest", "git"]
    }
    role_key = "frontend" if "frontend" in target_role.lower() else "fullstack" if "full" in target_role.lower() else "backend"
    role_keywords = keywords_by_role[role_key]

    skills_list = parsed_sections.get("skills", [])
    skills_text = " ".join(skills_list) if isinstance(skills_list, list) else str(skills_list)
    exp_list = parsed_sections.get("experience", [])
    exp_text = " ".join(exp_list) if isinstance(exp_list, list) else str(exp_list)
    summary_text = parsed_sections.get("summary", "")
    full_text = f"{summary_text} {exp_text} {skills_text}".lower()

    # 1. Keyword coverage (40 pts)
    matched_kws = [kw for kw in role_keywords if kw in full_text]
    missing_kws = [kw for kw in role_keywords if kw not in full_text]
    kw_score = (len(matched_kws) / len(role_keywords)) * 40.0

    # 2. Measurable metrics (25 pts)
    metric_bullets = 0
    total_bullets = len(exp_list) if isinstance(exp_list, list) else 1
    if isinstance(exp_list, list):
        for b in exp_list:
            if re.search(r'\d+[%kKmM]?|\$\d+|\d+ms', b):
                metric_bullets += 1
    metric_ratio = metric_bullets / max(1, total_bullets)
    metric_score = metric_ratio * 25.0

    # 3. Action Verbs (20 pts)
    action_verbs = ["architected", "engineered", "deployed", "scaled", "designed", "implemented", "optimized", "built", "spearheaded", "automated"]
    matched_verbs = [v for v in action_verbs if v in full_text]
    verb_score = min(20.0, (len(matched_verbs) / 4.0) * 20.0)

    # 4. Structure & Completeness (15 pts)
    struct_score = 0.0
    if summary_text and len(summary_text) > 20:
        struct_score += 5.0
    if exp_list and len(exp_list) > 0:
        struct_score += 5.0
    if skills_list and len(skills_list) > 0:
        struct_score += 5.0

    total_score = round(min(100.0, kw_score + metric_score + verb_score + struct_score), 1)

    # Generate suggestions for missing high-impact items
    suggestions = []
    if missing_kws:
        recommended_additions = ", ".join([k.title() for k in missing_kws[:3]])
        current_skills_str = ", ".join(skills_list) if isinstance(skills_list, list) else str(skills_list)
        suggestions.append({
            "section": "skills",
            "suggestion_type": "MISSING_KEYWORD",
            "current_text": current_skills_str,
            "recommended_text": f"{current_skills_str}, {recommended_additions}",
            "impact_reason": f"Aligns with Tier-1 {target_role} listing keyword criteria: {recommended_additions}."
        })

    if isinstance(exp_list, list):
        for bullet in exp_list:
            if not re.search(r'\d+[%kKmM]?|\$\d+|\d+ms', bullet):
                suggestions.append({
                    "section": "experience",
                    "suggestion_type": "QUANTIFIABLE_METRIC",
                    "current_text": bullet,
                    "recommended_text": f"{bullet.rstrip('.')} achieving 35% throughput increase and sub-50ms p99 latency.",
                    "impact_reason": "Adds exact performance benchmark and architectural leadership terminology for ATS scanners."
                })
                break

    # If all bullets already had metrics, provide an architectural optimization suggestion
    if not any(s["suggestion_type"] == "QUANTIFIABLE_METRIC" for s in suggestions) and exp_list:
        first_b = exp_list[0]
        suggestions.append({
            "section": "experience",
            "suggestion_type": "QUANTIFIABLE_METRIC",
            "current_text": first_b,
            "recommended_text": f"Architected and deployed distributed services handling 20k+ req/sec at 99.99% availability.",
            "impact_reason": "Highlights high-scale distributed architectural impact."
        })

    return total_score, suggestions

class ResumeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: UUID) -> List[Resume]:
        result = await self.db.execute(
            select(Resume).where(Resume.user_id == user_id).order_by(desc(Resume.updated_at))
        )
        return list(result.scalars().all())

    async def get_by_id(self, resume_id: UUID, user_id: UUID) -> Optional[Resume]:
        result = await self.db.execute(
            select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: UUID, title: str, target_role: str, raw_text: Optional[str] = None) -> Resume:
        default_sections = {
            "summary": "Experienced backend developer specialized in high concurrency microservices and scalable APIs.",
            "experience": [
                "Engineered REST & GraphQL backend services handling 10k+ req/sec using FastAPI and PostgreSQL.",
                "Implemented distributed Redis caching layer, decreasing p99 latency by 35%."
            ],
            "skills": ["Python", "FastAPI", "SQL", "PostgreSQL", "Docker", "AWS", "Redis"]
        }

        ats_score, sugg_data = compute_ats_metrics(default_sections, target_role)

        resume = Resume(
            user_id=user_id,
            title=title,
            target_role=target_role,
            raw_text=raw_text,
            ats_score=ats_score,
            parsed_sections=default_sections
        )
        self.db.add(resume)
        await self.db.flush()

        for s in sugg_data:
            self.db.add(ResumeSuggestion(
                resume_id=resume.id,
                section=s["section"],
                suggestion_type=s["suggestion_type"],
                current_text=s["current_text"],
                recommended_text=s["recommended_text"],
                impact_reason=s["impact_reason"]
            ))

        await self.db.commit()
        await self.db.refresh(resume)
        return resume

    async def apply_suggestion(self, resume_id: UUID, suggestion_id: UUID, user_id: UUID) -> Optional[Resume]:
        resume = await self.get_by_id(resume_id, user_id)
        if not resume:
            return None
        result = await self.db.execute(
            select(ResumeSuggestion).where(ResumeSuggestion.id == suggestion_id, ResumeSuggestion.resume_id == resume_id)
        )
        sugg = result.scalar_one_or_none()
        if sugg and not sugg.is_applied:
            sugg.is_applied = True
            sections = dict(resume.parsed_sections or {})

            if sugg.section == "skills" and sugg.recommended_text:
                sections["skills"] = [s.strip() for s in sugg.recommended_text.split(",") if s.strip()]
            elif sugg.section == "experience" and sugg.recommended_text:
                exp_bullets = list(sections.get("experience", []))
                for i, b in enumerate(exp_bullets):
                    if b == sugg.current_text or sugg.current_text in b:
                        exp_bullets[i] = sugg.recommended_text
                        break
                sections["experience"] = exp_bullets

            resume.parsed_sections = sections
            new_score, _ = compute_ats_metrics(sections, resume.target_role or "Backend Software Engineer")
            resume.ats_score = max(round(resume.ats_score + 2.0, 1), new_score)

            await self.db.commit()
            await self.db.refresh(resume)
        return resume
