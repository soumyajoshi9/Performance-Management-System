"use client";

import React from "react";
import { useAuth } from "@/context/auth-context";
import { UserRole } from "@/types";
import { 
  Building2, Calendar, ShieldCheck, ChevronDown, UserCircle2, LogOut 
} from "lucide-react";

export function TopNav() {
  const { user, switchRole, logout } = useAuth();
  const [roleMenuOpen, setRoleMenuOpen] = React.useState(false);

  const roles: UserRole[] = ["EMPLOYEE", "MANAGER", "HR", "ADMIN"];

  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 px-6 flex items-center justify-between z-20 sticky top-0">
      {/* Brand & Organization */}
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30">
            V
          </div>
          <div>
            <span className="font-bold tracking-wider text-lg text-white">VYORA</span>
            <span className="hidden sm:inline-block ml-2 text-xs bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded border border-indigo-800">
              Intelligence
            </span>
          </div>
        </div>

        <div className="hidden md:flex items-center gap-2 text-xs text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-md border border-slate-700/60">
          <Building2 className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-300 font-medium">Acme Corp</span>
          <span className="text-slate-600">|</span>
          <span className="text-slate-400">Engineering</span>
        </div>
      </div>

      {/* Center - Active Review Period */}
      <div className="hidden lg:flex items-center gap-2 bg-slate-850 px-3 py-1.5 rounded-full border border-slate-700/80 text-xs">
        <Calendar className="w-3.5 h-3.5 text-indigo-400" />
        <span className="text-slate-300">Period: <strong className="text-white">November 2026</strong></span>
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span className="text-emerald-400 font-medium">Active (8 days left)</span>
      </div>

      {/* Right - Role Switcher & User Profile */}
      <div className="flex items-center gap-4">
        {/* Role Switcher Pill for Demo Experience */}
        <div className="relative">
          <button
            onClick={() => setRoleMenuOpen(!roleMenuOpen)}
            className="flex items-center gap-1.5 text-xs bg-indigo-900/40 hover:bg-indigo-900/70 border border-indigo-700/50 text-indigo-200 px-2.5 py-1.5 rounded-md transition-colors"
            title="Switch demo persona"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
            <span className="font-semibold">{user?.role || "ROLE"}</span>
            <ChevronDown className="w-3 h-3 text-indigo-400" />
          </button>

          {roleMenuOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-slate-900 border border-slate-700 rounded-lg shadow-2xl p-1 z-50">
              <div className="px-2 py-1 text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                Switch Role View
              </div>
              {roles.map((r) => (
                <button
                  key={r}
                  onClick={() => {
                    switchRole(r);
                    setRoleMenuOpen(false);
                  }}
                  className={`w-full text-left px-2.5 py-1.5 text-xs rounded transition-colors flex items-center justify-between ${
                    user?.role === r 
                      ? "bg-indigo-600 text-white font-medium" 
                      : "text-slate-300 hover:bg-slate-800"
                  }`}
                >
                  <span>{r}</span>
                  {user?.role === r && <span className="text-[10px] opacity-75">Active</span>}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* User Profile Pill */}
        <div className="flex items-center gap-2 pl-2 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-slate-300 border border-slate-700">
            <UserCircle2 className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="hidden sm:block text-left">
            <div className="text-xs font-medium text-white">{user?.full_name || "Guest User"}</div>
            <div className="text-[10px] text-slate-400">{user?.email || "Signed in"}</div>
          </div>
          <button 
            onClick={logout}
            className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-md transition-colors ml-1"
            title="Sign out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
