import { apiClient } from './client';

export interface EvidenceItem {
  id: string;
  skill_id: string;
  source_type: string;
  source_id?: string;
  strength: number;
  description: string;
  occurred_at: string;
}

export interface SkillHistoryPoint {
  level: number;
  confidence: number;
  reason?: string;
  recorded_at: string;
}

export interface UserSkill {
  skill_id: string;
  name: string;
  category?: string;
  level: number;
  confidence: number;
  last_assessed_at: string;
  evidence_count: number;
  recent_evidence: EvidenceItem[];
  history: SkillHistoryPoint[];
}

export interface SkillCatalogItem {
  id: string;
  name: string;
  category?: string;
  description?: string;
  created_at: string;
}

export const skillsApi = {
  getMySkills: () => apiClient<UserSkill[]>('/skills/me'),

  getSkillDetail: (skillId: string) => apiClient<UserSkill>(`/skills/me/${skillId}`),

  getCatalog: (category?: string) => {
    const qs = category ? `?category=${encodeURIComponent(category)}` : '';
    return apiClient<SkillCatalogItem[]>(`/skills${qs}`);
  },

  createSkill: (data: { name: string; category?: string; description?: string }) =>
    apiClient<SkillCatalogItem>('/skills', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  assignTaskSkills: (taskId: string, skillIds: string[]) =>
    apiClient<{ message: string }>(`/skills/tasks/${taskId}/assign`, {
      method: 'POST',
      body: JSON.stringify({ skill_ids: skillIds }),
    }),
};
