"use client"

import * as React from "react"
import { QueryClientProvider } from "@tanstack/react-query"
import { queryClient } from "@/lib/query-client"
import { ThemeProvider } from "./theme-provider"
import { TooltipProvider } from "@/components/ui/tooltip"
import { Toaster } from "sonner"

export function AppProvider({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider
        attribute="class"
        defaultTheme="system"
        enableSystem
        disableTransitionOnChange
      >
        <TooltipProvider>
          {children}
          <Toaster richColors position="top-right" />
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}
