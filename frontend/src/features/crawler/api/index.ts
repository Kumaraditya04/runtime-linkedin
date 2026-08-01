import { http } from "@/lib/http";

export const runCrawler = async (keywordId: number): Promise<{ message: string }> => {
  const { data } = await http.post("/admin/crawler/run", { keyword_id: keywordId });
  return data;
};

export const runAllCrawlers = async (): Promise<{ message: string }> => {
  const { data } = await http.post("/admin/crawler/run-all");
  return data;
};
