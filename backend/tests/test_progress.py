import pytest

@pytest.mark.asyncio
async def test_progress_and_productivity_trends(client):
    # Register user
    user = await client.post("/api/v1/auth/register", json={
        "name": "Progress User",
        "email": "progress@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Query trends
    trends_resp = await client.get("/api/v1/progress/productivity?days=7", headers=headers)
    assert trends_resp.status_code == 200
    data = trends_resp.json()
    assert "history" in data
    assert len(data["history"]) == 7
    assert "estimation_accuracy_percentage" in data
