import { ColumnDef } from "@tanstack/react-table";
import { JobExecution } from "../types";
import { Badge } from "@/components/ui/badge";
import { formatIST } from "@/lib/date";

export const jobColumns: ColumnDef<JobExecution>[] = [
  {
    accessorKey: "keyword_id",
    header: "Keyword ID",
  },
  {
    accessorKey: "job_type",
    header: "Type",
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
    accessorKey: "started_at",
    header: "Started (IST)",
    cell: ({ row }) => {
      const date = row.getValue("started_at") as string;
      return <span className="font-mono text-xs text-muted-foreground">{formatIST(date)}</span>;
    },
  },
];
