import { useQuery } from "@tanstack/react-query";
import { getJobs } from "../api";

export const useJobs = () => {
  return useQuery({
    queryKey: ["jobs"],
    queryFn: getJobs,
    refetchInterval: 5000, // Poll every 5s for MVP real-time feel
  });
};
