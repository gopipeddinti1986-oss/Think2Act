import { apiClient } from './client';

export interface DecisionScore {
  id: string;
  option_id: string;
  criterion_id: string;
  score: number;
  rationale?: string;
  created_at: string;
}

export interface DecisionCriterion {
  id: string;
  decision_id: string;
  name: string;
  weight: number;
  created_at: string;
}

export interface DecisionOption {
  id: string;
  decision_id: string;
  name: string;
  description?: string;
  total_score: number;
  created_at: string;
  scores: DecisionScore[];
}

export interface Decision {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  category: string;
  status: string;
  recommended_option_id?: string;
  created_at: string;
  updated_at: string;
  options: DecisionOption[];
  criteria: DecisionCriterion[];
}

export const decisionsApi = {
  list: async (): Promise<Decision[]> => {
    return apiClient.get('/decisions');
  },
  create: async (data: {
    title: string;
    description?: string;
    category?: string;
    options?: string[];
    criteria?: Array<{ name: string; weight: number }>;
  }): Promise<Decision> => {
    return apiClient.post('/decisions', data);
  },
  getById: async (id: string): Promise<Decision> => {
    return apiClient.get(`/decisions/${id}`);
  },
  updateScore: async (
    decisionId: string,
    data: { option_id: string; criterion_id: string; score: number; rationale?: string }
  ): Promise<Decision> => {
    return apiClient.post(`/decisions/${decisionId}/score`, data);
  },
};
