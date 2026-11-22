"use client";

import React, { useState } from "react";
import { AIInsight } from "@/types";
import { Sparkles, Flag, CheckCircle, AlertCircle, Quote } from "lucide-react";
import { apiClient } from "@/lib/api-client";

interface AINarrativeCardProps {
  insight?: AIInsight | null;
  onFlagSuccess?: () => void;
}

export function AINarrativeCard({ insight, onFlagSuccess }: AINarrativeCardProps) {
  const [flagReason, setFlagReason] = useState("");
  const [isFlagging, setIsFlagging] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [flagSuccess, setFlagSuccess] = useState(false);

  if (!insight) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center text-slate-400">
        <Sparkles className="w-8 h-8 text-indigo-400 mx-auto mb-2 opacity-60" />
        <p>AI explanation will be generated upon review draft creation.</p>
      </div>
    );
  }

  const { structured_output } = insight;

  const handleFlag = async () => {
    if (!flagReason.trim()) return;
    setIsFlagging(true);
    try {
      await apiClient.post(`/ai/insights/${insight.id}/flag`, { reason: flagReason });
      setFlagSuccess(true);
      setShowModal(false);
      if (onFlagSuccess) onFlagSuccess();
    } catch (err) {
      console.error("Flagging failed:", err);
    } finally {
      setIsFlagging(false);
    }
  };

  return (
    <div className="bg-gradient-to-b from-slate-900 to-slate-950 border border-indigo-900/40 rounded-xl p-6 shadow-xl relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl -z-10"></div>

      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800/80">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-indigo-950 flex items-center justify-center border border-indigo-800/80 text-indigo-400">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              Explainable Performance Intelligence
              <span className="text-[10px] bg-indigo-900/60 text-indigo-300 px-2 py-0.5 rounded font-mono border border-indigo-700/50">
                {insight.model_version}
              </span>
            </h3>
            <p className="text-[11px] text-slate-400">Grounded strictly in verified metrics</p>
          </div>
        </div>

        {/* Flag Insight Button */}
        {insight.status !== "FLAGGED" && !flagSuccess ? (
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-rose-400 bg-slate-800/60 hover:bg-slate-800 px-3 py-1.5 rounded-md border border-slate-700/60 transition-colors"
          >
            <Flag className="w-3.5 h-3.5" />
            <span>Flag Discrepancy</span>
          </button>
        ) : (
          <span className="text-xs text-rose-400 flex items-center gap-1 bg-rose-950/60 px-2.5 py-1 rounded border border-rose-900">
            <AlertCircle className="w-3.5 h-3.5" /> Flagged for Manager Review
          </span>
        )}
      </div>

      {/* Narrative Body */}
      <div className="mt-4 space-y-4">
        {/* Executive Summary */}
        <div className="p-3.5 bg-slate-850/60 rounded-lg border border-slate-800 text-sm text-slate-200 leading-relaxed">
          {structured_output.summary}
        </div>

        {/* Strengths & Growth Areas Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-4">
            <div className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2 flex items-center gap-1.5">
              <CheckCircle className="w-3.5 h-3.5" /> Demonstrated Strengths
            </div>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {structured_output.strengths.map((s, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-emerald-500 font-bold">•</span>
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-4">
            <div className="text-xs font-bold uppercase tracking-wider text-amber-400 mb-2 flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5" /> Focus Areas for Growth
            </div>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {structured_output.growth_areas.map((g, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-amber-500 font-bold">•</span>
                  <span>{g}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Evidence References */}
        {structured_output.evidence_references?.length > 0 && (
          <div className="pt-2">
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
              <Quote className="w-3 h-3 text-indigo-400" />
              Audited Evidence Citations
            </div>
            <div className="flex flex-wrap gap-2">
              {structured_output.evidence_references.map((ref, idx) => (
                <span
                  key={idx}
                  className="text-[11px] font-mono bg-slate-800/90 text-indigo-300 px-2.5 py-1 rounded border border-indigo-900/60"
                >
                  {ref}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Disclaimer */}
        <div className="text-[10px] text-slate-500 italic border-t border-slate-800/60 pt-3">
          {structured_output.disclaimer || "AI-generated recommendations provide contextual support and are subject to human review."}
        </div>
      </div>

      {/* Flag Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 max-w-md w-full shadow-2xl">
            <h3 className="text-sm font-bold text-white mb-2">Flag Inaccurate AI Insight</h3>
            <p className="text-xs text-slate-400 mb-4">
              Describe why you believe this AI summary contradicts your objective work evidence. Your manager will be alerted.
            </p>
            <textarea
              value={flagReason}
              onChange={(e) => setFlagReason(e.target.value)}
              placeholder="e.g., Summary states low velocity, but P99 latency reduction goal was delivered ahead of schedule."
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-xs text-white focus:outline-none focus:border-indigo-500 min-h-[90px]"
            />
            <div className="flex justify-end gap-2 mt-4">
              <button
                onClick={() => setShowModal(false)}
                className="px-3 py-1.5 text-xs text-slate-400 hover:text-white transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleFlag}
                disabled={isFlagging || !flagReason.trim()}
                className="px-4 py-1.5 text-xs bg-rose-600 hover:bg-rose-700 disabled:opacity-50 text-white font-medium rounded-md transition-colors"
              >
                {isFlagging ? "Submitting..." : "Submit Flag"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
