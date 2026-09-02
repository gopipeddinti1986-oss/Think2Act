import pytest

@pytest.mark.asyncio
async def test_resume_ats_and_suggestions_flow(client):
    user = await client.post("/api/v1/auth/register", json={
        "name": "Resume User",
        "email": "resume@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. List / auto-create initial resume
    resumes_resp = await client.get("/api/v1/resume", headers=headers)
    assert resumes_resp.status_code == 200
    resumes = resumes_resp.json()
    assert len(resumes) >= 1
    resume_id = resumes[0]["id"]
    initial_score = resumes[0]["ats_score"]
    assert "suggestions" in resumes[0]
    assert len(resumes[0]["suggestions"]) >= 1

    sugg_id = resumes[0]["suggestions"][0]["id"]

    # 2. Apply ATS suggestion
    apply_resp = await client.post(f"/api/v1/resume/{resume_id}/suggestions/{sugg_id}/apply", headers=headers, json={
        "apply": True
    })
    assert apply_resp.status_code == 200
    updated_score = apply_resp.json()["ats_score"]
    assert updated_score >= initial_score
