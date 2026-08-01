"use client";

import { useQuery } from "@tanstack/react-query";
import { http } from "@/lib/http";
import { StatisticCard } from "@/components/shared/StatisticCard";
import { Users, Search, Activity, Cpu } from "lucide-react";
import { useJobs } from "@/features/jobs/hooks";
import { jobColumns } from "@/features/jobs/components/JobColumns";
import { DataTable } from "@/components/shared/DataTable";
import { Button } from "@/components/ui/button";
import { useRunCrawler } from "@/features/crawler/hooks";
import { toast } from "sonner";
import { useState } from "react";

const getStats = async () => {
  const { data } = await http.get("/admin/dashboard/stats");
  return data;
};

export default function DashboardPage() {
  const { data: stats, isLoading: isStatsLoading } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: getStats,
  });

  const { data: jobs = [], isLoading: isJobsLoading } = useJobs();
  const runCrawlerMutation = useRunCrawler();
  const [keywordId, setKeywordId] = useState("1"); // Hardcoded MVP input

  const handleRunCrawler = () => {
    if (!keywordId) return;
    runCrawlerMutation.mutate(parseInt(keywordId, 10), {
      onSuccess: () => toast.success("Crawler started!"),
      onError: (err: any) => toast.error(err.response?.data?.detail || "Failed to start crawler"),
    });
  };

  return (
    <>
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 p-4 md:p-8 pt-6">
      <StatisticCard
        title="Total Keywords"
        value={isStatsLoading ? "..." : stats?.total_keywords ?? 0}
        description="Monitored in system"
        icon={Users}
      />
      <StatisticCard
        title="Active Keywords"
        value={isStatsLoading ? "..." : stats?.active_keywords ?? 0}
        description={`Paused: ${stats?.paused_keywords ?? 0}`}
        icon={Activity}
      />
      <StatisticCard
        title="Crawler Status"
        value={isStatsLoading ? "..." : stats?.crawler_status ?? "Idle"}
        description="Last run: Never"
        icon={Search}
      />
      <StatisticCard
        title="AI Analysis"
        value="Enabled"
        description="Using gpt-4o"
        icon={Cpu}
      />
    </div>

    <div className="p-4 md:p-8 pt-0 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-bold tracking-tight">Recent Jobs</h3>
        <div className="flex space-x-2">
          <input
            type="number"
            value={keywordId}
            onChange={(e) => setKeywordId(e.target.value)}
            className="flex h-9 w-24 rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
            placeholder="Kw ID"
          />
          <Button onClick={handleRunCrawler} disabled={runCrawlerMutation.isPending}>
            Run Crawler
          </Button>
        </div>
      </div>
      <DataTable columns={jobColumns} data={jobs} isLoading={isJobsLoading} />
    </div>
    </>
  );
}
