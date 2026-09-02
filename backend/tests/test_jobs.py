import pytest

@pytest.mark.asyncio
async def test_job_matching_and_applications_flow(client):
    # Register user
    user = await client.post("/api/v1/auth/register", json={
        "name": "Job Candidate",
        "email": "candidate@think2act.ai",
        "password": "Password123!"
    })
    token = user.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. List Matched Jobs
    jobs_resp = await client.get("/api/v1/jobs", headers=headers)
    assert jobs_resp.status_code == 200
    jobs = jobs_resp.json()
    assert len(jobs) >= 1
    job_id = jobs[0]["id"]
    assert "match_percentage" in jobs[0]

    # 2. Create Application
    app_resp = await client.post("/api/v1/jobs/applications", headers=headers, json={
        "job_id": job_id,
        "status": "SAVED",
        "notes": "Strong match for my FastAPI skill stack"
    })
    assert app_resp.status_code == 201
    app_id = app_resp.json()["id"]
    assert app_resp.json()["status"] == "SAVED"

    # 3. Update Application Status to APPLIED
    update_resp = await client.patch(f"/api/v1/jobs/applications/{app_id}/status", headers=headers, json={
        "status": "APPLIED"
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "APPLIED"

    # 4. List Applications
    list_apps = await client.get("/api/v1/jobs/applications", headers=headers)
    assert list_apps.status_code == 200
    assert len(list_apps.json()) == 1
