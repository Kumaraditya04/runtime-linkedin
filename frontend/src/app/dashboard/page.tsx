"use client";

import { useQuery } from "@tanstack/react-query";
import { http } from "@/lib/http";
import { StatisticCard } from "@/components/shared/StatisticCard";
import { Users, Search, Activity, Cpu, Sparkles, RefreshCw } from "lucide-react";
import { useJobs } from "@/features/jobs/hooks";
import { useLeads } from "@/features/leads/hooks";
import { jobColumns } from "@/features/jobs/components/JobColumns";
import { leadColumns } from "@/features/leads/components/LeadColumns";
import { DataTable } from "@/components/shared/DataTable";
import { Button } from "@/components/ui/button";
import { useRunCrawler } from "@/features/crawler/hooks";
import { toast } from "sonner";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";

const getStats = async () => {
  try {
    const { data } = await http.get("/admin/dashboard/stats");
    return data;
  } catch (e) {
    return null;
  }
};

export default function DashboardPage() {
  const { data: stats, isLoading: isStatsLoading, refetch: refetchStats } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: getStats,
    refetchInterval: 15000, // Auto-refresh stats every 15s
  });

  const { data: leads = [], isLoading: isLeadsLoading, refetch: refetchLeads } = useLeads();
  const { data: jobs = [], isLoading: isJobsLoading, refetch: refetchJobs } = useJobs();
  const runCrawlerMutation = useRunCrawler();
  const [keywordId, setKeywordId] = useState("31");

  const newLeadsCount = leads.filter((l: any) => l.status === "NEW").length;

  const handleRunCrawler = () => {
    if (!keywordId) return;
    runCrawlerMutation.mutate(parseInt(keywordId, 10), {
      onSuccess: () => {
        toast.success("Crawl job triggered!");
        setTimeout(() => {
          refetchLeads();
          refetchJobs();
          refetchStats();
        }, 2000);
      },
      onError: (err: any) => toast.error(err.response?.data?.detail || "Failed to start crawler"),
    });
  };

  const handleRefreshAll = () => {
    refetchStats();
    refetchLeads();
    refetchJobs();
    toast.info("Dashboard data refreshed");
  };

  return (
    <div className="flex-1 space-y-6 p-4 md:p-8 pt-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            Dashboard Overview <Sparkles className="h-6 w-6 text-blue-500" />
          </h2>
          <p className="text-sm text-muted-foreground">
            Live AI Sales Intelligence & LinkedIn Lead Monitor
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="outline" className="px-3 py-1 text-xs font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse mr-2 inline-block" />
            Auto-Crawler Active (30m)
          </Badge>
          <Button variant="outline" size="sm" onClick={handleRefreshAll} className="gap-1.5">
            <RefreshCw className="h-3.5 w-3.5" /> Refresh
          </Button>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatisticCard
          title="Total Leads"
          value={isLeadsLoading ? "..." : leads.length}
          description="Extracted from LinkedIn"
          icon={Users}
        />
        <StatisticCard
          title="New Unreviewed Leads"
          value={isLeadsLoading ? "..." : newLeadsCount}
          description="Awaiting outreach"
          icon={Activity}
        />
        <StatisticCard
          title="Monitored Keywords"
          value={isStatsLoading ? "..." : stats?.total_keywords ?? 10}
          description={`Active: ${stats?.active_keywords ?? 10}`}
          icon={Search}
        />
        <StatisticCard
          title="Auto-Crawler Schedule"
          value="Every 30m"
          description="Background Playwright worker"
          icon={Cpu}
        />
      </div>

      {/* Manual Trigger Control Bar */}
      <div className="rounded-xl border bg-card p-4 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h4 className="text-sm font-semibold">Instant Lead Extraction</h4>
          <p className="text-xs text-muted-foreground">Run an immediate live crawl for any targeted keyword ID</p>
        </div>
        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <input
            type="number"
            value={keywordId}
            onChange={(e) => setKeywordId(e.target.value)}
            className="flex h-9 w-24 rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            placeholder="Kw ID"
          />
          <Button size="sm" onClick={handleRunCrawler} disabled={runCrawlerMutation.isPending}>
            {runCrawlerMutation.isPending ? "Crawling..." : "Run Crawl Now"}
          </Button>
        </div>
      </div>

      {/* Recent Extracted Leads Section */}
      <div className="space-y-4 pt-2">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold tracking-tight">Recent Extracted Leads</h3>
          <span className="text-xs text-muted-foreground font-medium">
            Showing top {leads.slice(0, 15).length} latest prospects
          </span>
        </div>
        <DataTable columns={leadColumns} data={leads.slice(0, 15)} isLoading={isLeadsLoading} />
      </div>

      {/* Recent Crawler Jobs Section */}
      <div className="space-y-4 pt-4">
        <h3 className="text-xl font-bold tracking-tight">Recent Crawler Executions</h3>
        <DataTable columns={jobColumns} data={jobs.slice(0, 5)} isLoading={isJobsLoading} />
      </div>
    </div>
  );
}
