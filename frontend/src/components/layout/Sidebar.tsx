"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Radar } from "lucide-react";
import { navigationConfig } from "@/config/navigation";
import { cn } from "@/lib/utils";

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 z-10 hidden w-14 flex-col border-r bg-background sm:flex lg:w-64">
      <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <Radar className="h-6 w-6 text-primary" />
          <span className="hidden lg:block text-lg">LeadRadar AI</span>
        </Link>
      </div>
      <nav className="flex-1 overflow-auto py-4">
        <ul className="grid gap-1 px-2 lg:px-4">
          {navigationConfig.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:text-primary",
                    isActive
                      ? "bg-muted text-primary"
                      : "text-muted-foreground"
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span className="hidden lg:block">{item.title}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}
