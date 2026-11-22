"use client";

import React, { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";
import { Goal } from "@/types";
import { Target, CheckCircle2, XCircle, Clock } from "lucide-react";

export default function GoalApprovalsPage() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadPendingGoals() {
      setIsLoading(true);
      try {
        const res = await apiClient.get("/goals");
        const pending = res.data.filter((g: Goal) => g.approval_status === "PENDING");
        setGoals(pending);
      } catch (err) {
        console.error("Failed to load goals:", err);
      } finally {
        setIsLoading(false);
      }
    }
    loadPendingGoals();
  }, []);

  const handleAction = async (goalId: string, action: "APPROVE" | "REJECT") => {
    try {
      await apiClient.post(`/goals/${goalId}/approval`, { action });
      setGoals(goals.filter((g) => g.id !== goalId));
    } catch (err) {
      console.error(`Failed to ${action} goal:`, err);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
          <Target className="w-5 h-5 text-indigo-400" />
          Employee Proposed Goal Approval Queue
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Review employee-created goals to ensure alignment with team objectives before they become active.
        </p>
      </div>

      <div className="space-y-3">
        {goals.length === 0 ? (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-slate-400">
            <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto mb-2 opacity-60" />
            <h3 className="text-sm font-bold text-white">All Clear</h3>
            <p className="text-xs mt-1">There are no pending employee goals requiring approval.</p>
          </div>
        ) : (
          goals.map((goal) => (
            <div
              key={goal.id}
              className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
            >
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                    {goal.category}
                  </span>
                  <span className="text-[10px] font-semibold text-amber-400 flex items-center gap-1 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800">
                    <Clock className="w-3 h-3" /> Awaiting Review
                  </span>
                </div>
                <h3 className="text-sm font-bold text-white">{goal.title}</h3>
                <div className="text-xs text-slate-400 mt-1">
                  Target: <strong className="text-slate-300">{goal.target_metric} ({goal.target_value})</strong> | Due:{" "}
                  <strong className="text-slate-300">{goal.due_date}</strong>
                </div>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => handleAction(goal.id, "REJECT")}
                  className="flex items-center gap-1 px-3 py-1.5 bg-rose-950 hover:bg-rose-900 border border-rose-800 text-rose-300 rounded-lg text-xs font-semibold transition-colors"
                >
                  <XCircle className="w-3.5 h-3.5" />
                  <span>Reject</span>
                </button>
                <button
                  onClick={() => handleAction(goal.id, "APPROVE")}
                  className="flex items-center gap-1 px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold transition-colors"
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Approve Goal</span>
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
