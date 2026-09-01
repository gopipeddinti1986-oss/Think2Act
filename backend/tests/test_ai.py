import pytest

@pytest.mark.asyncio
async def test_ai_coach_conversation_and_action_confirmation(client):
    # 1. Register user
    user = await client.post("/api/v1/auth/register", json={
        "name": "AI User",
        "email": "aiuser@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Chat with AI Coach requesting plan
    chat_resp = await client.post("/api/v1/ai/chat", headers=headers, json={
        "message": "What should I do today? Please help me plan my learning."
    })
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()
    assert "conversation_id" in chat_data
    assert len(chat_data["message"]["content"]) > 0
    assert len(chat_data["proposed_actions"]) > 0

    action = chat_data["proposed_actions"][0]
    action_id = action["id"]
    assert action["status"] == "PENDING"
    assert action["requires_confirmation"] is True

    # 3. User Confirms the Proposed Action (Guardrail verification)
    confirm_resp = await client.post(f"/api/v1/ai/actions/{action_id}/confirm", headers=headers)
    assert confirm_resp.status_code == 200
    confirmed_action = confirm_resp.json()
    assert confirmed_action["status"] == "EXECUTED"
    assert confirmed_action["confirmed_at"] is not None

    # 4. Verify that action actually executed in the database (e.g. task was created)
    tasks_resp = await client.get("/api/v1/tasks", headers=headers)
    assert tasks_resp.status_code == 200
    tasks = tasks_resp.json()
    assert len(tasks) > 0
