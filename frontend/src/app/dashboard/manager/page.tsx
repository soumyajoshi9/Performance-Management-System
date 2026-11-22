"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/auth-context";
import { apiClient } from "@/lib/api-client";
import { User } from "@/types";
import { Users, ClipboardCheck, Target, ArrowRight, ShieldCheck, Scale } from "lucide-react";
import { WorkloadBadge } from "@/components/workload/workload-badge";

export default function ManagerOverviewPage() {
  const { user } = useAuth();
  const [team, setTeam] = useState<User[]>([]);
  const [pendingGoalsCount, setPendingGoalsCount] = useState(0);

  useEffect(() => {
    async function loadTeam() {
      try {
        const usersRes = await apiClient.get("/users");
        // Direct reports
        const reports = usersRes.data.filter((u: User) => u.manager_id === user?.id || u.role === "EMPLOYEE");
        setTeam(reports);

        // Fetch pending goals
        const goalsRes = await apiClient.get("/goals");
        const pending = goalsRes.data.filter((g: any) => g.approval_status === "PENDING").length;
        setPendingGoalsCount(pending);
      } catch (err) {
        console.error("Failed to load team:", err);
      }
    }
    loadTeam();
  }, [user]);

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="text-xs uppercase font-semibold text-indigo-400 tracking-wider">
            Team Leadership Hub
          </div>
          <h1 className="text-2xl font-extrabold text-white mt-1">
            Manager Coaching &amp; Review Portal
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Supervise team performance with context awareness, review workbench tools, and collaborative development plans.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/dashboard/manager/approvals"
            className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-950/80 hover:bg-amber-900/90 border border-amber-800 text-amber-300 rounded-lg text-xs font-semibold transition-colors"
          >
            <Target className="w-3.5 h-3.5" />
            <span>{pendingGoalsCount} Pending Goals</span>
          </Link>
          <Link
            href="/dashboard/manager/reviews"
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition-colors shadow-lg shadow-indigo-600/20"
          >
            <ClipboardCheck className="w-3.5 h-3.5" />
            <span>Review Workbench</span>
          </Link>
        </div>
      </div>

      {/* Direct Reports List */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Users className="w-4 h-4 text-indigo-400" />
            Direct Reports ({team.length})
          </h2>
          <span className="text-xs text-slate-500">November 2026 Evaluation Period</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {team.map((emp) => (
            <div
              key={emp.id}
              className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between hover:border-indigo-600/50 transition-all"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-sm font-bold text-white">{emp.full_name}</h3>
                    <div className="text-xs text-slate-400 mt-0.5">{emp.email}</div>
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                    {emp.role}
                  </span>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                  <div className="text-[11px] text-slate-400">Workload:</div>
                  <WorkloadBadge status="NORMAL" totalTasks={8} completedTasks={6} />
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <Link
                  href={`/dashboard/manager/reviews?employee_id=${emp.id}`}
                  className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1 transition-colors"
                >
                  <span>Open Review Workbench</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
