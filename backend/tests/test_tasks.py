import pytest

@pytest.mark.asyncio
async def test_task_lifecycle_and_completion(client):
    # Register user
    user = await client.post("/api/v1/auth/register", json={
        "name": "Alex",
        "email": "alex@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Goal
    goal = await client.post("/api/v1/goals", headers=headers, json={
        "title": "Placement Preparation",
        "priority": "HIGH"
    })
    goal_id = goal.json()["id"]

    # Create Task linked to Goal
    task_resp = await client.post("/api/v1/tasks", headers=headers, json={
        "title": "Solve 5 Tree Problems",
        "description": "Binary tree traversals",
        "priority": "HIGH",
        "goal_id": goal_id,
        "estimated_minutes": 60,
        "category": "DSA"
    })
    assert task_resp.status_code == 201
    task_data = task_resp.json()
    assert task_data["status"] == "TODO"
    assert task_data["completed_at"] is None
    task_id = task_data["id"]

    # Complete Task
    complete_resp = await client.post(f"/api/v1/tasks/{task_id}/complete", headers=headers)
    assert complete_resp.status_code == 200
    completed_task = complete_resp.json()
    assert completed_task["status"] == "COMPLETED"
    assert completed_task["completed_at"] is not None
