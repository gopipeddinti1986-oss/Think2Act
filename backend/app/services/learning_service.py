from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.learning_repository import LearningRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.evidence_repository import EvidenceRepository
from app.schemas.learning import (
    RoleResponse, RoleSkillRequirement, SkillGapItem, SkillGapReport,
    LearningResourceResponse, LearningPathResponse, LearningPathItemResponse,
    GenerateRoadmapRequest, ConvertLearningToTaskResponse
)
from app.schemas.task import TaskCreate, TaskResponse
from app.schemas.evidence import EvidenceCreate

class LearningService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.learning_repo = LearningRepository(db)
        self.skill_repo = SkillRepository(db)
        self.task_repo = TaskRepository(db)
        self.evidence_repo = EvidenceRepository(db)

    async def ensure_defaults(self):
        # 1. Seed global skills
        from app.services.skill_service import SkillService
        await SkillService(self.db).ensure_default_seeds()

        # 2. Seed Default Role: Backend Software Engineer
        role = await self.learning_repo.get_role_by_name("Backend Software Engineer")
        if not role:
            role = await self.learning_repo.create_role(
                name="Backend Software Engineer",
                category="Software Engineering",
                description="Designs scalable REST APIs, relational database schemas, and containerized backend services."
            )
            # Map required skills
            all_skills = await self.skill_repo.list_all()
            skill_map = {s.name: s for s in all_skills}
            
            reqs = [
                ("Python", 80.0, "HIGH"),
                ("FastAPI", 75.0, "HIGH"),
                ("SQL & PostgreSQL", 75.0, "HIGH"),
                ("Docker & Containers", 65.0, "HIGH"),
                ("Data Structures & Algorithms", 70.0, "HIGH"),
                ("Git & Version Control", 70.0, "MEDIUM"),
                ("AWS Cloud", 60.0, "MEDIUM"),
            ]
            for sname, req_lvl, imp in reqs:
                if sname in skill_map:
                    await self.learning_repo.add_role_skill(
                        role_id=role.id,
                        skill_id=skill_map[sname].id,
                        required_level=req_lvl,
                        importance=imp
                    )

        # 3. Seed Learning Resources
        resources = await self.learning_repo.list_resources()
        if not resources:
            all_skills = await self.skill_repo.list_all()
            skill_map = {s.name: s for s in all_skills}

            sample_resources = [
                {
                    "title": "Mastering PostgreSQL Queries & Index Optimization",
                    "provider": "Documentation & Labs",
                    "url": "https://www.postgresql.org/docs/",
                    "description": "Deep dive into execution plans, indexing strategies, and transactional consistency.",
                    "difficulty": "Intermediate",
                    "skill_name": "SQL & PostgreSQL"
                },
                {
                    "title": "Production Docker & Compose for Python Microservices",
                    "provider": "Interactive Workshop",
                    "url": "https://docs.docker.com/compose/",
                    "description": "Containerizing FastAPI services with health checks and multi-stage Dockerfiles.",
                    "difficulty": "Intermediate",
                    "skill_name": "Docker & Containers"
                },
                {
                    "title": "Advanced Tree & Graph Algorithms Mastery",
                    "provider": "LeetCode & Problem Sets",
                    "url": "https://leetcode.com/problemset/",
                    "description": "Graph traversals, BFS/DFS applications, and topological sorting.",
                    "difficulty": "Advanced",
                    "skill_name": "Data Structures & Algorithms"
                },
                {
                    "title": "FastAPI Dependency Injection & Background Tasks",
                    "provider": "FastAPI Official Guide",
                    "url": "https://fastapi.tiangolo.com/",
                    "description": "Asynchronous request handling, Pydantic v2 schemas, and security scopes.",
                    "difficulty": "Intermediate",
                    "skill_name": "FastAPI"
                }
            ]

            for r in sample_resources:
                new_r = await self.learning_repo.create_resource(
                    title=r["title"],
                    provider=r["provider"],
                    url=r["url"],
                    description=r["description"],
                    difficulty=r["difficulty"]
                )
                if r["skill_name"] in skill_map:
                    await self.learning_repo.link_resource_skill(new_r.id, skill_map[r["skill_name"]].id)

    async def list_roles(self) -> List[RoleResponse]:
        await self.ensure_defaults()
        roles = await self.learning_repo.list_roles()
        results: List[RoleResponse] = []
        for r in roles:
            requirements = [
                RoleSkillRequirement(
                    skill_id=rs.skill_id,
                    skill_name=rs.skill.name if rs.skill else "Skill",
                    required_level=float(rs.required_level),
                    importance=rs.importance
                )
                for rs in r.role_skills
            ]
            results.append(RoleResponse(
                id=r.id,
                name=r.name,
                category=r.category,
                description=r.description,
                requirements=requirements
            ))
        return results

    async def compute_skill_gaps(self, user_id: UUID, role_id: Optional[UUID] = None) -> SkillGapReport:
        await self.ensure_defaults()
        if not role_id:
            roles = await self.learning_repo.list_roles()
            if not roles:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No roles defined.")
            role = roles[0]
        else:
            role = await self.learning_repo.get_role_by_id(role_id)
            if not role:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found.")

        # User's current skills
        user_skills = await self.skill_repo.list_user_skills(user_id)
        user_skill_map = {us.skill_id: float(us.level) for us in user_skills}

        gaps: List[SkillGapItem] = []
        total_weight = 0.0
        earned_weight = 0.0
        critical_count = 0

        imp_multiplier = {"HIGH": 1.5, "MEDIUM": 1.0, "LOW": 0.5}

        for rs in role.role_skills:
            skill = rs.skill
            current_lvl = user_skill_map.get(rs.skill_id, 0.0)
            req_lvl = float(rs.required_level)
            gap = max(0.0, round(req_lvl - current_lvl, 1))

            weight = imp_multiplier.get(rs.importance, 1.0)
            total_weight += req_lvl * weight
            earned_weight += min(req_lvl, current_lvl) * weight

            # Severity classification
            if gap >= 25.0 and rs.importance == "HIGH":
                severity = "CRITICAL"
                critical_count += 1
                rec_action = f"Prioritize dedicated project practice in {skill.name}"
            elif gap > 15.0:
                severity = "IMPORTANT"
                rec_action = f"Complete structured learning exercises for {skill.name}"
            elif gap > 0.0:
                severity = "MODERATE"
                rec_action = f"Solidify hands-on tasks to close {gap} pt gap"
            else:
                severity = "MINOR"
                rec_action = "Requirement satisfied. Maintain active practice."

            gaps.append(SkillGapItem(
                skill_id=rs.skill_id,
                skill_name=skill.name if skill else "Skill",
                category=skill.category if skill else "General",
                current_level=current_lvl,
                required_level=req_lvl,
                gap=gap,
                importance=rs.importance,
                severity=severity,
                recommended_action=rec_action
            ))

        # Sort gaps by severity/gap
        severity_order = {"CRITICAL": 4, "IMPORTANT": 3, "MODERATE": 2, "MINOR": 1}
        gaps.sort(key=lambda g: (severity_order.get(g.severity, 0), g.gap), reverse=True)

        overall_readiness = round((earned_weight / total_weight * 100), 1) if total_weight > 0 else 0.0

        return SkillGapReport(
            role_id=role.id,
            role_name=role.name,
            overall_readiness=overall_readiness,
            total_gaps=len([g for g in gaps if g.gap > 0]),
            critical_gaps=critical_count,
            gaps=gaps
        )

    async def list_learning_resources(self) -> List[LearningResourceResponse]:
        await self.ensure_defaults()
        res = await self.learning_repo.list_resources()
        return [LearningResourceResponse.model_validate(r) for r in res]

    async def list_user_paths(self, user_id: UUID) -> List[LearningPathResponse]:
        paths = await self.learning_repo.list_paths_by_user(user_id)
        results: List[LearningPathResponse] = []
        for p in paths:
            items_resp = [
                LearningPathItemResponse(
                    id=item.id,
                    learning_path_id=item.learning_path_id,
                    skill_id=item.skill_id,
                    skill_name=item.skill.name if item.skill else "Skill",
                    title=item.title,
                    sequence_number=item.sequence_number,
                    status=item.status,
                    progress=float(item.progress),
                    resource=LearningResourceResponse.model_validate(item.resource) if item.resource else None
                )
                for item in p.items
            ]
            results.append(LearningPathResponse(
                id=p.id,
                user_id=p.user_id,
                goal_id=p.goal_id,
                role_id=p.role_id,
                title=p.title,
                status=p.status,
                created_at=p.created_at,
                items=items_resp
            ))
        return results

    async def generate_learning_roadmap(
        self,
        user_id: UUID,
        data: GenerateRoadmapRequest
    ) -> LearningPathResponse:
        gap_report = await self.compute_skill_gaps(user_id, data.role_id)
        
        path_title = data.title or f"{gap_report.role_name} Accelerated Roadmap"
        path = await self.learning_repo.create_path(
            user_id=user_id,
            title=path_title,
            role_id=gap_report.role_id,
            goal_id=data.goal_id
        )

        resources = await self.learning_repo.list_resources()
        resource_map = {r.title: r for r in resources}

        seq = 1
        for gap in gap_report.gaps:
            if gap.gap <= 0:
                continue
            
            # Match a resource if available
            matched_res = None
            for r in resources:
                if any(s.skill_id == gap.skill_id for s in r.skills):
                    matched_res = r
                    break

            # Create step 1: Practice & Implementation
            await self.learning_repo.add_path_item(
                learning_path_id=path.id,
                skill_id=gap.skill_id,
                title=f"Master {gap.skill_name}: Core Concepts & Drills",
                sequence_number=seq,
                resource_id=matched_res.id if matched_res else None
            )
            seq += 1

            # Create step 2: Real Project Application
            await self.learning_repo.add_path_item(
                learning_path_id=path.id,
                skill_id=gap.skill_id,
                title=f"Build and ship a mini-project featuring {gap.skill_name}",
                sequence_number=seq,
                resource_id=None
            )
            seq += 1

        full_path = await self.learning_repo.get_path_by_id(path.id, user_id)
        items_resp = [
            LearningPathItemResponse(
                id=item.id,
                learning_path_id=item.learning_path_id,
                skill_id=item.skill_id,
                skill_name=item.skill.name if item.skill else "Skill",
                title=item.title,
                sequence_number=item.sequence_number,
                status=item.status,
                progress=float(item.progress),
                resource=LearningResourceResponse.model_validate(item.resource) if item.resource else None
            )
            for item in full_path.items
        ]
        return LearningPathResponse(
            id=full_path.id,
            user_id=full_path.user_id,
            goal_id=full_path.goal_id,
            role_id=full_path.role_id,
            title=full_path.title,
            status=full_path.status,
            created_at=full_path.created_at,
            items=items_resp
        )

    async def convert_item_to_task(self, item_id: UUID, user_id: UUID) -> ConvertLearningToTaskResponse:
        item = await self.learning_repo.get_path_item_by_id(item_id)
        if not item or item.learning_path.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning item not found.")

        # Create Task in execution system
        task = await self.task_repo.create(
            user_id=user_id,
            data=TaskCreate(
                title=item.title,
                description=f"Roadmap milestone for {item.skill.name if item.skill else 'Skill'} from '{item.learning_path.title}'",
                goal_id=item.learning_path.goal_id,
                category="Learning",
                priority="HIGH",
                estimated_minutes=60,
                status="TODO"
            )
        )

        # Associate Task to Skill
        await self.skill_repo.assign_task_skills(task.id, [item.skill_id])

        # Mark learning item as in-progress
        item.status = "IN_PROGRESS"
        item.progress = 25.0
        await self.db.commit()

        return ConvertLearningToTaskResponse(
            task=TaskResponse.model_validate(task),
            message="Converted roadmap milestone into active task. Ready for scheduling and focus."
        )

    async def complete_path_item(self, item_id: UUID, user_id: UUID) -> LearningPathItemResponse:
        item = await self.learning_repo.get_path_item_by_id(item_id)
        if not item or item.learning_path.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning item not found.")

        item.status = "COMPLETED"
        item.progress = 100.0
        await self.db.commit()

        # Generate Evidence & Boost Skill
        from app.services.skill_service import SkillService
        skill_service = SkillService(self.db)
        await skill_service.add_evidence_and_recalculate(
            user_id=user_id,
            data=EvidenceCreate(
                skill_id=item.skill_id,
                source_type="PROJECT",
                strength=20.0,
                description=f"Completed Learning Roadmap milestone: {item.title}"
            )
        )

        await self.db.refresh(item, ["skill", "resource"])
        return LearningPathItemResponse(
            id=item.id,
            learning_path_id=item.learning_path_id,
            skill_id=item.skill_id,
            skill_name=item.skill.name if item.skill else "Skill",
            title=item.title,
            sequence_number=item.sequence_number,
            status=item.status,
            progress=float(item.progress),
            resource=LearningResourceResponse.model_validate(item.resource) if item.resource else None
        )
