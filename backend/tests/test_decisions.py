import pytest

@pytest.mark.asyncio
async def test_decision_simulator_flow(client):
    user = await client.post("/api/v1/auth/register", json={
        "name": "Decision Maker",
        "email": "decide@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Decision
    dec_resp = await client.post("/api/v1/decisions", headers=headers, json={
        "title": "Choosing Tech Stack for AI Agent System",
        "description": "Evaluate FastAPI vs Go for low-latency agent streaming",
        "category": "TECHNICAL",
        "options": ["FastAPI (Python)", "Go / Fiber"],
        "criteria": [
            {"name": "Ecosystem & AI Tooling", "weight": 5.0},
            {"name": "Raw Concurrency Performance", "weight": 4.0}
        ]
    })
    assert dec_resp.status_code == 201
    dec = dec_resp.json()
    assert len(dec["options"]) == 2
    assert len(dec["criteria"]) == 2
    option_id = dec["options"][0]["id"]
    criterion_id = dec["criteria"][0]["id"]

    # 2. Update Option Score
    score_resp = await client.post(f"/api/v1/decisions/{dec['id']}/score", headers=headers, json={
        "option_id": option_id,
        "criterion_id": criterion_id,
        "score": 9.5,
        "rationale": "Unrivaled Python GenAI SDK integration ecosystem."
    })
    assert score_resp.status_code == 200
    updated_dec = score_resp.json()
    assert updated_dec["options"][0]["total_score"] > 0
