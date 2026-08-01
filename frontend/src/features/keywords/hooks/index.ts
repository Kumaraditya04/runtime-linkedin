import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getKeywords,
  getKeyword,
  createKeyword,
  updateKeyword,
  deleteKeyword,
  pauseKeyword,
  resumeKeyword,
} from "../api";
import { KeywordFormValues } from "../types";

export const useKeywords = (params?: Record<string, any>) => {
  return useQuery({
    queryKey: ["keywords", params],
    queryFn: () => getKeywords(params),
  });
};

export const useKeyword = (id: number) => {
  return useQuery({
    queryKey: ["keywords", id],
    queryFn: () => getKeyword(id),
    enabled: !!id,
  });
};

export const useCreateKeyword = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: KeywordFormValues) => createKeyword(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["keywords"] });
    },
  });
};

export const useUpdateKeyword = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: Partial<KeywordFormValues> }) =>
      updateKeyword({ id, payload }),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["keywords"] });
      queryClient.invalidateQueries({ queryKey: ["keywords", variables.id] });
    },
  });
};

export const useDeleteKeyword = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteKeyword(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["keywords"] });
    },
  });
};

export const usePauseKeyword = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => pauseKeyword(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ["keywords"] });
      queryClient.invalidateQueries({ queryKey: ["keywords", id] });
    },
  });
};

export const useResumeKeyword = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => resumeKeyword(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ["keywords"] });
      queryClient.invalidateQueries({ queryKey: ["keywords", id] });
    },
  });
};
