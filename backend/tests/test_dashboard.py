import pytest

@pytest.mark.asyncio
async def test_dashboard_aggregate_endpoint(client):
    # Register user
    user = await client.post("/api/v1/auth/register", json={
        "name": "Jordan",
        "email": "jordan@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Initial Dashboard (Empty state)
    d_empty = await client.get("/api/v1/dashboard", headers=headers)
    assert d_empty.status_code == 200
    empty_data = d_empty.json()
    assert empty_data["tasks_summary"]["total"] == 0
    assert empty_data["ai_suggestion"]["action_type"] == "CREATE_GOAL"

    # Create Goal & Tasks
    goal = await client.post("/api/v1/goals", headers=headers, json={"title": "Backend Mastery"})
    goal_id = goal.json()["id"]

    t1 = await client.post("/api/v1/tasks", headers=headers, json={
        "title": "Build Auth API",
        "priority": "HIGH",
        "goal_id": goal_id,
        "estimated_minutes": 45
    })
    t2 = await client.post("/api/v1/tasks", headers=headers, json={
        "title": "Write Unit Tests",
        "priority": "MEDIUM",
        "goal_id": goal_id,
        "estimated_minutes": 30
    })

    # Dashboard with tasks
    d_active = await client.get("/api/v1/dashboard", headers=headers)
    assert d_active.status_code == 200
    active_data = d_active.json()
    assert active_data["tasks_summary"]["total"] == 2
    assert active_data["tasks_summary"]["pending"] == 2
    assert active_data["next_action"]["title"] == "Build Auth API"

    # Complete highest priority task
    await client.post(f"/api/v1/tasks/{t1.json()['id']}/complete", headers=headers)

    # Dashboard reflects completion
    d_updated = await client.get("/api/v1/dashboard", headers=headers)
    assert d_updated.status_code == 200
    updated_data = d_updated.json()
    assert updated_data["tasks_summary"]["completed"] == 1
    assert updated_data["tasks_summary"]["completion_rate"] == 50
    assert updated_data["next_action"]["title"] == "Write Unit Tests"
