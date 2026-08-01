import { useQuery } from "@tanstack/react-query";
import { getLeads, getLead } from "../api";

export const useLeads = (params?: Record<string, any>) => {
  return useQuery({
    queryKey: ["leads", params],
    queryFn: () => getLeads(params),
  });
};

export const useLead = (id: number) => {
  return useQuery({
    queryKey: ["leads", id],
    queryFn: () => getLead(id),
    enabled: !!id,
  });
};
