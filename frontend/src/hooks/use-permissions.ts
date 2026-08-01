import { useAuth } from './use-auth';

export function usePermissions() {
  const { user, isAuthenticated } = useAuth();

  const hasRole = (role: string) => {
    if (!isAuthenticated || !user) return false;
    return user.role === role;
  };

  const isAdmin = hasRole('admin');

  return {
    hasRole,
    isAdmin,
  };
}
