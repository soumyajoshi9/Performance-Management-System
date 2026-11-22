"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { useAuth } from "@/context/auth-context";
import { apiClient } from "@/lib/api-client";
import { User, ScorePreview, AIInsight } from "@/types";
import { ScoreBreakdownCard } from "@/components/scoring/score-breakdown-card";
import { AINarrativeCard } from "@/components/ai/ai-narrative-card";
import { 
  ClipboardCheck, Sparkles, Lock, CheckCircle2, AlertTriangle, FileText, Send 
} from "lucide-react";

function ReviewWorkbenchContent() {
  const searchParams = useSearchParams();
  const { user } = useAuth();

  const [employees, setEmployees] = useState<User[]>([]);
  const [selectedEmpId, setSelectedEmpId] = useState<string>("");
  const [activePeriod, setActivePeriod] = useState<any | null>(null);

  const [scoreData, setScoreData] = useState<ScorePreview | null>(null);
  const [aiInsight, setAiInsight] = useState<AIInsight | null>(null);
  const [reviewDraft, setReviewDraft] = useState<any | null>(null);
  const [managerSummary, setManagerSummary] = useState("");
  const [isFinalizing, setIsFinalizing] = useState(false);
  const [isGeneratingAi, setIsGeneratingAi] = useState(false);
  const [feedbackList, setFeedbackList] = useState<any[]>([]);

  useEffect(() => {
    async function init() {
      try {
        const [usersRes, periodRes] = await Promise.all([
          apiClient.get("/users"),
          apiClient.get("/review-periods/active"),
        ]);
        const emps = usersRes.data.filter((u: User) => u.role === "EMPLOYEE");
        setEmployees(emps);
        setActivePeriod(periodRes.data);

        const paramEmpId = searchParams.get("employee_id");
        if (paramEmpId) {
          setSelectedEmpId(paramEmpId);
        } else if (emps.length > 0) {
          setSelectedEmpId(emps[0].id);
        }
      } catch (err) {
        console.error("Failed to load initial data:", err);
      }
    }
    init();
  }, [searchParams]);

  useEffect(() => {
    if (!selectedEmpId || !activePeriod) return;

    async function loadEmployeeReviewData() {
      try {
        // 1. Score preview
        const scoreRes = await apiClient.post("/scoring/preview", {
          employee_id: selectedEmpId,
          review_period_id: activePeriod.id,
        });
        setScoreData(scoreRes.data);

        // 2. Draft review
        const draftRes = await apiClient.post("/reviews/draft", {
          employee_id: selectedEmpId,
          review_period_id: activePeriod.id,
        });
        setReviewDraft(draftRes.data);
        if (draftRes.data.manager_summary) {
          setManagerSummary(draftRes.data.manager_summary);
        }

        // 3. Feedback list
        const fbRes = await apiClient.get(`/feedbacks?employee_id=${selectedEmpId}&review_period_id=${activePeriod.id}`);
        setFeedbackList(fbRes.data);

        // 4. Try loading existing AI insight
        const aiRes = await apiClient.get(`/ai/insights?employee_id=${selectedEmpId}&review_period_id=${activePeriod.id}`).catch(() => ({ data: [] }));
        if (aiRes.data && aiRes.data.length > 0) {
          setAiInsight(aiRes.data[0]);
        } else {
          setAiInsight(null);
        }
      } catch (err) {
        console.error("Failed to load employee review details:", err);
      }
    }

    loadEmployeeReviewData();
  }, [selectedEmpId, activePeriod]);

  const handleGenerateAi = async () => {
    if (!selectedEmpId || !activePeriod) return;
    setIsGeneratingAi(true);
    try {
      const res = await apiClient.post("/ai/insights/generate", {
        employee_id: selectedEmpId,
        review_period_id: activePeriod.id,
      });
      setAiInsight(res.data);
    } catch (err) {
      console.error("Failed to generate AI insight:", err);
    } finally {
      setIsGeneratingAi(false);
    }
  };

  const handleFinalizeReview = async () => {
    if (!reviewDraft || !managerSummary.trim()) return;
    setIsFinalizing(true);
    try {
      const res = await apiClient.post(`/reviews/${reviewDraft.id}/finalize`, {
        manager_summary: managerSummary,
      });
      setReviewDraft(res.data);
    } catch (err) {
      console.error("Failed to finalize review:", err);
    } finally {
      setIsFinalizing(false);
    }
  };

  const isFinalized = reviewDraft?.status === "FINALIZED";

  return (
    <div className="space-y-6">
      {/* Workbench Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-4">
        <div>
          <div className="text-xs uppercase font-semibold text-indigo-400 tracking-wider">
            Formal Evaluation Portal
          </div>
          <h1 className="text-xl font-extrabold text-white mt-0.5 flex items-center gap-2">
            <ClipboardCheck className="w-5 h-5 text-indigo-400" />
            Performance Review Workbench
          </h1>
        </div>

        {/* Employee Selector */}
        <div className="flex items-center gap-3">
          <label className="text-xs text-slate-400">Employee:</label>
          <select
            value={selectedEmpId}
            onChange={(e) => setSelectedEmpId(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-indigo-500"
          >
            {employees.map((emp) => (
              <option key={emp.id} value={emp.id}>
                {emp.full_name} ({emp.role})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Status Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
        <div className="flex items-center gap-3 text-xs">
          <span className="text-slate-400">Review Status:</span>
          <span
            className={`px-2.5 py-1 rounded-full font-semibold font-mono text-[11px] flex items-center gap-1 ${
              isFinalized
                ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                : "bg-amber-950 text-amber-300 border border-amber-800"
            }`}
          >
            {isFinalized ? <Lock className="w-3 h-3" /> : null}
            {reviewDraft?.status || "DRAFT"}
          </span>
          <span className="text-slate-600">|</span>
          <span className="text-slate-400">
            Calculated Score:{" "}
            <strong className="text-indigo-400">
              {scoreData?.calculated_score?.toFixed(1) || "N/A"}
            </strong>
          </span>
        </div>

        {/* Generate AI Button */}
        {!aiInsight && !isFinalized && (
          <button
            onClick={handleGenerateAi}
            disabled={isGeneratingAi}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-lg text-xs font-semibold transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>{isGeneratingAi ? "Synthesizing Evidence..." : "Generate AI Explanation"}</span>
          </button>
        )}
      </div>

      {/* Step 1: Deterministic Metrics */}
      <div>
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
          1. Deterministic Metrics &amp; Evidence Coverage
        </h3>
        <ScoreBreakdownCard scoreData={scoreData} />
      </div>

      {/* Step 2: Qualitative Feedback & Self Assessment */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
          2. Qualitative Context &amp; Employee Self-Assessment
        </h3>
        {feedbackList.length === 0 ? (
          <div className="text-xs text-slate-500 italic">No feedback entries recorded for this period yet.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {feedbackList.map((fb) => (
              <div key={fb.id} className="p-4 bg-slate-850 rounded-lg border border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-xs font-semibold">
                  <span className="text-indigo-400 uppercase tracking-wider text-[10px]">
                    {fb.feedback_type === "SELF_ASSESSMENT" ? "Employee Self-Assessment" : "Manager Feedback"}
                  </span>
                  <span className="text-slate-500 text-[10px]">
                    {new Date(fb.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-xs text-slate-200 leading-relaxed">{fb.content}</p>
                {fb.strengths && (
                  <div className="text-[11px] text-emerald-400">
                    <strong>Strengths:</strong> {fb.strengths}
                  </div>
                )}
                {fb.growth_areas && (
                  <div className="text-[11px] text-amber-400">
                    <strong>Growth Areas:</strong> {fb.growth_areas}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Step 3: AI Narrative Card */}
      {aiInsight && (
        <div>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
            3. AI-Assisted Evidence Synthesis &amp; Growth Recommendations
          </h3>
          <AINarrativeCard insight={aiInsight} />
        </div>
      )}

      {/* Step 4: Final Evaluation Decision & Immutability Lock */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <FileText className="w-4 h-4 text-indigo-400" />
          4. Formal Evaluation Decision &amp; Finalization
        </h3>

        {isFinalized ? (
          <div className="p-4 bg-emerald-950/60 border border-emerald-800 rounded-lg text-xs text-emerald-300 flex items-center gap-2">
            <Lock className="w-4 h-4 text-emerald-400 shrink-0" />
            <div>
              <strong>This review was finalized and locked on {new Date(reviewDraft.finalized_at).toLocaleDateString()}.</strong>
              <div className="mt-1 text-slate-300">"{reviewDraft.manager_summary}"</div>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            <p className="text-xs text-slate-400">
              Provide formal performance evaluation remarks. Finalizing will permanently compute the final score, notify the employee, and freeze immutable metric snapshots in the database.
            </p>
            <textarea
              value={managerSummary}
              onChange={(e) => setManagerSummary(e.target.value)}
              placeholder="Detail overall technical performance, delivery consistency, and strategic coaching notes..."
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 min-h-[100px]"
            />
            <div className="flex justify-end">
              <button
                onClick={handleFinalizeReview}
                disabled={isFinalizing || !managerSummary.trim()}
                className="flex items-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-semibold text-xs rounded-lg transition-colors shadow-lg shadow-emerald-600/20"
              >
                <Lock className="w-3.5 h-3.5" />
                <span>{isFinalizing ? "Locking Snapshots..." : "Finalize & Lock Review"}</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ReviewWorkbenchPage() {
  return (
    <Suspense fallback={<div className="p-8 text-xs text-slate-400">Loading Review Workbench...</div>}>
      <ReviewWorkbenchContent />
    </Suspense>
  );
}
