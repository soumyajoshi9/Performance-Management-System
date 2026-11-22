"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/auth-context";
import { UserRole } from "@/types";
import { ShieldCheck, ArrowRight, Lock, Mail, AlertCircle } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const { login, switchRole } = useAuth();
  const [email, setEmail] = useState("employee@vyora.local");
  const [password, setPassword] = useState("EmployeePass123!");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      await login(email);
      router.push("/dashboard/employee");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Invalid email or credentials");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleQuickLogin = async (role: UserRole) => {
    setError("");
    setIsSubmitting(true);
    try {
      await switchRole(role);
      if (role === "MANAGER") router.push("/dashboard/manager");
      else if (role === "HR") router.push("/dashboard/hr");
      else if (role === "ADMIN") router.push("/dashboard/admin");
      else router.push("/dashboard/employee");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Quick login failed");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="inline-flex w-12 h-12 rounded-xl bg-indigo-600 items-center justify-center font-black text-2xl text-white shadow-xl shadow-indigo-600/30 mb-3">
          V
        </div>
        <h2 className="text-2xl font-extrabold text-white tracking-tight">VYORA</h2>
        <p className="mt-1 text-xs text-slate-400">
          Smart Performance Management &amp; Employee Development Intelligence
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-slate-900 border border-slate-800 py-8 px-6 shadow-2xl rounded-2xl sm:px-10">
          {error && (
            <div className="mb-4 p-3 bg-rose-950/80 border border-rose-900 rounded-lg text-xs text-rose-300 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
              <span>{error}</span>
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Corporate Email</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  placeholder="name@vyora.local"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all disabled:opacity-50"
            >
              <span>{isSubmitting ? "Authenticating..." : "Sign in with Credentials"}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </form>

          {/* Quick Demo Access Bar */}
          <div className="mt-6 pt-6 border-t border-slate-800">
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider text-center mb-3">
              One-Click Demo Personas
            </div>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => handleQuickLogin("EMPLOYEE")}
                className="p-2 bg-slate-800 hover:bg-indigo-900/40 border border-slate-700 hover:border-indigo-700/60 rounded-lg text-left text-xs transition-colors"
              >
                <div className="font-semibold text-white">Sarah Chen</div>
                <div className="text-[10px] text-slate-400">EMPLOYEE</div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin("MANAGER")}
                className="p-2 bg-slate-800 hover:bg-indigo-900/40 border border-slate-700 hover:border-indigo-700/60 rounded-lg text-left text-xs transition-colors"
              >
                <div className="font-semibold text-white">David Miller</div>
                <div className="text-[10px] text-slate-400">MANAGER</div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin("HR")}
                className="p-2 bg-slate-800 hover:bg-indigo-900/40 border border-slate-700 hover:border-indigo-700/60 rounded-lg text-left text-xs transition-colors"
              >
                <div className="font-semibold text-white">Elena Vance</div>
                <div className="text-[10px] text-slate-400">HR ADMIN</div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin("ADMIN")}
                className="p-2 bg-slate-800 hover:bg-indigo-900/40 border border-slate-700 hover:border-indigo-700/60 rounded-lg text-left text-xs transition-colors"
              >
                <div className="font-semibold text-white">System Admin</div>
                <div className="text-[10px] text-slate-400">ADMIN</div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
