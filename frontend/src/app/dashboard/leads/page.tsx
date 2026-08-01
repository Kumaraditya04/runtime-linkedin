"use client";

import { useState, useMemo } from "react";
import { DataTable } from "@/components/shared/DataTable";
import { leadColumns } from "@/features/leads/components/LeadColumns";
import { useLeads } from "@/features/leads/hooks";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, Filter, Calendar, Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export default function LeadsPage() {
  const { data: rawLeads = [], isLoading } = useLeads();
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [sortOrder, setSortOrder] = useState<"desc" | "asc">("desc");
  const [activeTab, setActiveTab] = useState("all");

  // Helper to check date category
  const getDateCategory = (dateStr: string) => {
    let s = String(dateStr).trim();
    if (s.includes(" ") && !s.includes("T")) s = s.replace(" ", "T");
    if (!s.endsWith("Z") && !s.includes("+")) s += "Z";
    
    const d = new Date(s);
    const now = new Date();
    
    const isToday =
      d.getDate() === now.getDate() &&
      d.getMonth() === now.getMonth() &&
      d.getFullYear() === now.getFullYear();

    const yesterday = new Date(now);
    yesterday.setDate(now.getDate() - 1);
    const isYesterday =
      d.getDate() === yesterday.getDate() &&
      d.getMonth() === yesterday.getMonth() &&
      d.getFullYear() === yesterday.getFullYear();

    if (isToday) return "today";
    if (isYesterday) return "yesterday";
    return "older";
  };

  // Filtered & Sorted Leads
  const processedLeads = useMemo(() => {
    let list = [...rawLeads];

    // 1. Sort by created_at
    list.sort((a, b) => {
      const timeA = new Date(a.created_at || 0).getTime();
      const timeB = new Date(b.created_at || 0).getTime();
      return sortOrder === "desc" ? timeB - timeA : timeA - timeB;
    });

    // 2. Tab Datewise Segregation
    if (activeTab !== "all") {
      list = list.filter((lead) => getDateCategory(lead.created_at) === activeTab);
    }

    // 3. Search Filter
    if (searchTerm.trim()) {
      const q = searchTerm.toLowerCase();
      list = list.filter(
        (lead) =>
          (lead.author_name && lead.author_name.toLowerCase().includes(q)) ||
          (lead.post_text && lead.post_text.toLowerCase().includes(q))
      );
    }

    // 4. Status Filter
    if (statusFilter !== "all") {
      list = list.filter((lead) => lead.status === statusFilter);
    }

    return list;
  }, [rawLeads, searchTerm, statusFilter, sortOrder, activeTab]);

  // Counts for tabs
  const tabCounts = useMemo(() => {
    const todayCount = rawLeads.filter((l) => getDateCategory(l.created_at) === "today").length;
    const yesterdayCount = rawLeads.filter((l) => getDateCategory(l.created_at) === "yesterday").length;
    const olderCount = rawLeads.filter((l) => getDateCategory(l.created_at) === "older").length;
    return { all: rawLeads.length, today: todayCount, yesterday: yesterdayCount, older: olderCount };
  }, [rawLeads]);

  return (
    <div className="flex-1 space-y-6 p-4 md:p-8 pt-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            Leads Directory <Sparkles className="h-6 w-6 text-blue-500" />
          </h2>
          <p className="text-sm text-muted-foreground">
            Explore, filter, and review extracted high-intent sales leads
          </p>
        </div>
        <Badge variant="outline" className="px-3 py-1 text-xs font-semibold">
          Total Found: {processedLeads.length}
        </Badge>
      </div>

      {/* Datewise Segregation Tabs */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b pb-4">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full sm:w-auto">
          <TabsList className="grid grid-cols-4 w-full sm:w-auto">
            <TabsTrigger value="all" className="gap-1.5 text-xs font-semibold">
              All <Badge variant="secondary" className="ml-1 text-[10px] px-1.5">{tabCounts.all}</Badge>
            </TabsTrigger>
            <TabsTrigger value="today" className="gap-1.5 text-xs font-semibold">
              Today <Badge variant="secondary" className="ml-1 text-[10px] px-1.5">{tabCounts.today}</Badge>
            </TabsTrigger>
            <TabsTrigger value="yesterday" className="gap-1.5 text-xs font-semibold">
              Yesterday <Badge variant="secondary" className="ml-1 text-[10px] px-1.5">{tabCounts.yesterday}</Badge>
            </TabsTrigger>
            <TabsTrigger value="older" className="gap-1.5 text-xs font-semibold">
              Older <Badge variant="secondary" className="ml-1 text-[10px] px-1.5">{tabCounts.older}</Badge>
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {/* Filters & Search Control Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 bg-muted/30 p-3.5 rounded-xl border">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search author or text..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-9 text-sm"
          />
        </div>

        {/* Status Filter */}
        <Select value={statusFilter} onValueChange={(val) => setStatusFilter(val || "all")}>
          <SelectTrigger className="text-sm">
            <Filter className="h-3.5 w-3.5 mr-2 text-muted-foreground" />
            <SelectValue placeholder="Filter Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Statuses</SelectItem>
            <SelectItem value="NEW">New Leads</SelectItem>
            <SelectItem value="REVIEWED">Reviewed</SelectItem>
          </SelectContent>
        </Select>

        {/* Sort Order */}
        <Select value={sortOrder} onValueChange={(val) => setSortOrder((val as "desc" | "asc") || "desc")}>
          <SelectTrigger className="text-sm">
            <Calendar className="h-3.5 w-3.5 mr-2 text-muted-foreground" />
            <SelectValue placeholder="Sort Order" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="desc">Newest First (Desc)</SelectItem>
            <SelectItem value="asc">Oldest First (Asc)</SelectItem>
          </SelectContent>
        </Select>

        {/* Reset Button */}
        <button
          onClick={() => {
            setSearchTerm("");
            setStatusFilter("all");
            setSortOrder("desc");
            setActiveTab("all");
          }}
          className="text-xs font-medium text-muted-foreground hover:text-foreground transition-colors self-center text-center py-2"
        >
          Reset Filters
        </button>
      </div>

      {/* Leads Table */}
      <div className="space-y-4">
        <DataTable columns={leadColumns} data={processedLeads} isLoading={isLoading} />
      </div>
    </div>
  );
}
