"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { apiClient } from "@/lib/api-client";
import { LayoutDashboard, Users, Scale, FileText, ArrowRight, ShieldCheck } from "lucide-react";

export default function HROverviewPage() {
  const [departments, setDepartments] = useState<any[]>([]);
  const [jobRoles, setJobRoles] = useState<any[]>([]);
  const [usersCount, setUsersCount] = useState(0);

  useEffect(() => {
    async function loadOrgData() {
      try {
        const [deptRes, rolesRes, usersRes] = await Promise.all([
          apiClient.get("/organizations/departments"),
          apiClient.get("/organizations/roles"),
          apiClient.get("/users"),
        ]);
        setDepartments(deptRes.data);
        setJobRoles(rolesRes.data);
        setUsersCount(usersRes.data.length);
      } catch (err) {
        console.error("Failed to load org data:", err);
      }
    }
    loadOrgData();
  }, []);

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="text-xs uppercase font-semibold text-indigo-400 tracking-wider">
            Human Resources Management Hub
          </div>
          <h1 className="text-2xl font-extrabold text-white mt-1">
            Organization Structure &amp; People Governance
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Manage organization hierarchy, configure standardized role KPI templates, and perform bulk employee onboarding.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/dashboard/hr/directory"
            className="flex items-center gap-1.5 px-3.5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition-colors shadow-lg shadow-indigo-600/20"
          >
            <Users className="w-3.5 h-3.5" />
            <span>Employee Directory &amp; CSV Import</span>
          </Link>
        </div>
      </div>

      {/* Top Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
            Total Headcount
          </div>
          <div className="text-3xl font-extrabold text-white">{usersCount}</div>
          <div className="text-xs text-emerald-400 mt-1">100% active in November cycle</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
            Departments
          </div>
          <div className="text-3xl font-extrabold text-indigo-400">{departments.length}</div>
          <div className="text-xs text-slate-400 mt-1">Engineering, Sales, HR</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
            Standard Job Roles
          </div>
          <div className="text-3xl font-extrabold text-purple-400">{jobRoles.length}</div>
          <div className="text-xs text-slate-400 mt-1">Configured with KPI weights</div>
        </div>
      </div>

      {/* Department Breakdown */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 mb-4">
          Configured Departments &amp; Functional Units
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {departments.map((d) => (
            <div key={d.id} className="p-4 bg-slate-850 rounded-xl border border-slate-800 space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white text-sm">{d.name}</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-indigo-300 border border-indigo-900">
                  {d.code}
                </span>
              </div>
              <p className="text-xs text-slate-400">{d.description || "Active departmental division."}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
