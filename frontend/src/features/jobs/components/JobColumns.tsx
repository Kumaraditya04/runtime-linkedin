import { ColumnDef } from "@tanstack/react-table";
import { JobExecution } from "../types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatIST } from "@/lib/date";
import { useCancelJob } from "../hooks";
import { Square, Loader2 } from "lucide-react";
import { toast } from "sonner";

const ACTIVE_STATUSES = new Set(["RUNNING", "STARTING", "SAVING", "PARSING"]);

function CancelButton({ jobId }: { jobId: number }) {
  const { mutate, isPending } = useCancelJob();
  return (
    <Button
      variant="destructive"
      size="sm"
      className="h-7 px-2 text-xs gap-1"
      disabled={isPending}
      onClick={() =>
        mutate(jobId, {
          onSuccess: () => toast.success("Job stopped."),
          onError: () => toast.error("Failed to stop job."),
        })
      }
    >
      {isPending ? <Loader2 className="h-3 w-3 animate-spin" /> : <Square className="h-3 w-3" />}
      Stop
    </Button>
  );
}

export const jobColumns: ColumnDef<JobExecution>[] = [
  {
    id: "keyword_name",
    header: "Target Keyword",
    cell: ({ row }) => {
      const name = row.original.keyword_name || (row.original.keyword_id ? `Keyword #${row.original.keyword_id}` : "Global Crawl");
      return <span className="font-semibold text-foreground">{name}</span>;
    },
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as string;
      const variant = status === "COMPLETED" ? "default" : status === "FAILED" ? "destructive" : "secondary";
      return <Badge variant={variant as any}>{status}</Badge>;
    }
  },
  {
    accessorKey: "records_found",
    header: "Found",
  },
  {
    id: "saved",
    header: "Saved / Skipped",
    cell: ({ row }) => {
      const saved = row.original.records_saved ?? 0;
      const skipped = row.original.records_skipped ?? 0;
      return <span className="text-xs font-mono">{saved} saved ({skipped} dupes)</span>;
    },
  },
  {
    accessorKey: "started_at",
    header: "Started (IST)",
    cell: ({ row }) => {
      const date = row.getValue("started_at") as string;
      return <span className="font-mono text-xs text-muted-foreground">{formatIST(date)}</span>;
    },
  },
  {
    id: "actions",
    header: "",
    cell: ({ row }) => {
      if (!ACTIVE_STATUSES.has(row.original.status)) return null;
      return <CancelButton jobId={row.original.id} />;
    },
  },
];
