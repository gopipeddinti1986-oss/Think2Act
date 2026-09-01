import pytest

@pytest.mark.asyncio
async def test_evidence_based_skills_flow(client):
    # 1. Register user
    user = await client.post("/api/v1/auth/register", json={
        "name": "Skill Tester",
        "email": "skilltester@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get user skill graph (seeded)
    skills_resp = await client.get("/api/v1/skills/me", headers=headers)
    assert skills_resp.status_code == 200
    skills_data = skills_resp.json()
    assert len(skills_data) > 0
    
    python_skill = next(s for s in skills_data if "Python" in s["name"])
    skill_id = python_skill["skill_id"]

    # 3. Add Evidence for Python
    evidence_resp = await client.post("/api/v1/evidence/manual", headers=headers, json={
        "skill_id": skill_id,
        "source_type": "PROJECT",
        "strength": 25.0,
        "description": "Engineered async task queue in Python and Redis"
    })
    assert evidence_resp.status_code == 201
    assert evidence_resp.json()["strength"] == 25.0

    # 4. Check that Python skill level recalculated based on evidence
    updated_skill_resp = await client.get(f"/api/v1/skills/me/{skill_id}", headers=headers)
    assert updated_skill_resp.status_code == 200
    updated_skill = updated_skill_resp.json()
    assert updated_skill["evidence_count"] >= 1
    assert len(updated_skill["recent_evidence"]) >= 1
    assert updated_skill["level"] > 30.0
