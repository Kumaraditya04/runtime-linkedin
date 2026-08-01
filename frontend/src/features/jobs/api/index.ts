import { http } from "@/lib/http";
import { JobExecution } from "../types";

export const getJobs = async (): Promise<JobExecution[]> => {
  const { data } = await http.get("/admin/jobs");
  return data;
};
