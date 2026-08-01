import axios from 'axios';

export const http = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://runtime-linkedin.onrender.com/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

http.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

http.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized globally
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
