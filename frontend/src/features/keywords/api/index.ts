import { http } from "@/lib/http";
import { Keyword, KeywordFormValues } from "../types";

export const getKeywords = async (params?: Record<string, any>): Promise<Keyword[]> => {
  const { data } = await http.get("/admin/keywords", { params });
  return data;
};

export const getKeyword = async (id: number): Promise<Keyword> => {
  const { data } = await http.get(`/admin/keywords/${id}`);
  return data;
};

export const createKeyword = async (payload: KeywordFormValues): Promise<Keyword> => {
  const { data } = await http.post("/admin/keywords", payload);
  return data;
};

export const updateKeyword = async ({ id, payload }: { id: number; payload: Partial<KeywordFormValues> }): Promise<Keyword> => {
  const { data } = await http.put(`/admin/keywords/${id}`, payload);
  return data;
};

export const deleteKeyword = async (id: number): Promise<void> => {
  await http.delete(`/admin/keywords/${id}`);
};

export const pauseKeyword = async (id: number): Promise<Keyword> => {
  const { data } = await http.post(`/admin/keywords/${id}/pause`);
  return data;
};

export const resumeKeyword = async (id: number): Promise<Keyword> => {
  const { data } = await http.post(`/admin/keywords/${id}/resume`);
  return data;
};
