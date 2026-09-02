import { apiClient } from './client';

export interface InterviewQuestion {
  id: string;
  session_id: string;
  question_text: string;
  target_skill?: string;
  difficulty: string;
  user_answer?: string;
  rubric_scores: Record<string, number>;
  ai_feedback?: string;
  ideal_answer?: string;
  score: number;
  created_at: string;
}

export interface InterviewSession {
  id: string;
  user_id: string;
  role_title: string;
  session_type: string;
  status: string;
  overall_score: number;
  summary_feedback?: string;
  created_at: string;
  questions: InterviewQuestion[];
}

export const interviewsApi = {
  list: async (): Promise<InterviewSession[]> => {
    return apiClient.get('/interviews');
  },
  start: async (role_title = 'Backend Software Engineer', session_type = 'TECHNICAL'): Promise<InterviewSession> => {
    return apiClient.post('/interviews', { role_title, session_type });
  },
  getById: async (id: string): Promise<InterviewSession> => {
    return apiClient.get(`/interviews/${id}`);
  },
  submitAnswer: async (sessionId: string, questionId: string, answer: string): Promise<InterviewQuestion> => {
    return apiClient.post(`/interviews/${sessionId}/answer`, { question_id: questionId, answer });
  },
};
