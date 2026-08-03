import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getJobs, cancelJob } from "../api";

export const useJobs = () => {
  return useQuery({
    queryKey: ["jobs"],
    queryFn: getJobs,
    refetchInterval: 5000,
  });
};

export const useCancelJob = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: cancelJob,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["jobs"] }),
  });
};
