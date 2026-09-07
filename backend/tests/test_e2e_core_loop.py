import pytest
from datetime import datetime, timezone, timedelta
from app.models.entities import TaskStatus, PriorityEnum

@pytest.mark.asyncio
async def test_full_think2act_core_execution_loop(client):
    # 0. Step 0: Register User for Isolated Execution Context
    user = await client.post("/api/v1/auth/register", json={
        "name": "Full Loop User",
        "email": "fullloop@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    # 1. Step 1: Create Strategic Goal
    goal_res = await client.post(
        "/api/v1/goals",
        headers=auth_headers,
        json={
            "title": "Master Backend Engineering",
            "description": "Targeting Senior Python / FastAPI roles",
            "target_date": (datetime.now(timezone.utc) + timedelta(days=90)).strftime("%Y-%m-%d"),
            "priority": "HIGH"
        }
    )
    assert goal_res.status_code == 201
    goal_id = goal_res.json()["id"]

    # 2. Step 2: Create Executable Task Linked to Goal
    task_res = await client.post(
        "/api/v1/tasks",
        headers=auth_headers,
        json={
            "goal_id": goal_id,
            "title": "Implement PostgreSQL Connection Pooling",
            "priority": "HIGH",
            "estimated_duration_minutes": 45
        }
    )
    assert task_res.status_code == 201
    task_id = task_res.json()["id"]

    # 3. Step 3: Request Planner Schedule Suggestions
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=4)
    planner_res = await client.post(
        "/api/v1/planner/suggestions",
        params={
            "work_start": start_time.isoformat(),
            "work_end": end_time.isoformat()
        },
        headers=auth_headers
    )
    assert planner_res.status_code == 200
    suggestions = planner_res.json()["slots"]
    assert len(suggestions) >= 1
    assert suggestions[0]["task_id"] == task_id

    # 4. Step 4: Confirm Schedule Slot
    confirm_res = await client.post(
        "/api/v1/planner/confirm",
        headers=auth_headers,
        json={"confirmed_slots": suggestions}
    )
    assert confirm_res.status_code == 200

    # 5. Step 5: Execute Task and Log Actual Duration
    complete_res = await client.post(
        f"/api/v1/tasks/{task_id}/complete",
        headers=auth_headers,
        json={"actual_duration_minutes": 50}
    )
    assert complete_res.status_code == 200
    assert complete_res.json()["status"] == TaskStatus.COMPLETED

    # 6. Step 6: Verify Action-Centric Dashboard Reflects Execution Data
    dash_res = await client.get("/api/v1/dashboard/summary", headers=auth_headers)
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["today_execution"]["tasks_completed"] == 1
    assert dash_data["today_execution"]["focus_minutes"] == 50

    # 7. Step 7: Verify AI Coach Reads New Execution State Snapshot
    ai_res = await client.post(
        "/api/v1/ai/chat",
        headers=auth_headers,
        json={"message": "What have I accomplished today?"}
    )
    assert ai_res.status_code == 200
    assert "50" in ai_res.json()["reply"] or "1" in ai_res.json()["reply"]