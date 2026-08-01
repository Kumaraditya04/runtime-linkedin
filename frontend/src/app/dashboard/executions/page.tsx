"use client";

import { useJobs } from "@/features/jobs/hooks";
import { jobColumns } from "@/features/jobs/components/JobColumns";
import { DataTable } from "@/components/shared/DataTable";
import { Activity } from "lucide-react";

export default function ExecutionsPage() {
  const { data: jobs = [], isLoading: isJobsLoading } = useJobs();

  return (
    <div className="flex-1 space-y-6 p-4 md:p-8 pt-6">
      <div className="flex flex-col gap-2">
        <h2 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          Crawler Executions <Activity className="h-6 w-6 text-primary" />
        </h2>
        <p className="text-sm text-muted-foreground">
          View all historical and running crawler jobs across all keywords.
        </p>
      </div>
      
      <div className="rounded-xl border bg-card p-1 shadow-sm">
        <DataTable columns={jobColumns} data={jobs} isLoading={isJobsLoading} />
      </div>
    </div>
  );
}
