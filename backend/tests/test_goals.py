import pytest

@pytest.mark.asyncio
async def test_goal_crud_and_isolation(client):
    # Register User A
    user_a = await client.post("/api/v1/auth/register", json={
        "name": "User A",
        "email": "usera@think2act.ai",
        "password": "Password123!"
    })
    token_a = user_a.json()["token"]["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Register User B
    user_b = await client.post("/api/v1/auth/register", json={
        "name": "User B",
        "email": "userb@think2act.ai",
        "password": "Password123!"
    })
    token_b = user_b.json()["token"]["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A creates a Goal
    create_resp = await client.post("/api/v1/goals", headers=headers_a, json={
        "title": "Become Full Stack Architect",
        "description": "Master React, FastAPI and Cloud Infrastructure",
        "priority": "HIGH",
        "status": "IN_PROGRESS"
    })
    assert create_resp.status_code == 201
    goal_id = create_resp.json()["id"]

    # User A lists Goals
    list_resp = await client.get("/api/v1/goals", headers=headers_a)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
    assert list_resp.json()[0]["title"] == "Become Full Stack Architect"

    # User B should NOT see User A's goal
    list_b_resp = await client.get("/api/v1/goals", headers=headers_b)
    assert list_b_resp.status_code == 200
    assert len(list_b_resp.json()) == 0

    # User B cannot access or modify User A's goal
    get_b_resp = await client.get(f"/api/v1/goals/{goal_id}", headers=headers_b)
    assert get_b_resp.status_code == 404

    # User A updates goal
    patch_resp = await client.patch(f"/api/v1/goals/{goal_id}", headers=headers_a, json={
        "status": "COMPLETED"
    })
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "COMPLETED"
