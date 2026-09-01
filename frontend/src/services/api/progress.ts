import { apiClient } from './client';

export interface DailyMetricPoint {
  date: string;
  score: number;
  focus_minutes: number;
  distraction_minutes: number;
  tasks_completed: number;
}

export interface ProductivityTrendResponse {
  current_score: number;
  previous_score: number;
  change_percentage: number;
  range_days: number;
  history: DailyMetricPoint[];
  estimation_accuracy_percentage: number;
  strongest_focus_period: string;
}

export const progressApi = {
  getProductivityTrends: (days: number = 30) =>
    apiClient<ProductivityTrendResponse>(`/progress/productivity?days=${days}`),
};
