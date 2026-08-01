"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useMutation } from "@tanstack/react-query";
import { authService } from "@/services/auth.service";
import { toast } from "sonner";
import { Radar } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const mutation = useMutation({
    mutationFn: (data: LoginFormValues) => {
      const params = new URLSearchParams();
      params.append("username", data.email);
      params.append("password", data.password);
      return authService.login(params);
    },
    onSuccess: (res: any) => {
      toast.success("Login successful");
      const token = res?.data?.data?.access_token || res?.data?.access_token;
      if (token) {
        document.cookie = `access_token=Bearer ${token}; path=/; max-age=86400; SameSite=Lax`;
        if (typeof window !== "undefined") {
          localStorage.setItem("access_token", token);
        }
      }
      const searchParams = new URLSearchParams(window.location.search);
      const redirectPath = searchParams.get("redirect") || "/dashboard/leads";
      window.location.href = redirectPath;
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || "Failed to login");
    },
  });

  const onSubmit = (data: LoginFormValues) => {
    mutation.mutate(data);
  };

  return (
    <div className="flex h-screen w-full items-center justify-center bg-muted/40 px-4">
      <Card className="w-full max-w-sm">
        <CardHeader className="space-y-1 items-center">
          <div className="flex items-center gap-2 font-semibold mb-2">
            <Radar className="h-6 w-6 text-primary" />
            <span className="text-xl">LeadRadar AI</span>
          </div>
          <CardTitle className="text-2xl text-center">Sign in</CardTitle>
          <CardDescription className="text-center">
            Enter your email and password to access the dashboard
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="admin@runtime.com"
                {...register("email")}
              />
              {errors.email && (
                <p className="text-sm text-destructive">{errors.email.message}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                {...register("password")}
              />
              {errors.password && (
                <p className="text-sm text-destructive">{errors.password.message}</p>
              )}
            </div>
            <Button className="w-full" type="submit" disabled={mutation.isPending}>
              {mutation.isPending ? "Signing in..." : "Sign in"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
