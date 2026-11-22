"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/auth-context";
import { apiClient } from "@/lib/api-client";
import { Goal, Task, ScorePreview, DevelopmentPlan } from "@/types";
import { ScoreBreakdownCard } from "@/components/scoring/score-breakdown-card";
import { WorkloadBadge } from "@/components/workload/workload-badge";
import { 
  Target, CheckSquare, TrendingUp, ArrowRight, Sparkles, Send, CheckCircle2 
} from "lucide-react";

export default function EmployeeDashboardPage() {
  const { user } = useAuth();
  const [goals, setGoals] = useState<Goal[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [scoreData, setScoreData] = useState<ScorePreview | null>(null);
  const [plan, setPlan] = useState<DevelopmentPlan | null>(null);
  const [activePeriodId, setActivePeriodId] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  // Self assessment state
  const [selfContent, setSelfContent] = useState("");
  const [selfSubmitted, setSelfSubmitted] = useState(false);

  useEffect(() => {
    async function loadDashboardData() {
      if (!user) return;
      setIsLoading(true);
      try {
        // Fetch active period
        const periodRes = await apiClient.get("/review-periods/active");
        const period = periodRes.data;
        setActivePeriodId(period.id);

        // Fetch Goals & Tasks in parallel
        const [goalsRes, tasksRes, planRes] = await Promise.all([
          apiClient.get(`/goals?employee_id=${user.id}`),
          apiClient.get(`/tasks?employee_id=${user.id}`),
          apiClient.get(`/development-plans?employee_id=${user.id}`).catch(() => ({ data: [] })),
        ]);

        setGoals(goalsRes.data);
        setTasks(tasksRes.data);
        if (planRes.data && planRes.data.length > 0) {
          setPlan(planRes.data[0]);
        }

        // Preview Score
        const scoreRes = await apiClient.post("/scoring/preview", {
          employee_id: user.id,
          review_period_id: period.id,
        });
        setScoreData(scoreRes.data);
      } catch (err) {
        console.error("Failed to load dashboard data:", err);
      } finally {
        setIsLoading(false);
      }
    }

    loadDashboardData();
  }, [user]);

  const handleSelfAssessment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selfContent.trim() || !user || !activePeriodId) return;
    try {
      await apiClient.post("/feedbacks", {
        employee_id: user.id,
        review_period_id: activePeriodId,
        feedback_type: "SELF_ASSESSMENT",
        content: selfContent,
      });
      setSelfSubmitted(true);
    } catch (err) {
      console.error("Failed to submit self-assessment:", err);
    }
  };

  const completedTasks = tasks.filter((t) => t.status === "COMPLETED").length;
  const activeGoals = goals.filter((g) => g.status === "ACTIVE").length;
  const avgGoalProgress = goals.length > 0 
    ? Math.round(goals.reduce((acc, g) => acc + (g.progress_percentage || 0), 0) / goals.length) 
    : 0;

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="text-xs uppercase font-semibold text-indigo-400 tracking-wider">
            Employee Intelligence Hub
          </div>
          <h1 className="text-2xl font-extrabold text-white mt-1">
            Welcome back, {user?.full_name || "Sarah Chen"}
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Role: <strong className="text-slate-200">Senior Software Engineer</strong> | Dept:{" "}
            <strong className="text-slate-200">Engineering</strong> | Manager:{" "}
            <strong className="text-slate-200">David Miller</strong>
          </p>
        </div>

        {/* Workload Badge */}
        <div>
          <WorkloadBadge
            status={scoreData?.workload_context?.workload_status || "NORMAL"}
            totalTasks={tasks.length}
            completedTasks={completedTasks}
          />
        </div>
      </div>

      {/* Core KPI Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Active Goals</span>
            <Target className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">{activeGoals} Goals</div>
          <div className="text-xs text-indigo-400 mt-1 font-medium">
            Average Progress: {avgGoalProgress}%
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Monthly Tasks</span>
            <CheckSquare className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">
            {completedTasks} <span className="text-sm font-normal text-slate-400">/ {tasks.length}</span>
          </div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">
            {tasks.length > 0 ? Math.round((completedTasks / tasks.length) * 100) : 0}% Completion Rate
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Growth Plan</span>
            <TrendingUp className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-sm font-bold text-white truncate">
            {plan ? plan.title : "No Active Plan"}
          </div>
          <div className="text-xs text-purple-400 mt-1">
            {plan?.action_items ? `${plan.action_items.filter(a => a.is_completed).length} of ${plan.action_items.length} milestones complete` : "Collaborate with manager"}
          </div>
        </div>
      </div>

      {/* Score Breakdown Section */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300">
            Current Review Period Performance
          </h2>
          <span className="text-xs text-slate-400">Deterministic Engine &amp; Coverage Audited</span>
        </div>
        <ScoreBreakdownCard scoreData={scoreData} isLoading={isLoading} />
      </div>

      {/* Active Growth Plan Summary & Self Assessment Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Development Plan Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-indigo-400" />
                Collaborative Growth Plan
              </h3>
              {plan && (
                <span className="text-[10px] bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded border border-indigo-800 uppercase font-semibold">
                  {plan.status}
                </span>
              )}
            </div>

            {plan ? (
              <div className="space-y-3">
                <div className="font-semibold text-xs text-white">{plan.title}</div>
                <p className="text-xs text-slate-400">{plan.objective}</p>
                
                <div className="space-y-2 mt-4">
                  {plan.action_items?.slice(0, 3).map((item) => (
                    <div key={item.id} className="flex items-center gap-2 text-xs bg-slate-850 p-2.5 rounded-lg border border-slate-800">
                      <span className={`w-3.5 h-3.5 rounded flex items-center justify-center text-[10px] ${item.is_completed ? "bg-emerald-600 text-white" : "border border-slate-600"}`}>
                        {item.is_completed ? "✓" : ""}
                      </span>
                      <span className={item.is_completed ? "line-through text-slate-500" : "text-slate-200"}>
                        {item.title}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-400">No active growth plan for this period.</p>
            )}
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800">
            <Link
              href="/dashboard/employee/growth"
              className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1.5 transition-colors"
            >
              <span>View full growth plan and milestones</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {/* Qualitative Self-Assessment Submission */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <h3 className="text-sm font-bold text-white mb-2 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            Monthly Self-Assessment
          </h3>
          <p className="text-xs text-slate-400 mb-4">
            Summarize your achievements, context behind difficulties, and key growth accomplishments for this period.
          </p>

          {selfSubmitted ? (
            <div className="p-4 bg-emerald-950/60 border border-emerald-800 rounded-lg text-xs text-emerald-300 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Self-assessment submitted successfully! Your manager will review this during finalization.</span>
            </div>
          ) : (
            <form onSubmit={handleSelfAssessment} className="space-y-3">
              <textarea
                value={selfContent}
                onChange={(e) => setSelfContent(e.target.value)}
                placeholder="Detail high-impact deliverables, unpredicted technical blockers, or cross-team mentorship delivered..."
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 min-h-[110px]"
              />
              <button
                type="submit"
                disabled={!selfContent.trim()}
                className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-xs font-semibold text-white rounded-lg transition-colors"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Submit to Review Packet</span>
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
