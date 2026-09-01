import { apiClient } from './client';
import { User } from '@/types';

export interface AuthResponse {
  user: User;
  token: {
    access_token: string;
    token_type: string;
  };
}

export const authApi = {
  register: (data: { name: string; email: string; password: string }) =>
    apiClient<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  login: (data: { email: string; password: string }) =>
    apiClient<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getMe: () => apiClient<User>('/auth/me'),

  logout: () =>
    apiClient<{ message: string }>('/auth/logout', {
      method: 'POST',
    }),
};
