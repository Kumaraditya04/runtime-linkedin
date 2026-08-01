"use client";

import { ColumnDef } from "@tanstack/react-table";
import { Keyword } from "../types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { MoreHorizontal } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export const keywordColumns: ColumnDef<Keyword>[] = [
  {
    accessorKey: "keyword",
    header: "Keyword",
  },
  {
    accessorKey: "category",
    header: "Category",
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as string;
      const variant = status === "ACTIVE" ? "default" : status === "PAUSED" ? "secondary" : "outline";
      return <Badge variant={variant as any}>{status}</Badge>;
    },
  },
  {
    accessorKey: "priority",
    header: "Priority",
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const keyword = row.original;

      return (
        <DropdownMenu>
          <DropdownMenuTrigger>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuItem onClick={() => {
              if (typeof window !== "undefined") {
                window.location.href = `/dashboard/keywords/${keyword.id}/edit`;
              }
            }}>
              Edit
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-destructive">Delete</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    },
  },
];
