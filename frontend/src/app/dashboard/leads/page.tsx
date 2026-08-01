"use client";

import { DataTable } from "@/components/shared/DataTable";
import { leadColumns } from "@/features/leads/components/LeadColumns";
import { useLeads } from "@/features/leads/hooks";

export default function LeadsPage() {
  const { data: leads = [], isLoading } = useLeads();

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Leads</h2>
      </div>
      <div className="space-y-4">
        <DataTable columns={leadColumns} data={leads} isLoading={isLoading} />
      </div>
    </div>
  );
}
