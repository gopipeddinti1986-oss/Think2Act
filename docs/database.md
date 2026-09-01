# Think2Act Database Schema Documentation

## Milestone 1 Implemented Tables

### 1. `users`
- `id` (UUID PK, default `gen_random_uuid()`)
- `email` (VARCHAR(255) UNIQUE NOT NULL)
- `password_hash` (VARCHAR(255) NOT NULL)
- `name` (VARCHAR(255) NOT NULL)
- `is_active` (BOOLEAN DEFAULT TRUE)
- `created_at` (TIMESTAMP WITH TIME ZONE)
- `updated_at` (TIMESTAMP WITH TIME ZONE)

### 2. `user_profiles`
- `id` (UUID PK)
- `user_id` (UUID FK -> users.id ON DELETE CASCADE, UNIQUE)
- `bio` (TEXT)
- `location` (VARCHAR(255))
- `organization` (VARCHAR(255))
- `education` (TEXT)
- `experience` (TEXT)
- `user_mode` (VARCHAR(50) DEFAULT 'student')
- `career_goal` (TEXT)
- `timezone` (VARCHAR(100) DEFAULT 'UTC')
- `created_at` (TIMESTAMP WITH TIME ZONE)
- `updated_at` (TIMESTAMP WITH TIME ZONE)

### 3. `goals`
- `id` (UUID PK)
- `user_id` (UUID FK -> users.id ON DELETE CASCADE)
- `title` (VARCHAR(255) NOT NULL)
- `description` (TEXT)
- `category` (VARCHAR(100))
- `priority` (VARCHAR(50) DEFAULT 'MEDIUM')
- `status` (VARCHAR(50) DEFAULT 'IN_PROGRESS')
- `start_date` (DATE)
- `target_date` (DATE)
- `created_at` (TIMESTAMP WITH TIME ZONE)
- `updated_at` (TIMESTAMP WITH TIME ZONE)

### 4. `tasks`
- `id` (UUID PK)
- `user_id` (UUID FK -> users.id ON DELETE CASCADE)
- `goal_id` (UUID FK -> goals.id ON DELETE SET NULL)
- `title` (VARCHAR(255) NOT NULL)
- `description` (TEXT)
- `priority` (VARCHAR(50) DEFAULT 'MEDIUM')
- `status` (VARCHAR(50) DEFAULT 'TODO')
- `due_at` (TIMESTAMP WITH TIME ZONE)
- `estimated_minutes` (INTEGER DEFAULT 30)
- `actual_minutes` (INTEGER DEFAULT 0)
- `category` (VARCHAR(100))
- `completed_at` (TIMESTAMP WITH TIME ZONE)
- `created_at` (TIMESTAMP WITH TIME ZONE)
- `updated_at` (TIMESTAMP WITH TIME ZONE)
