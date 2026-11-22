"use client";

import React, { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";
import { AuditLog } from "@/types";
import { FileText, ShieldAlert } from "lucide-react";

export default function AuditLogsPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadLogs() {
      try {
        const res = await apiClient.get("/audit/logs?limit=50");
        setLogs(res.data);
      } catch (err) {
        console.error("Failed to load audit logs:", err);
      } finally {
        setIsLoading(false);
      }
    }
    loadLogs();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
          <FileText className="w-5 h-5 text-indigo-400" />
          Immutable Security &amp; Operational Audit Trail
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Every state-changing operation, review finalization, and security event is recorded in an append-only audit ledger.
        </p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-850/60 text-slate-400">
                <th className="py-3 px-4 font-semibold font-sans">Timestamp</th>
                <th className="py-3 px-4 font-semibold font-sans">Action</th>
                <th className="py-3 px-4 font-semibold font-sans">Resource Type</th>
                <th className="py-3 px-4 font-semibold font-sans">Actor ID</th>
                <th className="py-3 px-4 font-semibold font-sans">IP Address</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {logs.length === 0 ? (
                <tr>
                  <td colSpan={5} className="py-8 text-center text-slate-500 font-sans">
                    No audit records found.
                  </td>
                </tr>
              ) : (
                logs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-850/40 transition-colors">
                    <td className="py-3 px-4 text-slate-400">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">
                        {log.action}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-300">{log.resource_type}</td>
                    <td className="py-3 px-4 text-slate-500 truncate max-w-[120px]" title={log.actor_id}>
                      {log.actor_id || "SYSTEM"}
                    </td>
                    <td className="py-3 px-4 text-slate-500">{log.ip_address || "127.0.0.1"}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
