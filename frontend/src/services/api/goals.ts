import { apiClient } from './client';
import { Goal, Priority, GoalStatus } from '@/types';

export interface CreateGoalInput {
  title: string;
  description?: string;
  category?: string;
  priority?: Priority;
  status?: GoalStatus;
  start_date?: string;
  target_date?: string;
}

export interface UpdateGoalInput extends Partial<CreateGoalInput> {}

export const goalsApi = {
  list: () => apiClient<Goal[]>('/goals'),

  get: (id: string) => apiClient<Goal>(`/goals/${id}`),

  create: (data: CreateGoalInput) =>
    apiClient<Goal>('/goals', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: string, data: UpdateGoalInput) =>
    apiClient<Goal>(`/goals/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  delete: (id: string) =>
    apiClient<{ message: string }>(`/goals/${id}`, {
      method: 'DELETE',
    }),
};
