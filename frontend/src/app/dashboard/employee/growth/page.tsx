"use client";

import React, { useEffect, useState } from "react";
import { useAuth } from "@/context/auth-context";
import { apiClient } from "@/lib/api-client";
import { DevelopmentPlan } from "@/types";
import { TrendingUp, CheckCircle, Clock, ShieldCheck, ArrowRight } from "lucide-react";

export default function GrowthPlanPage() {
  const { user } = useAuth();
  const [plan, setPlan] = useState<DevelopmentPlan | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadPlan() {
      if (!user) return;
      setIsLoading(true);
      try {
        const res = await apiClient.get(`/development-plans?employee_id=${user.id}`);
        if (res.data && res.data.length > 0) {
          setPlan(res.data[0]);
        }
      } catch (err) {
        console.error("Failed to load development plan:", err);
      } finally {
        setIsLoading(false);
      }
    }
    loadPlan();
  }, [user]);

  const handleAgree = async () => {
    if (!plan) return;
    try {
      const res = await apiClient.post(`/development-plans/${plan.id}/agreement`, {
        agreed: true,
      });
      setPlan(res.data);
    } catch (err) {
      console.error("Failed to agree to plan:", err);
    }
  };

  const handleToggleItem = async (itemId: string, currentCompleted: boolean) => {
    if (!plan) return;
    try {
      const res = await apiClient.patch(`/development-plans/${plan.id}/action-items/${itemId}`, {
        is_completed: !currentCompleted,
      });
      setPlan(res.data);
    } catch (err) {
      console.error("Failed to toggle action item:", err);
    }
  };

  if (isLoading) {
    return <div className="text-xs text-slate-400 p-8">Loading development plans...</div>;
  }

  if (!plan) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-slate-400">
        <TrendingUp className="w-8 h-8 text-indigo-400 mx-auto mb-2 opacity-60" />
        <h3 className="text-sm font-bold text-white mb-1">No Active Development Plan</h3>
        <p className="text-xs">Your manager can propose a growth plan with milestones during your monthly review.</p>
      </div>
    );
  }

  const completedCount = plan.action_items?.filter((a) => a.is_completed).length || 0;
  const totalCount = plan.action_items?.length || 0;
  const progressPercent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-indigo-400" />
          Collaborative Development &amp; Growth Plan
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Development plans require bilateral agreement between manager and employee before activation.
        </p>
      </div>

      {/* Plan Overview Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-4">
          <div>
            <div className="text-[11px] font-bold text-indigo-400 uppercase tracking-wider">
              {plan.status} Plan
            </div>
            <h2 className="text-lg font-bold text-white mt-0.5">{plan.title}</h2>
            <p className="text-xs text-slate-400 mt-1">{plan.objective}</p>
          </div>

          <div className="text-right">
            <div className="text-[11px] text-slate-400 uppercase font-semibold">Milestones Completed</div>
            <div className="text-xl font-bold text-indigo-400">
              {completedCount} <span className="text-sm text-slate-400">/ {totalCount}</span>
            </div>
          </div>
        </div>

        {/* Bilateral Agreement Status Banner */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-slate-850 p-4 rounded-lg border border-slate-700/60 flex items-center justify-between">
            <div>
              <div className="text-xs font-semibold text-white">Manager Approval</div>
              <div className="text-[11px] text-slate-400">David Miller</div>
            </div>
            <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">
              <CheckCircle className="w-3.5 h-3.5" /> Agreed
            </span>
          </div>

          <div className="bg-slate-850 p-4 rounded-lg border border-slate-700/60 flex items-center justify-between">
            <div>
              <div className="text-xs font-semibold text-white">Employee Agreement</div>
              <div className="text-[11px] text-slate-400">Sarah Chen</div>
            </div>
            {plan.employee_agreed ? (
              <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">
                <CheckCircle className="w-3.5 h-3.5" /> Agreed
              </span>
            ) : (
              <button
                onClick={handleAgree}
                className="px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-md transition-colors"
              >
                Sign Agreement
              </button>
            )}
          </div>
        </div>

        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-xs font-semibold mb-1">
            <span className="text-slate-400">Overall Plan Progress</span>
            <span className="text-indigo-400">{progressPercent}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className="bg-indigo-600 h-full rounded-full transition-all duration-300"
              style={{ width: `${progressPercent}%` }}
            ></div>
          </div>
        </div>

        {/* Action Items List */}
        <div>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">
            Growth Action Items &amp; Milestones
          </h3>
          <div className="space-y-2">
            {plan.action_items?.map((item) => (
              <div
                key={item.id}
                onClick={() => handleToggleItem(item.id, item.is_completed)}
                className={`flex items-center justify-between p-3.5 rounded-lg border cursor-pointer transition-colors ${
                  item.is_completed
                    ? "bg-slate-850/40 border-slate-800 text-slate-500"
                    : "bg-slate-850 border-slate-700/80 hover:border-indigo-600/60 text-slate-200"
                }`}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-4 h-4 rounded flex items-center justify-center text-xs font-bold ${
                      item.is_completed ? "bg-emerald-600 text-white" : "border border-slate-600"
                    }`}
                  >
                    {item.is_completed ? "✓" : ""}
                  </div>
                  <div>
                    <div className={`text-xs font-medium ${item.is_completed ? "line-through" : ""}`}>
                      {item.title}
                    </div>
                    {item.description && (
                      <div className="text-[11px] text-slate-400 mt-0.5">{item.description}</div>
                    )}
                  </div>
                </div>

                {item.target_date && (
                  <span className="text-[11px] text-slate-400 font-mono">
                    Target: {new Date(item.target_date).toLocaleDateString()}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
