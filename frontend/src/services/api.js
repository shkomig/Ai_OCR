import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// Documents API
export const documentsAPI = {
  upload: (formData) =>
    api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  list: (skip = 0, limit = 20) =>
    api.get('/documents/', { params: { skip, limit } }),
  get: (id) => api.get(`/documents/${id}`),
  getStatus: (id) => api.get(`/documents/${id}/status`),
  delete: (id) => api.delete(`/documents/${id}`),
};

// Content API
export const contentAPI = {
  generateGame: (documentId, gameType = 'auto') =>
    api.post(`/content/${documentId}/games`, { game_type: gameType }),
  generateQuiz: (documentId, difficulty = 'medium') =>
    api.post(`/content/${documentId}/quizzes`, { difficulty }),
  generateReview: (documentId, topics = []) =>
    api.post(`/content/${documentId}/review-materials`, { topics }),
  get: (contentId) => api.get(`/content/${contentId}`),
  listByDocument: (documentId) => api.get(`/content/document/${documentId}/all`),
};

// Progress API
export const progressAPI = {
  submit: (data) => api.post('/progress/submit', data),
  getUserProgress: (userId, skip = 0, limit = 50) =>
    api.get(`/progress/user/${userId}`, { params: { skip, limit } }),
  getDashboard: (userId) => api.get(`/progress/user/${userId}/dashboard`),
  getContentProgress: (contentId) => api.get(`/progress/content/${contentId}`),
};

export default api;
