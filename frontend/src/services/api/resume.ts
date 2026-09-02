import { apiClient } from './client';

export interface ResumeSuggestion {
  id: string;
  resume_id: string;
  section: string;
  suggestion_type: string;
  current_text: string;
  recommended_text: string;
  impact_reason?: string;
  is_applied: boolean;
  created_at: string;
}

export interface Resume {
  id: string;
  user_id: string;
  title: string;
  target_role: string;
  raw_text?: string;
  parsed_sections: {
    summary?: string;
    experience?: string[];
    skills?: string[];
  };
  ats_score: number;
  created_at: string;
  updated_at: string;
  suggestions: ResumeSuggestion[];
}

export const resumeApi = {
  list: async (): Promise<Resume[]> => {
    return apiClient.get('/resume');
  },
  create: async (data: { title: string; target_role: string; raw_text?: string }): Promise<Resume> => {
    return apiClient.post('/resume', data);
  },
  getById: async (id: string): Promise<Resume> => {
    return apiClient.get(`/resume/${id}`);
  },
  applySuggestion: async (resumeId: string, suggestionId: string): Promise<Resume> => {
    return apiClient.post(`/resume/${resumeId}/suggestions/${suggestionId}/apply`, { apply: true });
  },
};
