# Think2Act Database Schema & Migration Guide

## Migration Lifecycle & Architecture
Think2Act strictly enforces database evolution through sequential **Alembic migrations**.
The application never relies on destructive `Base.metadata.create_all()` or runtime `DROP` statements in production or standard execution.

### Migration Revisions (001 to 012)
- **`001_initial_schema`**: Core entities (`users`, `user_profiles`, `goals`, `tasks`).
- **`002_milestone2_execution_loop`**: Timeboxing & execution (`planner_entries`, `focus_sessions`, `productivity_metrics`).
- **`003_milestone3_skills`**: Skill acquisition & evidence (`skills`, `user_skills`, `evidence`, `skill_history`, `task_skills`).
- **`004_milestone4_learning_intelligence`**: Career pathways (`roles`, `role_skills`, `learning_resources`, `learning_paths`).
- **`005_milestone5_ai_coach`**: Contextual intelligence (`ai_conversations`, `ai_messages`, `ai_actions`).
- **`006_milestone6_jobs`**: Job matching & applications (`jobs`, `job_skills`, `job_applications`, `application_events`).
- **`007_milestone7_resume`**: ATS Resume engine (`resume_profiles`, `resume_sections`, `tailored_resumes`).
- **`008_milestone8_interviews`**: AI Mock interview simulator (`interview_sessions`, `interview_questions`, `interview_feedback`).
- **`009_milestone9_decisions`**: Decision simulator & trade-offs (`decisions`).
- **`010_settings_fields`**: User preferences schema additions.
- **`011_user_availability_and_activity`**: Work availability, notification preferences, and system-wide activity log (`activity_events`).
- **`012_task_source`**: Task origin tracing (`source` column on `tasks`).

---

## Complete Table Directory

### 1. Identity & Profile
- `users`: Core authentication identity, password hash, status.
- `user_profiles`: Extended profile, bio, career goals, availability (`work_start_time`, `work_end_time`, `preferred_sprint_minutes`), `experience_level`, notification preferences.
- `activity_events`: Audit log of user actions (`USER_REGISTERED`, `USER_LOGGED_IN`, `TASK_COMPLETED`, etc.).

### 2. Goals & Task Execution
- `goals`: Strategic objectives with deadlines, priority, and progress tracking.
- `tasks`: Executable actions linked to goals, with estimates, actuals, category, and source.
- `planner_entries`: Scheduled calendar blocks for tasks.
- `focus_sessions`: Pomodoro / deep work timer sessions with distraction logging.
- `productivity_metrics`: Daily/weekly aggregated productivity and velocity metrics.

### 3. Skills & Evidence System
- `skills`: Global skill catalog with category taxonomy.
- `user_skills`: User's current proficiency score (0–100) and confidence.
- `evidence`: Proof items tied to task completions and external achievements.
- `skill_history`: Historical progression snapshots over time.
- `task_skills`: Many-to-many relationship linking tasks to the skills they develop.

### 4. Learning Intelligence & Career
- `roles`: Target job roles / career tracks.
- `role_skills`: Skills required for specific roles with required proficiency levels.
- `learning_resources`: Courses, tutorials, and documentation items.
- `learning_paths`: Guided roadmaps mapped to close identified skill gaps.

### 5. Jobs & Application Pipeline
- `jobs`: Tracked job postings with parsed requirements.
- `job_skills`: Required and bonus skills for specific job openings.
- `job_applications`: Kanban tracking for applications (Saved, Applied, Interviewing, Offered, Rejected).
- `application_events`: Status transitions and notes for applications.

### 6. Resume & ATS Engine
- `resume_profiles`: Master resume content per user.
- `resume_sections`: Work experience, education, projects, certifications.
- `tailored_resumes`: Role-tailored versions with ATS match scores and keyword suggestions.

### 7. Interview Simulator
- `interview_sessions`: Mock interview practices for specific roles or jobs.
- `interview_questions`: Questions presented with difficulty and category.
- `interview_feedback`: Rubric-based scoring (communication, technical, structure) and constructive guidance.

### 8. Decision Simulator
- `decisions`: Strategic choices modeled with pros, cons, risk analysis, and outcome tracking.

### 9. AI Coach
- `ai_conversations`: Multi-turn conversational sessions with the AI Coach.
- `ai_messages`: Contextual messages with system, user, and assistant roles.
- `ai_actions`: Proposed actions requiring explicit user confirmation before mutation.

---

## Running Migrations
To upgrade the database to the latest schema:
```bash
cd backend
alembic upgrade head
```

To verify migration state against a clean database without `create_all()`:
```bash
pytest tests/test_migrations.py -v
```
