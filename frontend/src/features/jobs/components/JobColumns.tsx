import { ColumnDef } from "@tanstack/react-table";
import { JobExecution } from "../types";
import { Badge } from "@/components/ui/badge";
import { formatIST } from "@/lib/date";

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
];
