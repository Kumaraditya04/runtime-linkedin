import { KeywordFormValues } from "../schemas";

export type { KeywordFormValues };
export type KeywordStatus = "ACTIVE" | "PAUSED" | "ARCHIVED";

export interface Keyword extends KeywordFormValues {
  id: number;
  last_run_at: string | null;
  last_result_count: number;
  created_at: string;
  updated_at: string;
  created_by: number | null;
  updated_by: number | null;
}
