import pytest

@pytest.mark.asyncio
async def test_register_and_login(client):
    # 1. Register User
    reg_payload = {
        "name": "Test Engineer",
        "email": "test@think2act.ai",
        "password": "Password123!"
    }
    reg_resp = await client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_resp.status_code == 201
    data = reg_resp.json()
    assert data["user"]["email"] == "test@think2act.ai"
    assert "access_token" in data["token"]

    token = data["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get Me
    me_resp = await client.get("/api/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["name"] == "Test Engineer"

    # 3. Login
    login_payload = {
        "email": "test@think2act.ai",
        "password": "Password123!"
    }
    login_resp = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()["token"]

    # 4. Duplicate registration check
    dup_resp = await client.post("/api/v1/auth/register", json=reg_payload)
    assert dup_resp.status_code == 409
