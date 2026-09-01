import { apiClient } from './client';
import { DashboardData } from '@/types';

export const dashboardApi = {
  getSummary: () => apiClient<DashboardData>('/dashboard'),
};
