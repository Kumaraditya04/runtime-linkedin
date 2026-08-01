"use client";

import { ColumnDef } from "@tanstack/react-table";
import { Lead } from "../types";
import { Badge } from "@/components/ui/badge";
import { ExternalLink, Eye, MessageSquareText, User, Clock } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

// Helper function to format date/time in Indian Standard Time (IST)
function formatIST(dateStr: string | null | undefined, includeTime = true) {
  if (!dateStr) return "N/A";
  try {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return "N/A";
    
    if (includeTime) {
      return date.toLocaleString("en-IN", {
        timeZone: "Asia/Kolkata",
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      });
    }
    return date.toLocaleDateString("en-IN", {
      timeZone: "Asia/Kolkata",
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  } catch (e) {
    return "N/A";
  }
}

export const leadColumns: ColumnDef<Lead>[] = [
  {
    accessorKey: "source",
    header: "Source",
    cell: ({ row }) => (
      <Badge variant="outline" className="capitalize font-semibold">
        {row.getValue("source")}
      </Badge>
    ),
  },
  {
    accessorKey: "author_name",
    header: "Author / Prospect",
    cell: ({ row }) => {
      const name = (row.getValue("author_name") as string) || "Unknown Author";
      const profileUrl = row.original.author_url;

      return (
        <div className="flex items-center gap-2">
          <span className="font-semibold text-foreground">{name}</span>
          {profileUrl && profileUrl.startsWith("http") && (
            <a
              href={profileUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-primary transition-colors inline-flex items-center"
              title="Open LinkedIn Profile"
            >
              <User className="h-3.5 w-3.5" />
            </a>
          )}
        </div>
      );
    },
  },
  {
    accessorKey: "post_text",
    header: "Post Snippet",
    cell: ({ row }) => {
      const text = (row.getValue("post_text") as string) || "";
      const snippet = text.length > 80 ? `${text.substring(0, 80)}...` : text;
      return (
        <p className="max-w-xs text-sm text-muted-foreground line-clamp-2">
          {snippet || "No text available"}
        </p>
      );
    },
  },
  {
    id: "posted_at",
    header: "Posted",
    cell: ({ row }) => {
      const norm = row.original.normalized_data;
      const postAge = norm?.published_at_str;
      return (
        <span className="text-xs font-medium text-muted-foreground flex items-center gap-1">
          <Clock className="h-3 w-3" />
          {postAge ? `${postAge} ago` : "Recent"}
        </span>
      );
    },
  },
  {
    accessorKey: "post_url",
    header: "Direct Post Link",
    cell: ({ row }) => {
      const postUrl = (row.getValue("post_url") as string) || row.original.author_url;

      if (!postUrl || !postUrl.startsWith("http")) {
        return <span className="text-xs text-muted-foreground">N/A</span>;
      }

      return (
        <a
          href={postUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 hover:underline bg-blue-50 dark:bg-blue-950/50 px-2.5 py-1 rounded-md border border-blue-200 dark:border-blue-800 transition-colors"
        >
          View Post
          <ExternalLink className="h-3 w-3" />
        </a>
      );
    },
  },
  {
    accessorKey: "intent_score",
    header: "Intent Score",
    cell: ({ row }) => {
      const score = row.getValue("intent_score") as number | null;
      if (score === null || score === undefined) {
        return <Badge variant="secondary">Unscored</Badge>;
      }
      const variant = score >= 70 ? "default" : score >= 40 ? "secondary" : "outline";
      return <Badge variant={variant as any}>{score} / 100</Badge>;
    },
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as string;
      const variant =
        status === "NEW" ? "default" : status === "REVIEWED" ? "secondary" : "outline";
      return <Badge variant={variant as any}>{status}</Badge>;
    },
  },
  {
    accessorKey: "created_at",
    header: "Discovered (IST)",
    cell: ({ row }) => {
      const dateVal = row.getValue("created_at") as string;
      return (
        <span className="text-xs text-muted-foreground font-mono">
          {formatIST(dateVal)}
        </span>
      );
    },
  },
  {
    id: "actions",
    header: "Actions",
    cell: ({ row }) => {
      const lead = row.original;
      const postUrl = lead.post_url || lead.author_url;
      const postAge = lead.normalized_data?.published_at_str;

      return (
        <Dialog>
          <DialogTrigger className="inline-flex items-center justify-center h-8 w-8 rounded-md hover:bg-accent text-muted-foreground hover:text-accent-foreground transition-colors">
            <Eye className="h-4 w-4" />
            <span className="sr-only">View lead details</span>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle className="flex items-center justify-between gap-4 text-xl">
                <span>{lead.author_name || "Lead Details"}</span>
                <div className="flex items-center gap-2">
                  {lead.author_url && (
                    <a
                      href={lead.author_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs font-medium text-muted-foreground hover:text-primary border rounded-md px-2.5 py-1"
                    >
                      Profile <User className="h-3 w-3" />
                    </a>
                  )}
                  {postUrl && (
                    <a
                      href={postUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-md px-3 py-1.5 transition-colors"
                    >
                      View Exact Post <ExternalLink className="h-3.5 w-3.5" />
                    </a>
                  )}
                </div>
              </DialogTitle>
              <DialogDescription>
                Posted {postAge ? `${postAge} ago` : "recently"} • Discovered: {formatIST(lead.created_at)} (IST) • Source: {lead.source}
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-4 py-2">
              <div>
                <h4 className="text-sm font-semibold mb-2 flex items-center gap-1.5 text-muted-foreground">
                  <MessageSquareText className="h-4 w-4" /> Post Content
                </h4>
                <div className="rounded-lg bg-muted p-4 text-sm whitespace-pre-wrap font-sans leading-relaxed border">
                  {lead.post_text || "No post text available."}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm pt-2">
                <div>
                  <span className="font-semibold text-muted-foreground">Status:</span>{" "}
                  <Badge variant="outline">{lead.status}</Badge>
                </div>
                <div>
                  <span className="font-semibold text-muted-foreground">Intent Score:</span>{" "}
                  {lead.intent_score !== null ? `${lead.intent_score} / 100` : "Not Scored Yet"}
                </div>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      );
    },
  },
];
