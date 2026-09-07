import asyncio
import httpx
import json
import sys
import uuid
from app.main import app

BASE_URL = "http://test/api/v1"

def print_step(title, res):
    print(f"\n==================== {title} ====================")
    print(f"Status Code: {res.status_code}")
    try:
        print("Response Body:\n" + json.dumps(res.json(), indent=2))
    except Exception:
        print(f"Response Body (raw):\n{res.text}")

async def main():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=BASE_URL, timeout=30.0) as client:
        # 1. Health check
        res = await client.get("/health")
        print_step("1. GET /api/v1/health", res)
        assert res.status_code == 200

        # 2. Register
        email = f"testuser_{uuid.uuid4().hex[:6]}@think2act.ai"
        register_payload = {
            "name": "Alex Mercer",
            "email": email,
            "password": "SecurePassword123!"
        }
        res = await client.post("/auth/register", json=register_payload)
        print_step("2. POST /api/v1/auth/register", res)
        assert res.status_code == 201
        data = res.json()
        token = data["token"]["access_token"]
        user_id = data["user"]["id"]

        headers = {"Authorization": f"Bearer {token}"}

        # 3. Login
        login_payload = {
            "email": email,
            "password": "SecurePassword123!"
        }
        res = await client.post("/auth/login", json=login_payload)
        print_step("3. POST /api/v1/auth/login", res)
        assert res.status_code == 200

        # 4. Get Current User (GET /auth/me)
        res = await client.get("/auth/me", headers=headers)
        print_step("4. GET /api/v1/auth/me", res)
        assert res.status_code == 200

        # 5. Logout (POST /auth/logout)
        res = await client.post("/auth/logout", headers=headers)
        print_step("5. POST /api/v1/auth/logout", res)
        assert res.status_code == 200

        # 6. Goals CRUD
        # 6a. Create Goal (POST /goals)
        goal_payload = {
            "title": "Master Distributed Systems & High-Throughput APIs",
            "description": "Design event-driven architectures with Kafka and Redis",
            "category": "Engineering",
            "priority": "HIGH",
            "target_date": "2026-12-31"
        }
        res = await client.post("/goals", headers=headers, json=goal_payload)
        print_step("6a. POST /api/v1/goals", res)
        assert res.status_code == 201
        goal_id = res.json()["id"]

        # 6b. Get Goals List (GET /goals)
        res = await client.get("/goals", headers=headers)
        print_step("6b. GET /api/v1/goals", res)
        assert res.status_code == 200
        assert len(res.json()) >= 1

        # 6c. Get Goal Details (GET /goals/{id})
        res = await client.get(f"/goals/{goal_id}", headers=headers)
        print_step("6c. GET /api/v1/goals/{id}", res)
        assert res.status_code == 200

        # 6d. Update Goal (PUT /goals/{id})
        res = await client.put(f"/goals/{goal_id}", headers=headers, json={"status": "IN_PROGRESS", "priority": "HIGH"})
        print_step("6d. PUT /api/v1/goals/{id}", res)
        assert res.status_code == 200

        # 7. Tasks CRUD
        # 7a. Create Task (POST /tasks)
        task_payload = {
            "goal_id": goal_id,
            "title": "Benchmarking SQLite vs PostgreSQL concurrency in Python 3.14",
            "description": "Measure connection pool saturation and write contention under heavy load",
            "priority": "HIGH",
            "estimated_duration_minutes": 45,
            "category": "Benchmarking"
        }
        res = await client.post("/tasks", headers=headers, json=task_payload)
        print_step("7a. POST /api/v1/tasks", res)
        assert res.status_code == 201
        task_id = res.json()["id"]

        # 7b. Get Tasks List (GET /tasks)
        res = await client.get("/tasks", headers=headers)
        print_step("7b. GET /api/v1/tasks", res)
        assert res.status_code == 200
        assert len(res.json()) >= 1

        # 7c. Get Task Details (GET /tasks/{id})
        res = await client.get(f"/tasks/{task_id}", headers=headers)
        print_step("7c. GET /api/v1/tasks/{id}", res)
        assert res.status_code == 200

        # 7d. Update Task (PUT /tasks/{id})
        res = await client.put(f"/tasks/{task_id}", headers=headers, json={"priority": "URGENT"})
        print_step("7d. PUT /api/v1/tasks/{id}", res)
        assert res.status_code == 200

        # 8. Complete Task (POST /tasks/{id}/complete)
        complete_payload = {
            "actual_duration_minutes": 50
        }
        res = await client.post(f"/tasks/{task_id}/complete", headers=headers, json=complete_payload)
        print_step("8. POST /api/v1/tasks/{id}/complete", res)
        assert res.status_code == 200

        # 9. Dashboard State after completion
        res = await client.get("/dashboard/summary", headers=headers)
        print_step("9. GET /api/v1/dashboard/summary (After Task Completion)", res)
        assert res.status_code == 200

        # 10. Delete Task (DELETE /tasks/{id})
        res_t2 = await client.post("/tasks", headers=headers, json={"title": "Temporary scratch task", "priority": "LOW"})
        t2_id = res_t2.json()["id"]
        res_del_task = await client.delete(f"/tasks/{t2_id}", headers=headers)
        print_step("10. DELETE /api/v1/tasks/{id}", res_del_task)
        assert res_del_task.status_code == 200

        # 11. Delete Goal (DELETE /goals/{id})
        res_g2 = await client.post("/goals", headers=headers, json={"title": "Temporary goal to delete", "priority": "LOW"})
        g2_id = res_g2.json()["id"]
        res_del_goal = await client.delete(f"/goals/{g2_id}", headers=headers)
        print_step("11. DELETE /api/v1/goals/{id}", res_del_goal)
        assert res_del_goal.status_code == 200

        print("\nALL API ENDPOINTS & FLOWS VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())
