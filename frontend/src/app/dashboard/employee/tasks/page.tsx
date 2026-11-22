"use client";

import React, { useEffect, useState } from "react";
import { useAuth } from "@/context/auth-context";
import { apiClient } from "@/lib/api-client";
import { Task } from "@/types";
import { CheckSquare, AlertCircle, Clock, CheckCircle2, ShieldAlert } from "lucide-react";
import { ComplexityBadge } from "@/components/workload/workload-badge";

export default function TasksPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [blockerModalTask, setBlockerModalTask] = useState<Task | null>(null);
  const [blockerReason, setBlockerReason] = useState("");

  useEffect(() => {
    async function loadTasks() {
      if (!user) return;
      try {
        const res = await apiClient.get(`/tasks?employee_id=${user.id}`);
        setTasks(res.data);
      } catch (err) {
        console.error("Failed to load tasks:", err);
      }
    }
    loadTasks();
  }, [user]);

  const updateStatus = async (taskId: string, newStatus: Task["status"], reason?: string) => {
    try {
      const payload: any = { status: newStatus };
      if (newStatus === "BLOCKED") {
        payload.blocker_reason = reason;
      }

      const res = await apiClient.patch(`/tasks/${taskId}/status`, payload);
      setTasks(tasks.map((t) => (t.id === taskId ? res.data : t)));
      setBlockerModalTask(null);
      setBlockerReason("");
    } catch (err) {
      console.error("Failed to update task status:", err);
    }
  };

  const handleStatusChange = (task: Task, targetStatus: Task["status"]) => {
    if (targetStatus === "BLOCKED") {
      setBlockerModalTask(task);
    } else {
      updateStatus(task.id, targetStatus);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
          <CheckSquare className="w-5 h-5 text-indigo-400" />
          Task Management &amp; Contextual Blockers
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Tasks record complexity weights and active blocker logs to ensure workload context is audited during evaluations.
        </p>
      </div>

      {/* Task List Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-850/60 text-slate-400">
                <th className="py-3 px-4 font-semibold">Task Title</th>
                <th className="py-3 px-4 font-semibold">Priority</th>
                <th className="py-3 px-4 font-semibold">Complexity</th>
                <th className="py-3 px-4 font-semibold">Due Date</th>
                <th className="py-3 px-4 font-semibold">Status</th>
                <th className="py-3 px-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {tasks.map((task) => (
                <tr key={task.id} className="hover:bg-slate-850/40 transition-colors">
                  <td className="py-3.5 px-4 font-medium text-slate-200">
                    <div>{task.title}</div>
                    {task.blocker_reason && (
                      <div className="text-[11px] text-rose-400 mt-1 flex items-center gap-1 bg-rose-950/40 p-1.5 rounded border border-rose-900/50">
                        <ShieldAlert className="w-3 h-3 shrink-0" />
                        <span>Blocker: {task.blocker_reason}</span>
                      </div>
                    )}
                  </td>
                  <td className="py-3.5 px-4">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                        task.priority === "URGENT" || task.priority === "HIGH"
                          ? "bg-rose-950/80 text-rose-300 border-rose-800"
                          : "bg-slate-800 text-slate-400 border-slate-700"
                      }`}
                    >
                      {task.priority}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    <ComplexityBadge complexity={task.complexity} />
                  </td>
                  <td className="py-3.5 px-4 text-slate-400 font-mono">
                    {task.due_date ? new Date(task.due_date).toLocaleDateString() : "—"}
                  </td>
                  <td className="py-3.5 px-4">
                    <span
                      className={`inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded ${
                        task.status === "COMPLETED"
                          ? "text-emerald-400 bg-emerald-950/60 border border-emerald-900"
                          : task.status === "BLOCKED"
                          ? "text-rose-400 bg-rose-950/60 border border-rose-900"
                          : task.status === "IN_PROGRESS"
                          ? "text-indigo-400 bg-indigo-950/60 border border-indigo-900"
                          : "text-slate-400 bg-slate-800 border border-slate-700"
                      }`}
                    >
                      {task.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <div className="flex items-center justify-end gap-1.5">
                      {task.status !== "COMPLETED" && (
                        <button
                          onClick={() => handleStatusChange(task, "COMPLETED")}
                          className="px-2 py-1 bg-emerald-950 hover:bg-emerald-900 border border-emerald-800 text-emerald-300 rounded text-[11px] font-medium transition-colors"
                        >
                          Complete
                        </button>
                      )}
                      {task.status !== "BLOCKED" && task.status !== "COMPLETED" && (
                        <button
                          onClick={() => handleStatusChange(task, "BLOCKED")}
                          className="px-2 py-1 bg-rose-950 hover:bg-rose-900 border border-rose-800 text-rose-300 rounded text-[11px] font-medium transition-colors"
                        >
                          Report Blocker
                        </button>
                      )}
                      {task.status !== "IN_PROGRESS" && task.status !== "COMPLETED" && (
                        <button
                          onClick={() => handleStatusChange(task, "IN_PROGRESS")}
                          className="px-2 py-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 rounded text-[11px] font-medium transition-colors"
                        >
                          Start
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Blocker Modal */}
      {blockerModalTask && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 max-w-md w-full shadow-2xl">
            <h3 className="text-sm font-bold text-white mb-2 flex items-center gap-2 text-rose-400">
              <ShieldAlert className="w-4 h-4" />
              Report Task Blocker
            </h3>
            <p className="text-xs text-slate-400 mb-4">
              Blocker reasons are mandatory so delays due to third-party dependencies are not penalized in your performance scoring.
            </p>
            <textarea
              value={blockerReason}
              onChange={(e) => setBlockerReason(e.target.value)}
              placeholder="e.g., Awaiting security audit approval from InfoSec team on KMS key rotation."
              required
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-xs text-white focus:outline-none focus:border-indigo-500 min-h-[90px]"
            />
            <div className="flex justify-end gap-2 mt-4">
              <button
                onClick={() => setBlockerModalTask(null)}
                className="px-3 py-1.5 text-xs text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={() => updateStatus(blockerModalTask.id, "BLOCKED", blockerReason)}
                disabled={!blockerReason.trim()}
                className="px-4 py-1.5 text-xs bg-rose-600 hover:bg-rose-700 disabled:opacity-50 text-white font-medium rounded-md transition-colors"
              >
                Log Blocker
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
