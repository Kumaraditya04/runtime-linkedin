export interface JobExecution {
  id: number;
  job_type: string;
  keyword_id: number | null;
  status: string;
  started_at: string | null;
  finished_at: string | null;
  duration_ms: number | null;
  records_found: number;
  error_message: string | null;
}
