"use client";

import React, { useEffect, useState } from "react";
import { useAuth } from "@/context/auth-context";
import { apiClient } from "@/lib/api-client";
import { Award, CheckCircle2, Lock, Calendar, FileText } from "lucide-react";

export default function EmployeeReviewsPage() {
  const { user } = useAuth();
  const [reviews, setReviews] = useState<any[]>([]);
  const [selectedReview, setSelectedReview] = useState<any | null>(null);

  useEffect(() => {
    async function loadReviews() {
      if (!user) return;
      try {
        const res = await apiClient.get(`/reviews?employee_id=${user.id}`);
        setReviews(res.data);
        if (res.data.length > 0) {
          setSelectedReview(res.data[0]);
        }
      } catch (err) {
        console.error("Failed to load reviews:", err);
      }
    }
    loadReviews();
  }, [user]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
          <Award className="w-5 h-5 text-indigo-400" />
          Formal Performance Reviews &amp; Metric Snapshots
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Finalized reviews create an immutable snapshot of all metric weights and evidence frozen in time.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Review Periods List */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg space-y-2">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-2 py-1">
            Review History
          </div>
          {reviews.length === 0 ? (
            <div className="text-xs text-slate-500 p-3">No reviews found.</div>
          ) : (
            reviews.map((rev) => (
              <button
                key={rev.id}
                onClick={() => setSelectedReview(rev)}
                className={`w-full text-left p-3 rounded-lg border transition-all ${
                  selectedReview?.id === rev.id
                    ? "bg-indigo-950/60 border-indigo-700/80 text-white"
                    : "bg-slate-850/60 border-slate-800 text-slate-300 hover:bg-slate-800"
                }`}
              >
                <div className="flex items-center justify-between text-xs font-semibold mb-1">
                  <span>November 2026 Cycle</span>
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded font-mono ${
                      rev.status === "FINALIZED"
                        ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                        : "bg-amber-950 text-amber-300 border border-amber-800"
                    }`}
                  >
                    {rev.status}
                  </span>
                </div>
                <div className="text-[11px] text-slate-400">
                  Score: <strong className="text-white">{rev.final_score ?? rev.calculated_score ?? "N/A"}</strong>
                </div>
              </button>
            ))
          )}
        </div>

        {/* Selected Review Detail */}
        <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          {selectedReview ? (
            <div className="space-y-6">
              <div className="flex items-center justify-between pb-4 border-b border-slate-800">
                <div>
                  <h2 className="text-base font-bold text-white flex items-center gap-2">
                    Review Summary &amp; Decision
                    {selectedReview.status === "FINALIZED" && (
                      <span className="text-xs text-emerald-400 flex items-center gap-1">
                        <Lock className="w-3.5 h-3.5" /> Immutable Lock
                      </span>
                    )}
                  </h2>
                  <div className="text-xs text-slate-400 mt-1">
                    Evaluated by: <strong className="text-slate-300">David Miller</strong>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-[11px] text-slate-400 uppercase font-semibold">Final Score</div>
                  <div className="text-3xl font-black text-indigo-400">
                    {selectedReview.final_score ?? selectedReview.calculated_score ?? "N/A"}
                  </div>
                </div>
              </div>

              {/* Manager Feedback */}
              {selectedReview.manager_summary && (
                <div className="p-4 bg-slate-850 rounded-lg border border-slate-800">
                  <div className="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-1">
                    Manager Evaluation Summary
                  </div>
                  <p className="text-xs text-slate-200 leading-relaxed">
                    {selectedReview.manager_summary}
                  </p>
                </div>
              )}

              {/* Frozen Metric Snapshots */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
                  Frozen Evidence Snapshots
                </h3>
                {selectedReview.metric_snapshots?.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs">
                      <thead>
                        <tr className="border-b border-slate-800 text-slate-400">
                          <th className="py-2">KPI Code</th>
                          <th className="py-2">Raw Value</th>
                          <th className="py-2">Normalized</th>
                          <th className="py-2">Applied Weight</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 font-mono">
                        {selectedReview.metric_snapshots.map((s: any) => (
                          <tr key={s.id}>
                            <td className="py-2 text-slate-200">{s.kpi_code}</td>
                            <td className="py-2 text-slate-300">{s.raw_value ?? "—"}</td>
                            <td className="py-2 text-indigo-300">{s.normalized_score ?? "—"}</td>
                            <td className="py-2 text-slate-300">{s.applied_weight * 100}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="text-xs text-slate-500 italic">
                    Snapshots freeze permanently upon review finalization.
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="text-center text-slate-400 py-12">Select a review from the left panel.</div>
          )}
        </div>
      </div>
    </div>
  );
}
