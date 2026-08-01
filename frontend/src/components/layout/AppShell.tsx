"use client";

import * as React from "react";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen w-full bg-muted/40">
      <Sidebar />
      <div className="flex flex-col sm:gap-4 sm:py-4 sm:pl-14 lg:pl-64 w-full">
        <TopBar />
        <main className="flex-1 items-start p-4 sm:px-6 sm:py-0 md:gap-8 w-full">
          {children}
        </main>
      </div>
    </div>
  );
}
