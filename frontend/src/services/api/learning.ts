import { apiClient } from './client';
import { Task } from '@/types';

export interface RoleSkillRequirement {
  skill_id: string;
  skill_name: string;
  required_level: number;
  importance: string;
}

export interface Role {
  id: string;
  name: string;
  category?: string;
  description?: string;
  requirements: RoleSkillRequirement[];
}

export interface SkillGapItem {
  skill_id: string;
  skill_name: string;
  category?: string;
  current_level: number;
  required_level: number;
  gap: number;
  importance: string;
  severity: 'CRITICAL' | 'IMPORTANT' | 'MODERATE' | 'MINOR';
  recommended_action: string;
}

export interface SkillGapReport {
  role_id: string;
  role_name: string;
  overall_readiness: number;
  total_gaps: number;
  critical_gaps: number;
  gaps: SkillGapItem[];
}

export interface LearningResource {
  id: string;
  title: string;
  provider?: string;
  url?: string;
  description?: string;
  difficulty: string;
}

export interface LearningPathItem {
  id: string;
  learning_path_id: string;
  skill_id: string;
  skill_name?: string;
  title: string;
  sequence_number: number;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
  progress: number;
  resource?: LearningResource;
}

export interface LearningPath {
  id: string;
  user_id: string;
  goal_id?: string;
  role_id?: string;
  title: string;
  status: 'ACTIVE' | 'COMPLETED' | 'ARCHIVED';
  created_at: string;
  items: LearningPathItem[];
}

export const learningApi = {
  getRoles: () => apiClient<Role[]>('/roles'),

  getSkillGaps: (roleId?: string) => {
    const qs = roleId ? `?role_id=${roleId}` : '';
    return apiClient<SkillGapReport>(`/skills/gaps${qs}`);
  },

  getResources: () => apiClient<LearningResource[]>('/learning/resources'),

  getPaths: () => apiClient<LearningPath[]>('/learning/paths'),

  generateRoadmap: (data: { role_id?: string; goal_id?: string; title?: string }) =>
    apiClient<LearningPath>('/learning/paths/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  convertToTask: (itemId: string) =>
    apiClient<{ task: Task; message: string }>(`/learning/items/${itemId}/convert-to-task`, {
      method: 'POST',
    }),

  completeItem: (itemId: string) =>
    apiClient<LearningPathItem>(`/learning/items/${itemId}/complete`, {
      method: 'POST',
    }),
};
