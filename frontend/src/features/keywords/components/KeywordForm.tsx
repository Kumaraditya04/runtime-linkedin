"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { keywordSchema, KeywordFormValues } from "../schemas";
import { Keyword } from "../types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

interface KeywordFormProps {
  initialData?: Keyword;
  onSubmit: (data: KeywordFormValues) => void;
  isLoading?: boolean;
}

export function KeywordForm({ initialData, onSubmit, isLoading }: KeywordFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<KeywordFormValues>({
    resolver: zodResolver(keywordSchema),
    defaultValues: initialData || {
      keyword: "",
      category: "",
      source: "LinkedIn",
      priority: 1,
      status: "ACTIVE",
      search_type: "exact",
      notes: "",
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="keyword">Keyword</Label>
        <Input id="keyword" placeholder="e.g. Next.js Developer" {...register("keyword")} />
        {errors.keyword && <p className="text-sm text-destructive">{errors.keyword.message}</p>}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="category">Category</Label>
          <Input id="category" placeholder="e.g. Hiring" {...register("category")} />
          {errors.category && <p className="text-sm text-destructive">{errors.category.message}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="priority">Priority (1-5)</Label>
          <Input id="priority" type="number" min="1" max="5" {...register("priority", { valueAsNumber: true })} />
          {errors.priority && <p className="text-sm text-destructive">{errors.priority.message}</p>}
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="notes">Notes</Label>
        <Textarea id="notes" placeholder="Internal notes about this keyword..." {...register("notes")} />
        {errors.notes && <p className="text-sm text-destructive">{errors.notes.message}</p>}
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button type="submit" disabled={isLoading}>
          {isLoading ? "Saving..." : initialData ? "Update Keyword" : "Create Keyword"}
        </Button>
      </div>
    </form>
  );
}
