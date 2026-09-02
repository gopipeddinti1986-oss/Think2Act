export type Priority = 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';
export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'COMPLETED' | 'DEFERRED' | 'CANCELLED';
export type GoalStatus = 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED' | 'ON_HOLD';
export type UserMode = 'student' | 'employee';

export interface User {
  id: string;
  name: string;
  email: string;
  is_active: boolean;
}

export interface UserProfile {
  id: string;
  user_id: string;
  bio?: string;
  location?: string;
  organization?: string;
  education?: string;
  experience?: string;
  user_mode: UserMode;
  career_goal?: string;
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface Goal {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  category?: string;
  priority: Priority;
  status: GoalStatus;
  start_date?: string;
  target_date?: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  user_id: string;
  goal_id?: string;
  title: string;
  description?: string;
  priority: Priority;
  status: TaskStatus;
  due_at?: string;
  estimated_minutes: number;
  actual_minutes: number;
  category?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface TasksSummary {
  total: number;
  completed: number;
  pending: number;
  completion_rate: number;
}

export interface AISuggestion {
  title: string;
  message: string;
  action_label?: string;
  action_type?: string;
}

export interface DashboardData {
  user: User;
  tasks_summary: {
    total: number;
    completed: number;
    pending: number;
    completion_rate: number;
  };
  productivity_score: number;
  focus_minutes_today: number;
  readiness_score: number;
  next_action?: Task;
  today_tasks: Task[];
  goals: Goal[];
  ai_suggestion?: AISuggestion;
}
