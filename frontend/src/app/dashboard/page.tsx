"use client";

import { useQuery } from "@tanstack/react-query";
import { http } from "@/lib/http";
import { StatisticCard } from "@/components/shared/StatisticCard";
import { Users, Search, Activity, Cpu, Sparkles, RefreshCw, Play, PlayCircle, Loader2 } from "lucide-react";
import { useJobs } from "@/features/jobs/hooks";
import { useLeads } from "@/features/leads/hooks";
import { jobColumns } from "@/features/jobs/components/JobColumns";
import { leadColumns } from "@/features/leads/components/LeadColumns";
import { DataTable } from "@/components/shared/DataTable";
import { Button } from "@/components/ui/button";
import { useRunCrawler, useRunAllCrawlers } from "@/features/crawler/hooks";
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
    refetchInterval: 10000, // Refresh every 10s for live progress
  });

  const { data: leads = [], isLoading: isLeadsLoading, refetch: refetchLeads } = useLeads();
  const { data: jobs = [], isLoading: isJobsLoading, refetch: refetchJobs } = useJobs();
  
  const runCrawlerMutation = useRunCrawler();
  const runAllCrawlersMutation = useRunAllCrawlers();
  const [keywordId, setKeywordId] = useState("31");

  // Progress metrics calculation
  const totalKeywords = stats?.total_keywords ?? 10;
  const runningJobsCount = jobs.filter((j) => j.status === "RUNNING" || j.status === "STARTING" || j.status === "SAVING").length;
  const completedJobsCount = jobs.filter((j) => j.status === "COMPLETED").length;
  const progressPercent = Math.min(100, Math.round((completedJobsCount / Math.max(1, totalKeywords)) * 100));

  const handleRunSingleCrawler = () => {
    if (!keywordId) return;
    runCrawlerMutation.mutate(parseInt(keywordId, 10), {
      onSuccess: () => {
        toast.success("Single keyword crawl started!");
        refetchAll();
      },
      onError: (err: any) => toast.error(err.response?.data?.detail || "Failed to start crawler"),
    });
  };

  const handleRunAllCrawlers = () => {
    runAllCrawlersMutation.mutate(undefined, {
      onSuccess: () => {
        toast.success("Batch crawl triggered for ALL active keywords!");
        refetchAll();
      },
      onError: (err: any) => toast.error(err.response?.data?.detail || "Failed to start batch crawl"),
    });
  };

  const refetchAll = () => {
    refetchStats();
    refetchLeads();
    refetchJobs();
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
          <Button variant="outline" size="sm" onClick={refetchAll} className="gap-1.5">
            <RefreshCw className="h-3.5 w-3.5" /> Refresh
          </Button>
        </div>
      </div>

      {/* Live Extraction Progress Indicator Widget */}
      {runningJobsCount > 0 && (
        <div className="rounded-xl border border-blue-200 bg-blue-50/50 dark:bg-blue-950/40 p-4 shadow-sm space-y-2 animate-in fade-in">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-semibold text-blue-900 dark:text-blue-200">
              <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
              <span>Live Extraction Progress</span>
            </div>
            <span className="text-xs font-bold text-blue-700 dark:text-blue-300">
              {progressPercent}% Completed ({completedJobsCount}/{totalKeywords} Keywords)
            </span>
          </div>
          <div className="w-full bg-blue-200 dark:bg-blue-900 h-2 rounded-full overflow-hidden">
            <div
              className="bg-blue-600 h-full transition-all duration-500 rounded-full"
              style={{ width: `${Math.max(10, progressPercent)}%` }}
            />
          </div>
          <p className="text-xs text-blue-700 dark:text-blue-400">
            Currently extracting leads in background • Total Extracted: <strong>{leads.length} Leads</strong>
          </p>
        </div>
      )}

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
          value={isLeadsLoading ? "..." : leads.filter((l: any) => l.status === "NEW").length}
          description="Awaiting outreach"
          icon={Activity}
        />
        <StatisticCard
          title="Monitored Keywords"
          value={isStatsLoading ? "..." : totalKeywords}
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

      {/* Extraction Action Controls Bar */}
      <div className="rounded-xl border bg-card p-4 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h4 className="text-sm font-semibold">Crawl & Lead Extraction Controls</h4>
          <p className="text-xs text-muted-foreground">Trigger crawl for a single keyword or batch crawl all active keywords at once</p>
        </div>
        <div className="flex flex-wrap items-center gap-2.5 w-full sm:w-auto">
          {/* Run All Keywords Button */}
          <Button
            size="sm"
            variant="default"
            onClick={handleRunAllCrawlers}
            disabled={runAllCrawlersMutation.isPending || runningJobsCount > 0}
            className="gap-1.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold"
          >
            <PlayCircle className="h-4 w-4" />
            {runAllCrawlersMutation.isPending ? "Starting Batch..." : "Run Crawl for ALL Keywords"}
          </Button>

          {/* Single Keyword Input & Run */}
          <div className="flex items-center space-x-1.5">
            <input
              type="number"
              value={keywordId}
              onChange={(e) => setKeywordId(e.target.value)}
              className="flex h-9 w-20 rounded-md border border-input bg-transparent px-2 py-1 text-xs shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              placeholder="Kw ID"
            />
            <Button
              size="sm"
              variant="outline"
              onClick={handleRunSingleCrawler}
              disabled={runCrawlerMutation.isPending}
              className="gap-1 text-xs"
            >
              <Play className="h-3 w-3" />
              {runCrawlerMutation.isPending ? "Crawling..." : "Run ID"}
            </Button>
          </div>
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
        <DataTable columns={jobColumns} data={jobs.slice(0, 10)} isLoading={isJobsLoading} />
      </div>
    </div>
  );
}
