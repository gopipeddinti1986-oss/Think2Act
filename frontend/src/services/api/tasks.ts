import { apiClient } from './client';
import { Task, Priority, TaskStatus } from '@/types';

export interface CreateTaskInput {
  title: string;
  description?: string;
  goal_id?: string;
  priority?: Priority;
  status?: TaskStatus;
  due_at?: string;
  estimated_minutes?: number;
  category?: string;
}

export interface UpdateTaskInput extends Partial<CreateTaskInput> {
  actual_minutes?: number;
  completed_at?: string;
}

export interface TaskFilters {
  status?: string;
  priority?: string;
  goal_id?: string;
  category?: string;
}

export const tasksApi = {
  list: (filters: TaskFilters = {}) => {
    const params = new URLSearchParams();
    if (filters.status) params.append('status', filters.status);
    if (filters.priority) params.append('priority', filters.priority);
    if (filters.goal_id) params.append('goal_id', filters.goal_id);
    if (filters.category) params.append('category', filters.category);

    const queryString = params.toString();
    return apiClient<Task[]>(queryString ? `/tasks?${queryString}` : '/tasks');
  },

  get: (id: string) => apiClient<Task>(`/tasks/${id}`),

  create: (data: CreateTaskInput) =>
    apiClient<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: string, data: UpdateTaskInput) =>
    apiClient<Task>(`/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  complete: (id: string) =>
    apiClient<Task>(`/tasks/${id}/complete`, {
      method: 'POST',
    }),

  delete: (id: string) =>
    apiClient<{ message: string }>(`/tasks/${id}`, {
      method: 'DELETE',
    }),
};
