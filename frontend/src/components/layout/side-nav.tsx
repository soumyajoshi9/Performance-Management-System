"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/auth-context";
import { 
  LayoutDashboard, Target, CheckSquare, Award, TrendingUp,
  Users, ClipboardCheck, Scale, FileText, Settings, ShieldAlert
} from "lucide-react";

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
}

export function SideNav() {
  const pathname = usePathname();
  const { user } = useAuth();

  const getNavItems = (): NavItem[] => {
    switch (user?.role) {
      case "EMPLOYEE":
        return [
          { label: "Overview", href: "/dashboard/employee", icon: <LayoutDashboard className="w-4 h-4" /> },
          { label: "Goals Tracker", href: "/dashboard/employee/goals", icon: <Target className="w-4 h-4" /> },
          { label: "Tasks & Blockers", href: "/dashboard/employee/tasks", icon: <CheckSquare className="w-4 h-4" /> },
          { label: "Monthly Reviews", href: "/dashboard/employee/reviews", icon: <Award className="w-4 h-4" /> },
          { label: "Development Plan", href: "/dashboard/employee/growth", icon: <TrendingUp className="w-4 h-4" /> },
        ];
      case "MANAGER":
        return [
          { label: "Team Overview", href: "/dashboard/manager", icon: <Users className="w-4 h-4" /> },
          { label: "Review Workbench", href: "/dashboard/manager/reviews", icon: <ClipboardCheck className="w-4 h-4" /> },
          { label: "Goal Approvals", href: "/dashboard/manager/approvals", icon: <Target className="w-4 h-4" /> },
          { label: "Workload Heatmap", href: "/dashboard/manager/workload", icon: <Scale className="w-4 h-4" /> },
        ];
      case "HR":
        return [
          { label: "Org Analytics", href: "/dashboard/hr", icon: <LayoutDashboard className="w-4 h-4" /> },
          { label: "Employee Directory", href: "/dashboard/hr/directory", icon: <Users className="w-4 h-4" /> },
          { label: "Role KPI Templates", href: "/dashboard/hr/kpi-templates", icon: <Scale className="w-4 h-4" /> },
        ];
      case "ADMIN":
        return [
          { label: "System Health", href: "/dashboard/admin", icon: <ShieldAlert className="w-4 h-4" /> },
          { label: "Audit Logs", href: "/dashboard/admin/audit-logs", icon: <FileText className="w-4 h-4" /> },
          { label: "User Provisioning", href: "/dashboard/admin/users", icon: <Settings className="w-4 h-4" /> },
        ];
      default:
        return [
          { label: "Overview", href: "/dashboard/employee", icon: <LayoutDashboard className="w-4 h-4" /> },
        ];
    }
  };

  const navItems = getNavItems();

  return (
    <aside className="w-64 bg-slate-900/60 border-r border-slate-800/80 flex flex-col justify-between py-6 px-3">
      <div className="space-y-6">
        <div>
          <div className="px-3 text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">
            {user?.role || "User"} Navigation
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? "bg-indigo-600/90 text-white shadow-md shadow-indigo-600/20"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                  }`}
                >
                  <span className={isActive ? "text-white" : "text-slate-400"}>{item.icon}</span>
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* System Boundary Reminder Card */}
        <div className="p-3 bg-slate-850/60 rounded-xl border border-slate-800 text-[11px] text-slate-400">
          <div className="font-semibold text-indigo-400 mb-1 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
            VYORA Core Tenet
          </div>
          Deterministic scoring is decoupled from AI narrative generation. AI never decides compensation or employment status.
        </div>
      </div>

      <div className="text-[11px] text-slate-600 px-3">
        VYORA Platform v1.0.0
      </div>
    </aside>
  );
}
