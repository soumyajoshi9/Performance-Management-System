"use client";

import React, { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";
import { Scale, CheckCircle2 } from "lucide-react";

export default function KPITemplatesPage() {
  const [jobRoles, setJobRoles] = useState<any[]>([]);
  const [selectedRoleId, setSelectedRoleId] = useState("");
  const [roleConfigs, setRoleConfigs] = useState<any[]>([]);

  useEffect(() => {
    async function loadRoles() {
      try {
        const res = await apiClient.get("/organizations/roles");
        setJobRoles(res.data);
        if (res.data.length > 0) {
          setSelectedRoleId(res.data[0].id);
        }
      } catch (err) {
        console.error("Failed to load job roles:", err);
      }
    }
    loadRoles();
  }, []);

  useEffect(() => {
    if (!selectedRoleId) return;
    async function loadConfigs() {
      try {
        const res = await apiClient.get(`/kpis/configs?job_role_id=${selectedRoleId}`);
        setRoleConfigs(res.data);
      } catch (err) {
        console.error("Failed to load configs:", err);
      }
    }
    loadConfigs();
  }, [selectedRoleId]);

  const totalWeight = roleConfigs.reduce((acc, c) => acc + (c.target_weight || 0), 0);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
            <Scale className="w-5 h-5 text-indigo-400" />
            Standardized Role KPI Weight Configurations
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Configured target weights must sum to exactly 1.00 (100%) to maintain deterministic mathematical validity.
          </p>
        </div>

        {/* Role Selector */}
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400">Job Role:</label>
          <select
            value={selectedRoleId}
            onChange={(e) => setSelectedRoleId(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-indigo-500"
          >
            {jobRoles.map((r) => (
              <option key={r.id} value={r.id}>
                {r.title} ({r.level})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* KPI Weight Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        <div className="p-4 bg-slate-850/60 border-b border-slate-800 flex items-center justify-between">
          <div className="text-xs font-semibold text-slate-300">Target Weight Distribution</div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">Total Sum:</span>
            <span
              className={`font-mono text-xs font-bold px-2 py-0.5 rounded ${
                Math.abs(totalWeight - 1.0) < 0.001
                  ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                  : "bg-rose-950 text-rose-300 border border-rose-800"
              }`}
            >
              {(totalWeight * 100).toFixed(0)}%
            </span>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400">
                <th className="py-3 px-4 font-semibold">KPI Code</th>
                <th className="py-3 px-4 font-semibold">Assigned Weight</th>
                <th className="py-3 px-4 font-semibold">Minimum Evidence Threshold</th>
                <th className="py-3 px-4 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {roleConfigs.map((cfg) => (
                <tr key={cfg.id} className="hover:bg-slate-850/40 transition-colors">
                  <td className="py-3 px-4 font-mono font-medium text-slate-200">
                    {cfg.kpi_code || "KPI"}
                  </td>
                  <td className="py-3 px-4 font-mono font-bold text-indigo-400">
                    {(cfg.target_weight * 100).toFixed(0)}%
                  </td>
                  <td className="py-3 px-4 text-slate-400">
                    {cfg.min_evidence_threshold} items minimum
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-emerald-400 font-medium inline-flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Enforced
                    </span>
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
