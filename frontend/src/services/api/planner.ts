import { apiClient } from './client';
import { Task, Priority } from '@/types';

export interface PlannerEntry {
  id: string;
  user_id: string;
  task_id: string;
  start_at: string;
  end_at: string;
  status: 'SCHEDULED' | 'COMPLETED' | 'MISSED' | 'CANCELLED';
  source: 'MANUAL' | 'AUTO_SUGGESTED' | 'AI_COACH';
  created_at: string;
  updated_at: string;
  task?: Task;
}

export interface CreatePlannerEntryInput {
  task_id: string;
  start_at: string;
  end_at: string;
  status?: string;
  source?: string;
}

export interface AutoScheduleSuggestion {
  task_id: string;
  task_title: string;
  start_at: string;
  end_at: string;
  priority: Priority;
}

export interface AutoScheduleResponse {
  date: string;
  available_hours: number;
  total_planned_hours: number;
  is_overloaded: boolean;
  suggestions: AutoScheduleSuggestion[];
}

export const plannerApi = {
  list: (startTime?: string, endTime?: string) => {
    const params = new URLSearchParams();
    if (startTime) params.append('start_time', startTime);
    if (endTime) params.append('end_time', endTime);
    const qs = params.toString();
    return apiClient<PlannerEntry[]>(qs ? `/planner?${qs}` : '/planner');
  },

  create: (data: CreatePlannerEntryInput) =>
    apiClient<PlannerEntry>('/planner', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: string, data: Partial<CreatePlannerEntryInput>) =>
    apiClient<PlannerEntry>(`/planner/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  delete: (id: string) =>
    apiClient<{ message: string }>(`/planner/${id}`, {
      method: 'DELETE',
    }),

  autoSchedule: (date?: string) =>
    apiClient<AutoScheduleResponse>('/planner/auto-schedule', {
      method: 'POST',
      body: JSON.stringify({ schedule_date: date }),
    }),
};
