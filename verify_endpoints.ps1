
# Full endpoint verification script
$base = "http://127.0.0.1:8000/api/v1"
$errors = @()

function Show-Response($label, $resp, $code) {
    Write-Output "`n=== $label === STATUS: $code ==="
    Write-Output ($resp | ConvertTo-Json -Depth 5 -Compress)
}

# ── STEP 1: Health ──────────────────────────────────────────────────────
try {
    $r = Invoke-WebRequest -Uri "$base/health" -Method GET -ErrorAction Stop
    Show-Response "GET /health" ($r.Content | ConvertFrom-Json) $r.StatusCode
} catch { $errors += "Health: $_" }

# ── STEP 2: Register ────────────────────────────────────────────────────
$rand = Get-Random -Min 10000 -Max 99999
$email = "verify_$rand@think2act.ai"
try {
    $r = Invoke-WebRequest -Uri "$base/auth/register" -Method POST -ContentType "application/json" -Body (@{
        name="Verify User"; email=$email; password="Verify123!"
    } | ConvertTo-Json) -ErrorAction Stop
    $reg = $r.Content | ConvertFrom-Json
    Show-Response "POST /auth/register" $reg $r.StatusCode
    $token = $reg.token.access_token
} catch { $errors += "Register: $_"; $token = $null }

if (-not $token) { Write-Output "FATAL: No token, aborting"; exit 1 }
$h = @{ Authorization = "Bearer $token" }

# ── STEP 3: Auth/me ─────────────────────────────────────────────────────
try {
    $r = Invoke-WebRequest -Uri "$base/auth/me" -Method GET -Headers $h -ErrorAction Stop
    Show-Response "GET /auth/me" ($r.Content | ConvertFrom-Json) $r.StatusCode
} catch { $errors += "Me: $_" }

# ── STEP 4: Dashboard ───────────────────────────────────────────────────
try {
    $r = Invoke-WebRequest -Uri "$base/dashboard" -Method GET -Headers $h -ErrorAction Stop
    Show-Response "GET /dashboard" ($r.Content | ConvertFrom-Json) $r.StatusCode
} catch { $errors += "Dashboard: $_" }

# ── STEP 5: Create Goal ─────────────────────────────────────────────────
try {
    $r = Invoke-WebRequest -Uri "$base/goals" -Method POST -Headers $h -ContentType "application/json" -Body (@{
        title="Land Senior Engineer Role"; description="Get hired at FAANG-tier"; category="Career"; priority="HIGH"
    } | ConvertTo-Json) -ErrorAction Stop
    $goal = $r.Content | ConvertFrom-Json
    Show-Response "POST /goals" $goal $r.StatusCode
    $goalId = $goal.id
} catch { $errors += "Create Goal: $_"; $goalId = $null }

# ── STEP 6: GET /goals ──────────────────────────────────────────────────
try {
    $r = Invoke-WebRequest -Uri "$base/goals" -Method GET -Headers $h -ErrorAction Stop
    Show-Response "GET /goals" ($r.Content | ConvertFrom-Json) $r.StatusCode
} catch { $errors += "List Goals: $_" }

# ── STEP 7: Create Task ─────────────────────────────────────────────────
try {
    $body = @{ title="Build Redis Rate Limiter"; description="Implement sliding window log"; priority="HIGH"; status="TODO"; estimated_minutes=90; category="Backend Engineering" }
    if ($goalId) { $body.goal_id = $goalId }
    $r = Invoke-WebRequest -Uri "$base/tasks" -Method POST -Headers $h -ContentType "application/json" -Body ($body | ConvertTo-Json) -ErrorAction Stop
    $task = $r.Content | ConvertFrom-Json
    Show-Response "POST /tasks" $task $r.StatusCode
    $taskId = $task.id
} catch { $errors += "Create Task: $_"; $taskId = $null }

# ── STEP 8: GET /tasks ──────────────────────────────────────────────────
try {
    $r = Invoke-WebRequest -Uri "$base/tasks" -Method GET -Headers $h -ErrorAction Stop
    $tasklist = $r.Content | ConvertFrom-Json
    Show-Response "GET /tasks (count=$($tasklist.Count))" $tasklist[0] $r.StatusCode
} catch { $errors += "List Tasks: $_" }

# ── STEP 9: GET /tasks/:id ──────────────────────────────────────────────
if ($taskId) {
    try {
        $r = Invoke-WebRequest -Uri "$base/tasks/$taskId" -Method GET -Headers $h -ErrorAction Stop
        Show-Response "GET /tasks/$taskId" ($r.Content | ConvertFrom-Json) $r.StatusCode
    } catch { $errors += "Get Task: $_" }
}

# ── STEP 10: PATCH /tasks/:id ───────────────────────────────────────────
if ($taskId) {
    try {
        $r = Invoke-WebRequest -Uri "$base/tasks/$taskId" -Method PATCH -Headers $h -ContentType "application/json" -Body (@{ priority="URGENT"; description="Updated desc" } | ConvertTo-Json) -ErrorAction Stop
        Show-Response "PATCH /tasks/$taskId" ($r.Content | ConvertFrom-Json) $r.StatusCode
    } catch { $errors += "Update Task: $_" }
}

# ── STEP 11: POST /tasks/:id/complete ───────────────────────────────────
if ($taskId) {
    try {
        $r = Invoke-WebRequest -Uri "$base/tasks/$taskId/complete" -Method POST -Headers $h -ContentType "application/json" -Body "{}" -ErrorAction Stop
        Show-Response "POST /tasks/$taskId/complete" ($r.Content | ConvertFrom-Json) $r.StatusCode
    } catch { $errors += "Complete Task: $_" }
}

# ── STEP 12: Dashboard after completion ─────────────────────────────────
try {
    $r = Invoke-WebRequest -Uri "$base/dashboard" -Method GET -Headers $h -ErrorAction Stop
    Show-Response "GET /dashboard (post-completion)" ($r.Content | ConvertFrom-Json) $r.StatusCode
} catch { $errors += "Dashboard2: $_" }

# ── STEP 13: Logout ─────────────────────────────────────────────────────
try {
    $r = Invoke-WebRequest -Uri "$base/auth/logout" -Method POST -Headers $h -ContentType "application/json" -Body "{}" -ErrorAction Stop
    Show-Response "POST /auth/logout" ($r.Content | ConvertFrom-Json) $r.StatusCode
} catch { $errors += "Logout: $_" }

# ── SUMMARY ─────────────────────────────────────────────────────────────
Write-Output "`n========== ERRORS ($($errors.Count)) =========="
if ($errors.Count -eq 0) {
    Write-Output "NONE - all endpoints returned expected status codes"
} else {
    $errors | ForEach-Object { Write-Output "  ERROR: $_" }
}
