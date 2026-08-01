import { useMutation } from "@tanstack/react-query";
import { runCrawler, runAllCrawlers } from "../api";

export const useRunCrawler = () => {
  return useMutation({
    mutationFn: (keywordId: number) => runCrawler(keywordId),
  });
};

export const useRunAllCrawlers = () => {
  return useMutation({
    mutationFn: () => runAllCrawlers(),
  });
};
