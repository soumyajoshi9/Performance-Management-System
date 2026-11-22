"use client";

import React, { useEffect, useState } from "react";
import { useAuth } from "@/context/auth-context";
import { apiClient } from "@/lib/api-client";
import { Goal } from "@/types";
import { Target, Plus, CheckCircle2, Clock, XCircle, ArrowUpRight } from "lucide-react";

export default function GoalsTrackerPage() {
  const { user } = useAuth();
  const [goals, setGoals] = useState<Goal[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [activePeriodId, setActivePeriodId] = useState("");

  // Form state
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState<"PROJECT" | "DEVELOPMENT" | "OPERATIONAL">("PROJECT");
  const [targetMetric, setTargetMetric] = useState("");
  const [targetValue, setTargetValue] = useState(100);
  const [dueDate, setDueDate] = useState("2026-11-30");

  useEffect(() => {
    async function loadGoals() {
      if (!user) return;
      try {
        const periodRes = await apiClient.get("/review-periods/active");
        setActivePeriodId(periodRes.data.id);

        const goalsRes = await apiClient.get(`/goals?employee_id=${user.id}`);
        setGoals(goalsRes.data);
      } catch (err) {
        console.error("Failed to load goals:", err);
      }
    }
    loadGoals();
  }, [user]);

  const handleCreateGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !user || !activePeriodId) return;

    try {
      const res = await apiClient.post("/goals", {
        title,
        category,
        target_metric: targetMetric || "Percentage",
        start_value: 0,
        target_value: targetValue,
        due_date: dueDate,
        review_period_id: activePeriodId,
      });

      setGoals([res.data, ...goals]);
      setShowModal(false);
      setTitle("");
      setTargetMetric("");
    } catch (err) {
      console.error("Failed to create goal:", err);
    }
  };

  const handleUpdateProgress = async (goalId: string, currentVal: number) => {
    try {
      const res = await apiClient.patch(`/goals/${goalId}/progress`, {
        current_value: currentVal,
      });
      setGoals(goals.map((g) => (g.id === goalId ? res.data : g)));
    } catch (err) {
      console.error("Failed to update progress:", err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-indigo-400" />
            Performance &amp; Development Goals
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Track measurable outcomes, update progress, and submit proposed goals for manager approval.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-1.5 px-3.5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition-colors shadow-lg shadow-indigo-600/20"
        >
          <Plus className="w-4 h-4" />
          <span>Propose Goal</span>
        </button>
      </div>

      {/* Goals Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {goals.map((goal) => {
          const isPending = goal.approval_status === "PENDING";
          const isApproved = goal.approval_status === "APPROVED";

          return (
            <div
              key={goal.id}
              className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                    {goal.category}
                  </span>

                  {isPending && (
                    <span className="text-[11px] font-semibold text-amber-400 flex items-center gap-1 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800">
                      <Clock className="w-3 h-3" /> Pending Manager Approval
                    </span>
                  )}
                  {isApproved && (
                    <span className="text-[11px] font-semibold text-emerald-400 flex items-center gap-1 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">
                      <CheckCircle2 className="w-3 h-3" /> Active &amp; Approved
                    </span>
                  )}
                  {goal.approval_status === "REJECTED" && (
                    <span className="text-[11px] font-semibold text-rose-400 flex items-center gap-1 bg-rose-950/60 px-2 py-0.5 rounded border border-rose-800">
                      <XCircle className="w-3 h-3" /> Rejected
                    </span>
                  )}
                </div>

                <h3 className="text-sm font-bold text-white mt-1">{goal.title}</h3>
                <div className="text-xs text-slate-400 mt-1">
                  Metric: <strong className="text-slate-300">{goal.target_metric}</strong> | Due:{" "}
                  <strong className="text-slate-300">{goal.due_date}</strong>
                </div>

                {/* Progress bar */}
                <div className="mt-4">
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span className="text-slate-400">Progress</span>
                    <span className="text-indigo-400">{Math.round(goal.progress_percentage || 0)}%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-indigo-600 h-full rounded-full transition-all duration-300"
                      style={{ width: `${Math.min(100, goal.progress_percentage || 0)}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              {/* Progress Slider (Only if approved) */}
              {isApproved && (
                <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                  <span className="text-slate-500">Update value:</span>
                  <div className="flex items-center gap-2">
                    <input
                      type="range"
                      min="0"
                      max={goal.target_value}
                      value={goal.current_value || 0}
                      onChange={(e) => handleUpdateProgress(goal.id, Number(e.target.value))}
                      className="w-24 accent-indigo-600 cursor-pointer"
                    />
                    <span className="text-slate-300 font-mono text-xs w-10 text-right">
                      {goal.current_value}/{goal.target_value}
                    </span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Propose Goal Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 max-w-md w-full shadow-2xl">
            <h3 className="text-sm font-bold text-white mb-3">Propose New Goal</h3>
            <form onSubmit={handleCreateGoal} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Goal Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Implement zero-downtime database migration strategy"
                  required
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Category</label>
                  <select
                    value={category}
                    onChange={(e: any) => setCategory(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
                  >
                    <option value="PROJECT">PROJECT</option>
                    <option value="DEVELOPMENT">DEVELOPMENT</option>
                    <option value="OPERATIONAL">OPERATIONAL</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Target Value</label>
                  <input
                    type="number"
                    value={targetValue}
                    onChange={(e) => setTargetValue(Number(e.target.value))}
                    required
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Target Metric</label>
                <input
                  type="text"
                  value={targetMetric}
                  onChange={(e) => setTargetMetric(e.target.value)}
                  placeholder="e.g. Latency P99 or Percent Complete"
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-3 py-1.5 text-xs text-slate-400 hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 text-xs bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-colors"
                >
                  Submit for Approval
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
