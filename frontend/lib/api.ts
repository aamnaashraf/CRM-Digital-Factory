import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:7860';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints
export const apiClient = {
  // Health check
  health: () => api.get('/api/health'),

  // Support
  submitTicket: (data: {
    name: string;
    email: string;
    subject: string;
    message: string;
    priority?: string;
  }) => api.post('/api/support/submit', data),

  getTicket: (ticketId: string) => api.get(`/api/support/ticket/${ticketId}`),

  // Dashboard stats
  getStats: () => api.get('/api/dashboard/metrics'),

  // Activity feed
  getActivity: () => api.get('/api/dashboard/activity'),
  getBalancedActivity: () => api.get('/api/dashboard/activity/balanced'),
  // Use balanced activity for conversations to ensure all channels are represented
  getConversations: () => api.get('/api/dashboard/activity/balanced'),
  getConversation: (id: string) => api.get(`/api/support/ticket/${id}`),

  // Analytics data
  getAnalytics: () => api.get('/api/dashboard/analytics'),

  // Daily reports
  getDailyReports: () => api.get('/api/reports/sentiment/daily'),
  getDailyReport: (date: string) => api.get(`/api/reports/sentiment/daily/${date}`),

  // Settings
  getSettings: () => api.get('/api/settings'),
  updateSettings: (data: any) => api.post('/api/settings', data),
};
