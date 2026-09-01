import { apiClient } from './client';

export interface AIMessage {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export interface AIAction {
  id: string;
  user_id: string;
  conversation_id?: string;
  action_type: 'CREATE_TASK' | 'SCHEDULE_TASK' | 'COMPLETE_TASK' | 'CREATE_ROADMAP';
  target_type: string;
  target_id?: string;
  payload?: any;
  status: 'PENDING' | 'CONFIRMED' | 'REJECTED' | 'EXECUTED';
  requires_confirmation: boolean;
  created_at: string;
  confirmed_at?: string;
}

export interface AIConversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages: AIMessage[];
  actions: AIAction[];
}

export interface ChatResponse {
  conversation_id: string;
  message: AIMessage;
  proposed_actions: AIAction[];
}

export const aiApi = {
  listConversations: () => apiClient<AIConversation[]>('/ai/conversations'),

  getConversation: (id: string) => apiClient<AIConversation>(`/ai/conversations/${id}`),

  chat: (message: string, conversationId?: string) =>
    apiClient<ChatResponse>('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ message, conversation_id: conversationId }),
    }),

  confirmAction: (actionId: string) =>
    apiClient<AIAction>(`/ai/actions/${actionId}/confirm`, {
      method: 'POST',
    }),

  rejectAction: (actionId: string) =>
    apiClient<AIAction>(`/ai/actions/${actionId}/reject`, {
      method: 'POST',
    }),
};
