import pytest

@pytest.mark.asyncio
async def test_focus_session_flow(client):
    # Register user
    user = await client.post("/api/v1/auth/register", json={
        "name": "Focus User",
        "email": "focus@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create task
    task = await client.post("/api/v1/tasks", headers=headers, json={
        "title": "Solve Hard DP Problem",
        "estimated_minutes": 45
    })
    task_id = task.json()["id"]

    # Start focus session
    start_resp = await client.post("/api/v1/focus/sessions", headers=headers, json={"task_id": task_id})
    assert start_resp.status_code == 201
    session_id = start_resp.json()["id"]

    # Check active session
    active_resp = await client.get("/api/v1/focus/active", headers=headers)
    assert active_resp.status_code == 200
    assert active_resp.json()["id"] == session_id

    # Finish focus session with 40m productive, 5m distracted
    finish_resp = await client.post(f"/api/v1/focus/sessions/{session_id}/finish", headers=headers, json={
        "productive_seconds": 2400,
        "distracted_seconds": 300,
        "mark_task_completed": True
    })
    assert finish_resp.status_code == 200
    finished_session = finish_resp.json()
    assert finished_session["status"] == "COMPLETED"
    assert finished_session["productive_seconds"] == 2400

    # Verify task was completed
    task_check = await client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert task_check.json()["status"] == "COMPLETED"
    assert task_check.json()["actual_minutes"] == 40

    # Verify today summary
    summary_resp = await client.get("/api/v1/focus/today", headers=headers)
    assert summary_resp.status_code == 200
    assert summary_resp.json()["total_sessions"] == 1
    assert summary_resp.json()["focus_seconds"] == 2400
