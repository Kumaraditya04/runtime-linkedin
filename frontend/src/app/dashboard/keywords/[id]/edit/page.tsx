"use client";

import { use } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { KeywordForm } from "@/features/keywords/components/KeywordForm";
import { useKeyword, useUpdateKeyword } from "@/features/keywords/hooks";
import { KeywordFormValues } from "@/features/keywords/schemas";

export default function EditKeywordPage({ params }: { params: Promise<{ id: string }> }) {
  const router = useRouter();
  const resolvedParams = use(params);
  const keywordId = parseInt(resolvedParams.id, 10);
  
  const { data: keyword, isLoading: isFetching } = useKeyword(keywordId);
  const mutation = useUpdateKeyword();

  const handleSubmit = (data: KeywordFormValues) => {
    mutation.mutate(
      { id: keywordId, payload: data },
      {
        onSuccess: () => {
          toast.success("Keyword updated successfully");
          router.push("/dashboard/keywords");
        },
        onError: (error: any) => {
          toast.error(error?.response?.data?.detail || "Failed to update keyword");
        },
      }
    );
  };

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Edit Keyword</h2>
      </div>
      <div className="mx-auto max-w-2xl mt-8">
        {isFetching ? (
          <div>Loading...</div>
        ) : keyword ? (
          <KeywordForm initialData={keyword} onSubmit={handleSubmit} isLoading={mutation.isPending} />
        ) : (
          <div>Keyword not found.</div>
        )}
      </div>
    </div>
  );
}
