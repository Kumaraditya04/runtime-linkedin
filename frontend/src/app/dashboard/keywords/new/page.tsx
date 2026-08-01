"use client";

import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { KeywordForm } from "@/features/keywords/components/KeywordForm";
import { useCreateKeyword } from "@/features/keywords/hooks";
import { KeywordFormValues } from "@/features/keywords/schemas";

export default function NewKeywordPage() {
  const router = useRouter();
  const mutation = useCreateKeyword();

  const handleSubmit = (data: KeywordFormValues) => {
    mutation.mutate(data, {
      onSuccess: () => {
        toast.success("Keyword created successfully");
        router.push("/dashboard/keywords");
      },
      onError: (error: any) => {
        toast.error(error?.response?.data?.detail || "Failed to create keyword");
      },
    });
  };

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Create Keyword</h2>
      </div>
      <div className="mx-auto max-w-2xl mt-8">
        <KeywordForm onSubmit={handleSubmit} isLoading={mutation.isPending} />
      </div>
    </div>
  );
}
