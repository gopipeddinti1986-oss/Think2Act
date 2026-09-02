from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from app.models.decision import Decision, DecisionOption, DecisionCriterion, DecisionScore

class DecisionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: UUID) -> List[Decision]:
        result = await self.db.execute(
            select(Decision)
            .options(
                selectinload(Decision.options).selectinload(DecisionOption.scores),
                selectinload(Decision.criteria)
            )
            .where(Decision.user_id == user_id)
            .order_by(desc(Decision.updated_at))
        )
        return list(result.scalars().all())

    async def get_by_id(self, decision_id: UUID, user_id: Optional[UUID] = None) -> Optional[Decision]:
        query = (
            select(Decision)
            .options(
                selectinload(Decision.options).selectinload(DecisionOption.scores),
                selectinload(Decision.criteria)
            )
            .where(Decision.id == decision_id)
        )
        if user_id:
            query = query.where(Decision.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: UUID,
        title: str,
        description: Optional[str] = None,
        category: str = "CAREER",
        options: List[str] = [],
        criteria: List[Dict[str, Any]] = []
    ) -> Decision:
        decision = Decision(
            user_id=user_id,
            title=title,
            description=description,
            category=category,
            status="DRAFT"
        )
        self.db.add(decision)
        await self.db.flush()

        default_criteria = criteria or [
            {"name": "Career Growth & Leverage", "weight": 5.0},
            {"name": "Execution Time Commitment", "weight": 3.0},
            {"name": "Financial Compensation", "weight": 4.0},
            {"name": "Technical Learning Depth", "weight": 4.0}
        ]

        default_options = options or [
            "Join High-Growth AI Startup as Senior Backend Engineer",
            "Transition to Lead Distributed Systems Role at Mid-Scale SaaS"
        ]

        crit_objs = []
        for c in default_criteria:
            crit = DecisionCriterion(decision_id=decision.id, name=c["name"], weight=float(c.get("weight", 3.0)))
            self.db.add(crit)
            crit_objs.append(crit)
        await self.db.flush()

        opt_objs = []
        for o_name in default_options:
            opt = DecisionOption(decision_id=decision.id, name=o_name)
            self.db.add(opt)
            opt_objs.append(opt)
        await self.db.flush()

        # Seed scores
        for opt in opt_objs:
            tot = 0.0
            tot_w = 0.0
            for crit in crit_objs:
                base_score = 8.5 if "AI Startup" in opt.name and "Growth" in crit.name else 7.5
                sc = DecisionScore(
                    option_id=opt.id,
                    criterion_id=crit.id,
                    score=base_score,
                    rationale=f"High score on {crit.name} based on multi-factor market analysis."
                )
                self.db.add(sc)
                tot += base_score * crit.weight
                tot_w += crit.weight
            opt.total_score = round(tot / tot_w, 2) if tot_w > 0 else 0.0

        await self.db.commit()
        return await self.get_by_id(decision.id, user_id)

    async def update_score(
        self,
        decision_id: UUID,
        option_id: UUID,
        criterion_id: UUID,
        score: float,
        rationale: Optional[str] = None
    ) -> Optional[Decision]:
        result = await self.db.execute(
            select(DecisionScore).where(
                DecisionScore.option_id == option_id,
                DecisionScore.criterion_id == criterion_id
            )
        )
        ds = result.scalar_one_or_none()
        if ds:
            ds.score = score
            if rationale:
                ds.rationale = rationale
        else:
            ds = DecisionScore(option_id=option_id, criterion_id=criterion_id, score=score, rationale=rationale)
            self.db.add(ds)
        await self.db.commit()

        # Re-compute total scores
        dec = await self.get_by_id(decision_id)
        if dec:
            crit_map = {c.id: c.weight for c in dec.criteria}
            for opt in dec.options:
                opt_res = await self.db.execute(select(DecisionScore).where(DecisionScore.option_id == opt.id))
                scores = list(opt_res.scalars().all())
                tot = sum(s.score * crit_map.get(s.criterion_id, 1.0) for s in scores)
                w_tot = sum(crit_map.get(s.criterion_id, 1.0) for s in scores)
                opt.total_score = round(tot / w_tot, 2) if w_tot > 0 else 0.0
            await self.db.commit()
        return await self.get_by_id(decision_id)
