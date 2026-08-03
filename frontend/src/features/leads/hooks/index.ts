import { useQuery } from "@tanstack/react-query";
import { getLeads, getLead } from "../api";

export const useLeads = (params?: Record<string, any>) => {
  return useQuery({
    queryKey: ["leads", params],
    queryFn: () => getLeads(params),
    refetchInterval: 15000, // auto-refresh every 15s while page is open
    refetchOnWindowFocus: true,
  });
};

export const useLead = (id: number) => {
  return useQuery({
    queryKey: ["leads", id],
    queryFn: () => getLead(id),
    enabled: !!id,
  });
};
