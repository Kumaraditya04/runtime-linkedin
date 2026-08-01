import * as z from "zod";

export const keywordSchema = z.object({
  keyword: z.string().min(1, "Keyword is required"),
  category: z.string().optional(),
  source: z.string().default("LinkedIn"),
  priority: z.number().int().min(1).max(5).default(1),
  status: z.enum(["ACTIVE", "PAUSED", "ARCHIVED"]).default("ACTIVE"),
  search_type: z.string().default("exact"),
  notes: z.string().optional(),
});

export type KeywordFormValues = z.infer<typeof keywordSchema>;
