import { LayoutDashboard, Key, Settings, Search, Contact, List } from 'lucide-react';

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
    title: 'System Settings',
    icon: Settings,
    href: '/dashboard/settings',
    requiredRole: 'admin',
  },
];
