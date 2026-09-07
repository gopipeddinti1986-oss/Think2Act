import { apiClient } from './client';

export interface UserSettingsData {
  user_id: string;
  name: string;
  email: string;
  user_mode: 'student' | 'employee';
  timezone: string;
  bio?: string;
  location?: string;
  organization?: string;
  education?: string;
  experience?: string;
  career_goal?: string;
  target_role?: string;
  target_companies?: string[];
  career_mode?: string;
  github_handle?: string;
  linkedin_profile_url?: string;
  leetcode_username?: string;
}

export const settingsApi = {
  getSettings: () => apiClient<UserSettingsData>('/settings'),
  updateProfile: (data: Partial<UserSettingsData>) =>
    apiClient<{ message: string }>('/settings/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
  updateCareer: (data: Partial<UserSettingsData>) =>
    apiClient<{ message: string }>('/settings/career', {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
  updateIntegrations: (data: Partial<UserSettingsData>) =>
    apiClient<{ message: string }>('/settings/integrations', {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
  exportData: () => apiClient<Record<string, any>>('/settings/export'),
  deleteAccount: () =>
    apiClient<{ message: string }>('/settings/account', {
      method: 'DELETE',
    }),
};
