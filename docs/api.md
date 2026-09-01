# Think2Act API Specification (`/api/v1`)

## Authentication (`/api/v1/auth`)
- `POST /register`: Create account, hashes password, returns user object and JWT bearer token.
- `POST /login`: Verify credentials and returns JWT bearer token.
- `GET /me`: Returns current user identity.
- `POST /logout`: Invalidates client session.

## Users (`/api/v1/users`)
- `GET /me`: Full profile details (bio, education, user_mode, timezone, career goal).
- `PATCH /me`: Update profile parameters.

## Dashboard (`/api/v1/dashboard`)
- `GET /`: Aggregate dashboard endpoint returning tasks summary, daily productivity score, active next action, today's tasks, active goals, and AI suggestion in a single unified round-trip.

## Goals (`/api/v1/goals`)
- `GET /`: List user goals.
- `POST /`: Create goal.
- `GET /{id}`: Fetch goal by ID.
- `PATCH /{id}`: Update goal.
- `DELETE /{id}`: Delete goal.

## Tasks (`/api/v1/tasks`)
- `GET /`: List tasks with query filters (`status`, `priority`, `goal_id`, `category`).
- `POST /`: Create task.
- `GET /{id}`: Get task details.
- `PATCH /{id}`: Update task.
- `POST /{id}/complete`: Mark task completed and record UTC timestamp.
- `DELETE /{id}`: Delete task.
