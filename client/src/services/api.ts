import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login/', { email, password }),
  
  register: (userData: { username: string; email: string; password: string; first_name: string; last_name: string }) =>
    api.post('/accounts/users/', userData),
  
  logout: (refreshToken: string) =>
    api.post('/accounts/users/logout/', { refresh_token: refreshToken }),
};

// Accounts API
export const accountsAPI = {
  profile: () => api.get('/accounts/profile/'),
  updateProfile: (data: any) => api.patch('/accounts/profile/', data),
  changePassword: (data: { old_password: string; new_password: string }) =>
    api.post('/accounts/change-password/', data),
  logout: (refreshToken: string) =>
    api.post('/accounts/users/logout/', { refresh_token: refreshToken }),
};

// Devices API
export const devicesAPI = {
  list: () => api.get('/devices/'),
  create: (data: any) => api.post('/devices/', data),
  get: (id: string) => api.get(`/devices/${id}/`),
  update: (id: string, data: any) => api.patch(`/devices/${id}/`, data),
  delete: (id: string) => api.delete(`/devices/${id}/`),
};

// Device Types API
export const deviceTypesAPI = {
  list: () => api.get('/devices/device-types/'),
};

// Personality Traits API
export const personalityTraitsAPI = {
  list: () => api.get('/devices/personality-traits/'),
};

// Apps API
export const appsAPI = {
  list: () => api.get('/apps/'),
  search: (query: string) => api.get(`/apps/?search=${query}`),
};

// Device Apps API (Apps installed on device)
export const deviceAppsAPI = {
  list: (deviceId?: string) => 
    api.get('/apps/device-apps/', { params: { device: deviceId } }),
  create: (data: any) => api.post('/apps/device-apps/', data),
  update: (id: number, data: any) => api.patch(`/apps/device-apps/${id}/`, data),
  delete: (id: number) => api.delete(`/apps/device-apps/${id}/`),
};

// Usage Data API
export const usageAPI = {
  list: (params?: any) => api.get('/usage/usage-data/', { params }),
  create: (data: any) => api.post('/usage/usage-data/', data),
  bulkCreate: (data: any[]) => api.post('/usage/usage-data/bulk_upload/', data ),
};

// App Usage API (Per-app usage tracking)
export const appUsageAPI = {
  list: (params?: any) => api.get('/usage/app-usage/', { params }),
  create: (data: any) => api.post('/usage/app-usage/', data),
  bulkCreate: (data: any[]) => api.post('/usage/app-usage/bulk_upload/', data),
};

// Conversations API
export const conversationsAPI = {
  list: (params?: any) => api.get('/conversations/', { params }),
  get: (id: string) => api.get(`/conversations/${id}/`),
  rate: (id: string, rating: number, feedback?: string) =>
    api.post(`/conversations/${id}/rate/`, { rating, feedback }),
  toggleFavorite: (id: string) => api.post(`/conversations/${id}/toggle_favorite/`),
  toggleHidden: (id: string) => api.post(`/conversations/${id}/toggle_hidden/`),
  favorites: () => api.get('/conversations/favorites/'),
  recent: (limit?: number) => api.get('/conversations/recent/', { params: { limit } }),
};

// Journals API
export const journalsAPI = {
  deviceJournals: {
    list: (params?: any) => api.get('/conversations/device-journals/', { params }),
    get: (id: string) => api.get(`/conversations/device-journals/${id}/`),
    recent: (limit?: number) => api.get('/conversations/device-journals/recent/', { params: { limit } }),
  },
  appJournals: {
    list: (params?: any) => api.get('/conversations/app-journals/', { params }),
    get: (id: string) => api.get(`/conversations/app-journals/${id}/`),
    recent: (limit?: number) => api.get('/conversations/app-journals/recent/', { params: { limit } }),
  },
};

// Analytics API
export const analyticsAPI = {
  stats: {
    list: (params?: any) => api.get('/analytics/stats/', { params }),
    latest: () => api.get('/analytics/stats/latest/'),
  },
  trends: {
    list: (params?: any) => api.get('/analytics/trends/', { params }),
    latest: (periodType?: string) => api.get('/analytics/trends/latest/', { params: { period_type: periodType } }),
  },
};

// Usage Patterns API
export const patternsAPI = {
  list: (params?: any) => api.get('/usage/patterns/', { params }),
  get: (id: string) => api.get(`/usage/patterns/${id}/`),
};

// Usage Goals API
export const goalsAPI = {
  list: (params?: any) => api.get('/usage/goals/', { params }),
  create: (data: any) => api.post('/usage/goals/', data),
  get: (id: string) => api.get(`/usage/goals/${id}/`),
  update: (id: string, data: any) => api.patch(`/usage/goals/${id}/`, data),
  delete: (id: string) => api.delete(`/usage/goals/${id}/`),
};

// Social API
export const socialAPI = {
  friends: {
    list: () => api.get('/social/'),
    active: () => api.get('/social/active/'),
    create: (data: any) => api.post('/social/', data),
    delete: (id: string) => api.delete(`/social/${id}/`),
  },
  challenges: {
    list: () => api.get('/social/challenges/'),
    active: () => api.get('/social/challenges/active/'),
    create: (data: any) => api.post('/social/challenges/', data),
    get: (id: string) => api.get(`/social/challenges/${id}/`),
    join: (id: string) => api.post(`/social/challenges/${id}/join/`),
    leave: (id: string) => api.post(`/social/challenges/${id}/leave/`),
  },
};

// AI Generation API (for testing/manual trigger)
export const aiGenerationAPI = {
  generateConversations: () => api.post('/ai-engine/generate-conversations/'),
  generateJournals: () => api.post('/ai-engine/generate-journals/'),
  generateForUser: () => api.post('/ai-engine/generate-conversations/'),
};

export default api;
