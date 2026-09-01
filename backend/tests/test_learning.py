import pytest

@pytest.mark.asyncio
async def test_skill_gap_and_learning_roadmap_loop(client):
    # 1. Register user
    user = await client.post("/api/v1/auth/register", json={
        "name": "Learning Engineer",
        "email": "learner@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. List Roles
    roles_resp = await client.get("/api/v1/roles", headers=headers)
    assert roles_resp.status_code == 200
    roles = roles_resp.json()
    assert len(roles) > 0
    role_id = roles[0]["id"]

    # 3. Compute on-demand skill gaps
    gap_resp = await client.get(f"/api/v1/skills/gaps?role_id={role_id}", headers=headers)
    assert gap_resp.status_code == 200
    gap_report = gap_resp.json()
    assert "gaps" in gap_report
    assert "overall_readiness" in gap_report

    # 4. Generate structured learning roadmap from gaps
    roadmap_resp = await client.post("/api/v1/learning/paths/generate", headers=headers, json={
        "role_id": role_id,
        "title": "Backend Mastery Fast-Track"
    })
    assert roadmap_resp.status_code == 201
    roadmap = roadmap_resp.json()
    assert len(roadmap["items"]) > 0
    item_id = roadmap["items"][0]["id"]

    # 5. Convert learning item to actionable Task (closes the execution loop!)
    convert_resp = await client.post(f"/api/v1/learning/items/{item_id}/convert-to-task", headers=headers)
    assert convert_resp.status_code == 200
    task_created = convert_resp.json()["task"]
    assert task_created["category"] == "Learning"
    assert task_created["status"] == "TODO"

    # 6. Complete learning item and verify evidence is recorded
    comp_item_resp = await client.post(f"/api/v1/learning/items/{item_id}/complete", headers=headers)
    assert comp_item_resp.status_code == 200
    assert comp_item_resp.json()["status"] == "COMPLETED"
