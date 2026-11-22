"use client";

import React, { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";
import { User } from "@/types";
import { Users, Upload, AlertCircle, CheckCircle2, FileText } from "lucide-react";

export default function EmployeeDirectoryPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [showImportModal, setShowImportModal] = useState(false);
  const [csvContent, setCsvContent] = useState("");
  const [importResult, setImportResult] = useState<any | null>(null);
  const [isImporting, setIsImporting] = useState(false);

  useEffect(() => {
    async function loadUsers() {
      try {
        const res = await apiClient.get("/users");
        setUsers(res.data);
      } catch (err) {
        console.error("Failed to load users:", err);
      }
    }
    loadUsers();
  }, []);

  const handleBulkImport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!csvContent.trim()) return;

    setIsImporting(true);
    setImportResult(null);

    // Create a Blob file from CSV content
    const blob = new Blob([csvContent], { type: "text/csv" });
    const formData = new FormData();
    formData.append("file", blob, "employees.csv");

    try {
      const res = await apiClient.post("/organizations/import/csv", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setImportResult(res.data);
      // Reload users list
      const updated = await apiClient.get("/users");
      setUsers(updated.data);
    } catch (err: any) {
      setImportResult({
        error: err?.response?.data?.detail || "Import process failed.",
      });
    } finally {
      setIsImporting(false);
    }
  };

  const sampleCsvTemplate = `email,full_name,role,department_code,job_role_title
john.doe@vyora.local,John Doe,EMPLOYEE,ENG,Senior Software Engineer
mary.smith@vyora.local,Mary Smith,EMPLOYEE,ENG,Staff QA Engineer`;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-indigo-400" />
            Employee Directory &amp; Batch CSV Onboarding
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Provision employee records with row-by-row error auditing and import batch ledgers.
          </p>
        </div>

        <button
          onClick={() => setShowImportModal(true)}
          className="flex items-center gap-1.5 px-3.5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition-colors shadow-lg shadow-indigo-600/20"
        >
          <Upload className="w-4 h-4" />
          <span>Batch CSV Import</span>
        </button>
      </div>

      {/* Directory Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-850/60 text-slate-400">
                <th className="py-3 px-4 font-semibold">Full Name</th>
                <th className="py-3 px-4 font-semibold">Corporate Email</th>
                <th className="py-3 px-4 font-semibold">System Role</th>
                <th className="py-3 px-4 font-semibold">Account Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-slate-850/40 transition-colors">
                  <td className="py-3.5 px-4 font-medium text-slate-200">{u.full_name}</td>
                  <td className="py-3.5 px-4 text-slate-400 font-mono">{u.email}</td>
                  <td className="py-3.5 px-4">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-indigo-300 border border-slate-700">
                      {u.role}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    <span className="text-[11px] text-emerald-400 font-medium inline-flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Active
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* CSV Import Modal */}
      {showImportModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 max-w-lg w-full shadow-2xl space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Upload className="w-4 h-4 text-indigo-400" />
              Batch CSV Employee Import
            </h3>
            <p className="text-xs text-slate-400">
              Paste employee records in CSV format. Any invalid rows will be captured in the import error ledger without terminating valid rows.
            </p>

            <div className="flex justify-between items-center text-[11px] text-slate-400">
              <span>Required headers: <code className="text-indigo-400">email,full_name,role,department_code</code></span>
              <button
                type="button"
                onClick={() => setCsvContent(sampleCsvTemplate)}
                className="text-indigo-400 hover:text-indigo-300 underline"
              >
                Insert Sample Data
              </button>
            </div>

            <textarea
              value={csvContent}
              onChange={(e) => setCsvContent(e.target.value)}
              placeholder="email,full_name,role,department_code,job_role_title&#10;..."
              rows={6}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-xs font-mono text-white focus:outline-none focus:border-indigo-500"
            />

            {/* Error Ledger / Result */}
            {importResult && (
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs">
                {importResult.error ? (
                  <div className="text-rose-400">{importResult.error}</div>
                ) : (
                  <div>
                    <div className="font-bold text-emerald-400 mb-1">
                      Batch processed: {importResult.successful_rows} successful, {importResult.failed_rows} failed.
                    </div>
                    {importResult.errors?.length > 0 && (
                      <div className="mt-2 space-y-1 max-h-28 overflow-y-auto font-mono text-[11px] text-rose-300">
                        {importResult.errors.map((err: any, idx: number) => (
                          <div key={idx}>Row {err.row}: {err.error}</div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setShowImportModal(false)}
                className="px-3 py-1.5 text-xs text-slate-400 hover:text-white"
              >
                Close
              </button>
              <button
                type="button"
                onClick={handleBulkImport}
                disabled={isImporting || !csvContent.trim()}
                className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs rounded-lg transition-colors"
              >
                {isImporting ? "Processing CSV..." : "Process Batch Import"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
