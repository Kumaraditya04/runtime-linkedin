import { http } from "@/lib/http";
import { Lead } from "../types";

export const getLeads = async (params?: Record<string, any>): Promise<Lead[]> => {
  const { data } = await http.get("/admin/leads", { params });
  return data;
};

export const getLead = async (id: number): Promise<Lead> => {
  const { data } = await http.get(`/admin/leads/${id}`);
  return data;
};
