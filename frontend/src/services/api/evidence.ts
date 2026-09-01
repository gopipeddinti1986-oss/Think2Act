import { apiClient } from './client';
import { EvidenceItem } from './skills';

export interface CreateEvidenceInput {
  skill_id: string;
  source_type?: string;
  strength?: number;
  description: string;
}

export const evidenceApi = {
  list: () => apiClient<EvidenceItem[]>('/evidence'),

  addManual: (data: CreateEvidenceInput) =>
    apiClient<EvidenceItem>('/evidence/manual', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};
