import { apiClient } from './client';

export interface JobPosting {
  id: string;
  title: string;
  company: string;
  location: string;
  salary_range?: string;
  description?: string;
  required_skills: Array<{ name: string; required_level: number }>;
  match_percentage: number;
  missing_skills: string[];
  created_at: string;
}

export interface ApplicationEvent {
  id: string;
  application_id: string;
  event_type: string;
  title: string;
  notes?: string;
  event_date: string;
  created_at: string;
}

export interface JobApplication {
  id: string;
  user_id: string;
  job_id: string;
  status: 'SAVED' | 'APPLIED' | 'OA' | 'INTERVIEW' | 'OFFER' | 'REJECTED';
  applied_at?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
  job?: JobPosting;
  events: ApplicationEvent[];
}

export const jobsApi = {
  list: async (): Promise<JobPosting[]> => {
    return apiClient.get('/jobs');
  },
  listApplications: async (): Promise<JobApplication[]> => {
    return apiClient.get('/jobs/applications');
  },
  createApplication: async (jobId: string, status = 'SAVED', notes?: string): Promise<JobApplication> => {
    return apiClient.post('/jobs/applications', { job_id: jobId, status, notes });
  },
  updateStatus: async (appId: string, status: string): Promise<JobApplication> => {
    return apiClient.patch(`/jobs/applications/${appId}/status`, { status });
  },
};
