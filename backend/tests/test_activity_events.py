import pytest

@pytest.mark.asyncio
async def test_activity_events_logging_and_retrieval(client):
    # 1. Register User (Triggers USER_REGISTERED event)
    reg_resp = await client.post("/api/v1/auth/register", json={
        "name": "Activity Tester",
        "email": "activity@think2act.ai",
        "password": "Password123!"
    })
    assert reg_resp.status_code == 201
    token = reg_resp.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Login User (Triggers USER_LOGGED_IN event)
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "activity@think2act.ai",
        "password": "Password123!"
    })
    assert login_resp.status_code == 200

    # 3. Retrieve Activity Events
    activity_resp = await client.get("/api/v1/users/activity", headers=headers)
    assert activity_resp.status_code == 200
    events = activity_resp.json()
    assert len(events) >= 2

    event_types = [e["event_type"] for e in events]
    assert "USER_REGISTERED" in event_types
    assert "USER_LOGGED_IN" in event_types

    # 4. Filter by Event Type
    filtered_resp = await client.get("/api/v1/users/activity?event_type=USER_REGISTERED", headers=headers)
    assert filtered_resp.status_code == 200
    filtered_events = filtered_resp.json()
    assert len(filtered_events) == 1
    assert filtered_events[0]["event_type"] == "USER_REGISTERED"
