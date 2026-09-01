import { apiClient } from './client';
import { Task } from '@/types';

export interface FocusSession {
  id: string;
  user_id: string;
  task_id?: string;
  started_at: string;
  ended_at?: string;
  duration_seconds: number;
  productive_seconds: number;
  distracted_seconds: number;
  status: 'RUNNING' | 'PAUSED' | 'COMPLETED' | 'CANCELLED';
  created_at: string;
  task?: Task;
}

export interface FocusSummaryToday {
  total_sessions: number;
  focus_seconds: number;
  distracted_seconds: number;
  focus_ratio: number;
}

export const focusApi = {
  start: (taskId?: string) =>
    apiClient<FocusSession>('/focus/sessions', {
      method: 'POST',
      body: JSON.stringify({ task_id: taskId }),
    }),

  getActive: () => apiClient<FocusSession | null>('/focus/active'),

  finish: (sessionId: string, data: { productive_seconds: number; distracted_seconds: number; mark_task_completed?: boolean }) =>
    apiClient<FocusSession>(`/focus/sessions/${sessionId}/finish`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  list: () => apiClient<FocusSession[]>('/focus/sessions'),

  getToday: () => apiClient<FocusSummaryToday>('/focus/today'),
};
