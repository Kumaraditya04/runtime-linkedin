import { useMutation } from "@tanstack/react-query";
import { runCrawler } from "../api";

export const useRunCrawler = () => {
  return useMutation({
    mutationFn: runCrawler,
  });
};
