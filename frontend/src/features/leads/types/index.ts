export type LeadStatus = "NEW" | "REVIEWED" | "CONTACTED";

export interface Lead {
  id: number;
  source: string;
  keyword_id: number | null;
  author_name: string | null;
  author_url: string | null;
  post_url: string;
  post_text: string | null;
  published_at: string | null;
  intent_score: number | null;
  status: LeadStatus;
  normalized_data: any;
  raw_payload: any;
  crawler_version: string | null;
  parser_version: string | null;
  created_at: string;
  updated_at: string;
}
