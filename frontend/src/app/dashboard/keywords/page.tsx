"use client";

import Link from "next/link";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DataTable } from "@/components/shared/DataTable";
import { keywordColumns } from "@/features/keywords/components/KeywordColumns";
import { useKeywords } from "@/features/keywords/hooks";

export default function KeywordsPage() {
  const { data: keywords = [], isLoading } = useKeywords();

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Keywords</h2>
        <div className="flex items-center space-x-2">
          <Link href="/dashboard/keywords/new">
            <Button>
              <Plus className="mr-2 h-4 w-4" /> Add Keyword
            </Button>
          </Link>
        </div>
      </div>
      <div className="space-y-4">
        <DataTable columns={keywordColumns} data={keywords} isLoading={isLoading} />
      </div>
    </div>
  );
}
