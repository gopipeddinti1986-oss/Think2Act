import pytest
from datetime import datetime, timezone, timedelta

@pytest.mark.asyncio
async def test_planner_scheduling(client):
    # Register user
    user = await client.post("/api/v1/auth/register", json={
        "name": "Planner User",
        "email": "planner@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create task
    task = await client.post("/api/v1/tasks", headers=headers, json={
        "title": "Study Graph Algorithms",
        "priority": "HIGH",
        "estimated_minutes": 60
    })
    task_id = task.json()["id"]

    # Schedule task
    now = datetime.now(timezone.utc)
    start_at = now + timedelta(hours=1)
    end_at = start_at + timedelta(minutes=60)

    entry_resp = await client.post("/api/v1/planner", headers=headers, json={
        "task_id": task_id,
        "start_at": start_at.isoformat(),
        "end_at": end_at.isoformat(),
        "status": "SCHEDULED",
        "source": "MANUAL"
    })
    assert entry_resp.status_code == 201
    entry_data = entry_resp.json()
    assert entry_data["status"] == "SCHEDULED"

    # List planner entries
    list_resp = await client.get("/api/v1/planner", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    # Auto schedule suggestions
    auto_resp = await client.post("/api/v1/planner/auto-schedule", headers=headers)
    assert auto_resp.status_code == 200
    assert "suggestions" in auto_resp.json()
