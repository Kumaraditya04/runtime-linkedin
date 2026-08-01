import { http } from '@/lib/http';

export const authService = {
  login: async (credentials: URLSearchParams) => {
    // URLSearchParams is used because FastAPI OAuth2PasswordRequestForm expects form data
    const response = await http.post('/public/auth/login', credentials, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },
  
  logout: async () => {
    const response = await http.post('/public/auth/logout');
    return response.data;
  },
};
