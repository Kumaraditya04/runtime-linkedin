import { http } from "@/lib/http";
import { JobExecution } from "../types";

export const getJobs = async (): Promise<JobExecution[]> => {
  const { data } = await http.get("/admin/jobs");
  return data;
};

export const cancelJob = async (jobId: number): Promise<void> => {
  await http.post(`/admin/jobs/${jobId}/cancel`);
};
