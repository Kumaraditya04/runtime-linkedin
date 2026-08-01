import { useQuery } from '@tanstack/react-query';
import { http } from '@/lib/http';

export function useAuth() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      // In a real app, this would hit a /me endpoint
      // For now we'll just check if we can hit an internal endpoint
      const response = await http.get('/internal/health');
      return response.data;
    },
    retry: false,
  });

  return {
    user: data?.data,
    isLoading,
    error,
    isAuthenticated: !!data,
  };
}
