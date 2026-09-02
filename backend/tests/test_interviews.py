import pytest

@pytest.mark.asyncio
async def test_interview_session_and_grading_flow(client):
    user = await client.post("/api/v1/auth/register", json={
        "name": "Interview User",
        "email": "interview@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Start or list interview session
    session_resp = await client.post("/api/v1/interviews", headers=headers, json={
        "role_title": "Senior Backend Architect",
        "session_type": "TECHNICAL"
    })
    assert session_resp.status_code == 201
    session = session_resp.json()
    session_id = session["id"]
    assert len(session["questions"]) >= 1

    question_id = session["questions"][0]["id"]

    # 2. Submit Answer
    answer_resp = await client.post(f"/api/v1/interviews/{session_id}/answer", headers=headers, json={
        "question_id": question_id,
        "answer": "Asyncio is single-threaded event-loop based concurrency for I/O; CPU tasks should use worker processes."
    })
    assert answer_resp.status_code == 200
    q_data = answer_resp.json()
    assert q_data["score"] > 0
    assert "rubric_scores" in q_data
    assert "ai_feedback" in q_data
