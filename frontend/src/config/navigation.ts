import { LayoutDashboard, Key, Settings, Search, Contact, List, Activity } from 'lucide-react';

export const navigationConfig = [
  {
    title: 'Dashboard',
    icon: LayoutDashboard,
    href: '/dashboard',
  },
  {
    title: 'Keywords',
    icon: List,
    href: '/dashboard/keywords',
  },
  {
    title: 'Leads',
    icon: Contact,
    href: '/dashboard/leads',
  },
  {
    title: 'Executions',
    icon: Activity,
    href: '/dashboard/executions',
  },
  {
    title: 'System Settings',
    icon: Settings,
    href: '/dashboard/settings',
    requiredRole: 'admin',
  },
];
