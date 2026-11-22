"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/auth-context";

export default function RootPage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (user) {
        if (user.role === "MANAGER") router.replace("/dashboard/manager");
        else if (user.role === "HR") router.replace("/dashboard/hr");
        else if (user.role === "ADMIN") router.replace("/dashboard/admin");
        else router.replace("/dashboard/employee");
      } else {
        router.replace("/login");
      }
    }
  }, [user, isLoading, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 text-slate-400">
      <div className="flex items-center gap-3">
        <div className="w-5 h-5 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin"></div>
        <span className="text-sm font-medium">Loading VYORA Intelligence...</span>
      </div>
    </div>
  );
}
