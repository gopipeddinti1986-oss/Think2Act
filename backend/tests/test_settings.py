import pytest

@pytest.mark.asyncio
async def test_settings_endpoints(client):
    # 1. Register User
    reg_resp = await client.post("/api/v1/auth/register", json={
        "name": "Settings Tester",
        "email": "settings@think2act.ai",
        "password": "Password123!"
    })
    token = reg_resp.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get Settings
    get_res = await client.get("/api/v1/settings", headers=headers)
    assert get_res.status_code == 200
    settings_data = get_res.json()
    assert settings_data["name"] == "Settings Tester"
    assert "target_role" in settings_data

    # 3. Update Profile
    update_prof = await client.put("/api/v1/settings/profile", headers=headers, json={
        "name": "Senior Settings Tester",
        "timezone": "America/New_York",
        "bio": "Building autonomous developer tools",
        "user_mode": "employee"
    })
    assert update_prof.status_code == 200

    # 4. Update Career
    update_career = await client.put("/api/v1/settings/career", headers=headers, json={
        "target_role": "Staff Distributed Systems Engineer",
        "target_companies": ["OpenAI", "Anthropic", "Google DeepMind"],
        "career_mode": "SKILL_BUILDING"
    })
    assert update_career.status_code == 200

    # 5. Update Integrations
    update_int = await client.put("/api/v1/settings/integrations", headers=headers, json={
        "github_handle": "think2act-dev",
        "linkedin_profile_url": "https://linkedin.com/in/think2act",
        "leetcode_username": "algo_master"
    })
    assert update_int.status_code == 200

    # 6. Verify Settings Persisted
    verify_res = await client.get("/api/v1/settings", headers=headers)
    assert verify_res.status_code == 200
    updated_data = verify_res.json()
    assert updated_data["name"] == "Senior Settings Tester"
    assert updated_data["target_role"] == "Staff Distributed Systems Engineer"
    assert updated_data["github_handle"] == "think2act-dev"
    assert updated_data["user_mode"] == "employee"

    # 7. Test Availability
    update_avail = await client.put("/api/v1/settings/availability", headers=headers, json={
        "work_start_time": "08:30",
        "work_end_time": "17:30",
        "preferred_sprint_minutes": 50
    })
    assert update_avail.status_code == 200

    # 8. Test Notifications
    update_notif = await client.put("/api/v1/settings/notifications", headers=headers, json={
        "email_alerts": True,
        "daily_briefing": True
    })
    assert update_notif.status_code == 200

    # 9. Verify Availability and Notifications Persisted
    verify_res2 = await client.get("/api/v1/settings", headers=headers)
    assert verify_res2.status_code == 200
    assert verify_res2.json()["work_start_time"] == "08:30"
    assert verify_res2.json()["preferred_sprint_minutes"] == 50
    assert verify_res2.json()["notification_preferences"]["email_alerts"] is True

    # 10. Test Export Data
    export_res = await client.get("/api/v1/settings/export", headers=headers)
    assert export_res.status_code == 200
    export_data = export_res.json()
    assert export_data["user"]["name"] == "Senior Settings Tester"
    assert "goals" in export_data
    assert "tasks" in export_data

