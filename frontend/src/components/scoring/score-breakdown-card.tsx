import React from "react";
import { ScorePreview } from "@/types";
import { ShieldCheck, AlertTriangle, CheckCircle2, Info } from "lucide-react";
import { formatPercent, formatScore } from "@/lib/utils";

interface ScoreBreakdownCardProps {
  scoreData?: ScorePreview | null;
  isLoading?: boolean;
}

export function ScoreBreakdownCard({ scoreData, isLoading }: ScoreBreakdownCardProps) {
  if (isLoading) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 animate-pulse space-y-4">
        <div className="h-6 bg-slate-800 rounded w-1/3"></div>
        <div className="h-20 bg-slate-850 rounded"></div>
        <div className="space-y-2">
          <div className="h-10 bg-slate-800 rounded"></div>
          <div className="h-10 bg-slate-800 rounded"></div>
        </div>
      </div>
    );
  }

  if (!scoreData) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-slate-400">
        <Info className="w-8 h-8 text-slate-500 mx-auto mb-2" />
        <p>No performance score computed for this period yet.</p>
      </div>
    );
  }

  const isInsufficient = scoreData.score_status === "INSUFFICIENT_DATA";

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-6 border-b border-slate-800 gap-4">
        <div>
          <div className="text-xs uppercase font-semibold text-slate-400 tracking-wider">
            Deterministic Evaluation Score
          </div>
          <div className="flex items-baseline gap-3 mt-1">
            <span className="text-4xl font-extrabold text-white">
              {isInsufficient ? "N/A" : formatScore(scoreData.calculated_score)}
            </span>
            <span className="text-sm text-slate-400">/ 100.0 Max</span>
            
            <span
              className={`px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 ${
                isInsufficient
                  ? "bg-amber-950/80 text-amber-300 border border-amber-800"
                  : "bg-emerald-950/80 text-emerald-300 border border-emerald-800"
              }`}
            >
              {isInsufficient ? (
                <>
                  <AlertTriangle className="w-3.5 h-3.5" />
                  Insufficient Data (&lt;50% Coverage)
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Audited &amp; Validated
                </>
              )}
            </span>
          </div>
        </div>

        {/* Coverage Meter */}
        <div className="bg-slate-850 border border-slate-700/60 rounded-lg p-3 text-right sm:min-w-[180px]">
          <div className="text-[11px] text-slate-400 uppercase font-semibold">Data Coverage</div>
          <div className="text-lg font-bold text-indigo-400">
            {formatPercent(scoreData.data_coverage_percentage)}
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-1.5 overflow-hidden">
            <div
              className={`h-full rounded-full ${
                scoreData.data_coverage_percentage >= 50 ? "bg-indigo-500" : "bg-amber-500"
              }`}
              style={{ width: `${Math.min(100, scoreData.data_coverage_percentage)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Metrics Breakdown Table */}
      <div className="mt-6">
        <h4 className="text-xs font-bold uppercase text-slate-400 tracking-wider mb-3">
          KPI Metric Weight Redistribution &amp; Audit Breakdown
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 pb-2">
                <th className="py-2.5 font-semibold">Metric Name</th>
                <th className="py-2.5 font-semibold">Raw Result</th>
                <th className="py-2.5 font-semibold">Normalized (0-100)</th>
                <th className="py-2.5 font-semibold">Target Weight</th>
                <th className="py-2.5 font-semibold">Applied Weight</th>
                <th className="py-2.5 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {scoreData.metrics.map((m) => (
                <tr key={m.kpi_code} className="hover:bg-slate-850/50 transition-colors">
                  <td className="py-3 font-medium text-slate-200">
                    <div>{m.kpi_name}</div>
                    <span className="text-[10px] text-slate-500 font-mono">{m.kpi_code}</span>
                  </td>
                  <td className="py-3 text-slate-300">
                    {m.raw_value !== null ? `${m.raw_value} ${m.unit}` : "No Activity"}
                  </td>
                  <td className="py-3 font-mono font-medium text-indigo-300">
                    {m.normalized_score !== null ? m.normalized_score.toFixed(1) : "—"}
                  </td>
                  <td className="py-3 text-slate-400">
                    {formatPercent(m.assigned_weight * 100)}
                  </td>
                  <td className="py-3 font-semibold text-slate-200">
                    {formatPercent(m.applied_weight * 100)}
                  </td>
                  <td className="py-3">
                    {m.data_sufficient ? (
                      <span className="text-emerald-400 font-medium inline-flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5" /> Sufficient
                      </span>
                    ) : (
                      <span className="text-amber-400 font-medium inline-flex items-center gap-1" title={m.insufficient_reason || "Threshold not met"}>
                        <AlertTriangle className="w-3.5 h-3.5" /> Excluded
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
