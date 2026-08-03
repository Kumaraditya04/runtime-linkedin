"use client";

import { useState, useMemo } from "react";
import { DataTable } from "@/components/shared/DataTable";
import { leadColumns } from "@/features/leads/components/LeadColumns";
import { useLeads } from "@/features/leads/hooks";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, Filter, Calendar, Sparkles, User, ExternalLink, Eye, Clock, MessageSquareText } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

// Helper function to format date string to IST
function formatIST(dateStr: string | null | undefined) {
  if (!dateStr) return "N/A";
  try {
    let s = String(dateStr).trim();
    if (s.includes(" ") && !s.includes("T")) s = s.replace(" ", "T");
    if (!s.endsWith("Z") && !s.includes("+")) s += "Z";
    const date = new Date(s);
    if (isNaN(date.getTime())) return "N/A";
    return date.toLocaleString("en-IN", {
      timeZone: "Asia/Kolkata",
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
  } catch (e) {
    return "N/A";
  }
}

export default function LeadsPage() {
  const { data: rawLeads = [], isLoading } = useLeads();
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [sortOrder, setSortOrder] = useState<"desc" | "asc">("desc");
  const [activeTab, setActiveTab] = useState("all");

  const getDateCategory = (dateStr: string) => {
    let s = String(dateStr).trim();
    if (s.includes(" ") && !s.includes("T")) s = s.replace(" ", "T");
    if (!s.endsWith("Z") && !s.includes("+")) s += "Z";
    const d = new Date(s);

    // Compare dates in IST (Asia/Kolkata) to avoid UTC midnight off-by-one
    const toISTDateStr = (date: Date) =>
      date.toLocaleDateString("en-CA", { timeZone: "Asia/Kolkata" }); // YYYY-MM-DD

    const todayIST = toISTDateStr(new Date());
    const dIST = toISTDateStr(d);

    const yesterdayDate = new Date();
    yesterdayDate.setDate(yesterdayDate.getDate() - 1);
    const yesterdayIST = toISTDateStr(yesterdayDate);

    if (dIST === todayIST) return "today";
    if (dIST === yesterdayIST) return "yesterday";
    return "older";
  };

  const processedLeads = useMemo(() => {
    let list = [...rawLeads];

    list.sort((a, b) => {
      const timeA = new Date(a.created_at || 0).getTime();
      const timeB = new Date(b.created_at || 0).getTime();
      return sortOrder === "desc" ? timeB - timeA : timeA - timeB;
    });

    if (activeTab !== "all") {
      list = list.filter((lead) => getDateCategory(lead.created_at) === activeTab);
    }

    if (searchTerm.trim()) {
      const q = searchTerm.toLowerCase();
      list = list.filter(
        (lead) =>
          (lead.author_name && lead.author_name.toLowerCase().includes(q)) ||
          (lead.post_text && lead.post_text.toLowerCase().includes(q))
      );
    }

    if (statusFilter !== "all") {
      list = list.filter((lead) => lead.status === statusFilter);
    }

    return list;
  }, [rawLeads, searchTerm, statusFilter, sortOrder, activeTab]);

  const tabCounts = useMemo(() => {
    const todayCount = rawLeads.filter((l) => getDateCategory(l.created_at) === "today").length;
    const yesterdayCount = rawLeads.filter((l) => getDateCategory(l.created_at) === "yesterday").length;
    const olderCount = rawLeads.filter((l) => getDateCategory(l.created_at) === "older").length;
    return { all: rawLeads.length, today: todayCount, yesterday: yesterdayCount, older: olderCount };
  }, [rawLeads]);

  return (
    <div className="flex-1 space-y-4 sm:space-y-6 p-3 sm:p-6 md:p-8 pt-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 sm:gap-4">
        <div>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight flex items-center gap-2">
            Leads Directory <Sparkles className="h-5 w-5 sm:h-6 sm:w-6 text-blue-500" />
          </h2>
          <p className="text-xs sm:text-sm text-muted-foreground">
            Explore, filter, and review extracted sales leads on mobile & desktop
          </p>
        </div>
        <Badge variant="outline" className="px-2.5 py-1 text-xs font-semibold self-start sm:self-auto">
          Found: {processedLeads.length}
        </Badge>
      </div>

      {/* Datewise Segregation Tabs */}
      <div className="border-b pb-3 overflow-x-auto">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid grid-cols-4 w-full min-w-[320px]">
            <TabsTrigger value="all" className="text-xs font-semibold px-1 py-1.5">
              All <Badge variant="secondary" className="ml-1 text-[10px] px-1">{tabCounts.all}</Badge>
            </TabsTrigger>
            <TabsTrigger value="today" className="text-xs font-semibold px-1 py-1.5">
              Today <Badge variant="secondary" className="ml-1 text-[10px] px-1">{tabCounts.today}</Badge>
            </TabsTrigger>
            <TabsTrigger value="yesterday" className="text-xs font-semibold px-1 py-1.5">
              Yesterday <Badge variant="secondary" className="ml-1 text-[10px] px-1">{tabCounts.yesterday}</Badge>
            </TabsTrigger>
            <TabsTrigger value="older" className="text-xs font-semibold px-1 py-1.5">
              Older <Badge variant="secondary" className="ml-1 text-[10px] px-1">{tabCounts.older}</Badge>
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {/* Filters Control Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 bg-muted/30 p-3 rounded-xl border">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search author or text..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-9 text-xs sm:text-sm h-9"
          />
        </div>

        {/* Status Filter */}
        <Select value={statusFilter} onValueChange={(val) => setStatusFilter(val || "all")}>
          <SelectTrigger className="text-xs sm:text-sm h-9">
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
          <SelectTrigger className="text-xs sm:text-sm h-9">
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
          className="text-xs font-medium text-muted-foreground hover:text-foreground transition-colors text-center py-1.5"
        >
          Reset Filters
        </button>
      </div>

      {/* MOBILE CARD VIEW (Visible on Mobile Screens < 768px) */}
      <div className="grid grid-cols-1 gap-3 md:hidden">
        {isLoading ? (
          <div className="text-center py-8 text-sm text-muted-foreground">Loading leads...</div>
        ) : processedLeads.length ? (
          processedLeads.map((lead) => {
            const postUrl = lead.post_url || lead.author_url;
            const postAge = lead.normalized_data?.published_at_str;

            return (
              <div
                key={lead.id}
                className="rounded-xl border bg-card p-4 shadow-sm space-y-3 relative transition-all hover:border-primary/50"
              >
                {/* Header: Author & Direct Link */}
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span className="font-semibold text-sm text-foreground">{lead.author_name || "Unknown Author"}</span>
                      {lead.author_url && (
                        <a
                          href={lead.author_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-muted-foreground hover:text-primary"
                          title="LinkedIn Profile"
                        >
                          <User className="h-3.5 w-3.5" />
                        </a>
                      )}
                    </div>
                    <span className="text-[11px] text-muted-foreground flex items-center gap-1 mt-0.5">
                      <Clock className="h-3 w-3" /> {postAge ? `${postAge} ago` : formatIST(lead.created_at)}
                    </span>
                  </div>

                  {postUrl && (
                    <a
                      href={postUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/60 px-2.5 py-1 rounded-md border border-blue-200 dark:border-blue-800"
                    >
                      View Post <ExternalLink className="h-3 w-3" />
                    </a>
                  )}
                </div>

                {/* Content Snippet */}
                <p className="text-xs text-muted-foreground line-clamp-3 leading-relaxed font-sans bg-muted/30 p-2.5 rounded-lg border border-border/50">
                  {lead.post_text || "No post text available."}
                </p>

                {/* Footer Controls */}
                <div className="flex items-center justify-between pt-1 text-xs">
                  <div className="flex items-center gap-2">
                    <Badge variant={lead.status === "NEW" ? "default" : "outline"} className="text-[10px] px-2 py-0.5">
                      {lead.status}
                    </Badge>
                    <Badge variant="outline" className="text-[10px] px-2 py-0.5 capitalize">
                      {lead.source}
                    </Badge>
                  </div>

                  {/* Detail Modal Trigger */}
                  <Dialog>
                    <DialogTrigger className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline px-2 py-1 rounded-md bg-muted">
                      <Eye className="h-3.5 w-3.5" /> Inspect
                    </DialogTrigger>
                    <DialogContent className="max-w-md w-[92vw] max-h-[85vh] overflow-y-auto rounded-xl">
                      <DialogHeader>
                        <DialogTitle className="text-lg font-bold">
                          {lead.author_name || "Lead Details"}
                        </DialogTitle>
                        <DialogDescription className="text-xs">
                          Posted {postAge ? `${postAge} ago` : "recently"} • {formatIST(lead.created_at)} (IST)
                        </DialogDescription>
                      </DialogHeader>

                      <div className="space-y-4 py-2">
                        <div>
                          <h4 className="text-xs font-semibold mb-1.5 flex items-center gap-1 text-muted-foreground">
                            <MessageSquareText className="h-3.5 w-3.5" /> Full Post Content
                          </h4>
                          <div className="rounded-lg bg-muted p-3 text-xs whitespace-pre-wrap leading-relaxed border">
                            {lead.post_text || "No post text available."}
                          </div>
                        </div>

                        {postUrl && (
                          <a
                            href={postUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center justify-center w-full gap-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 py-2.5 rounded-lg transition-colors"
                          >
                            Open Original LinkedIn Post <ExternalLink className="h-3.5 w-3.5" />
                          </a>
                        )}
                      </div>
                    </DialogContent>
                  </Dialog>
                </div>
              </div>
            );
          })
        ) : (
          <div className="text-center py-8 text-sm text-muted-foreground">No leads found.</div>
        )}
      </div>

      {/* DESKTOP TABLE VIEW (Visible on Screens >= 768px) */}
      <div className="hidden md:block space-y-4">
        <DataTable columns={leadColumns} data={processedLeads} isLoading={isLoading} />
      </div>
    </div>
  );
}
