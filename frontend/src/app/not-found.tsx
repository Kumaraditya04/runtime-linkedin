import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function NotFound() {
  return (
    <div className="flex h-screen w-full flex-col items-center justify-center space-y-4">
      <h2 className="text-2xl font-bold tracking-tight">404 - Page Not Found</h2>
      <p className="text-muted-foreground text-center max-w-md">
        The page you are looking for does not exist or has been moved.
      </p>
      <Link href="/dashboard">
        <Button>Return to Dashboard</Button>
      </Link>
    </div>
  );
}
