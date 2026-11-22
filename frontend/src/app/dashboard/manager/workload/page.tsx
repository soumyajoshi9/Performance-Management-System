"use client";

import React, { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";
import { User, Task } from "@/types";
import { Scale, Users, ShieldAlert, CheckCircle2 } from "lucide-react";
import { WorkloadBadge, ComplexityBadge } from "@/components/workload/workload-badge";

export default function WorkloadHeatmapPage() {
  const [employees, setEmployees] = useState<User[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    async function loadData() {
      try {
        const [usersRes, tasksRes] = await Promise.all([
          apiClient.get("/users"),
          apiClient.get("/tasks"),
        ]);
        setEmployees(usersRes.data.filter((u: User) => u.role === "EMPLOYEE"));
        setTasks(tasksRes.data);
      } catch (err) {
        console.error("Failed to load workload data:", err);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
          <Scale className="w-5 h-5 text-indigo-400" />
          Team Workload Distribution &amp; Task Complexity Analysis
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Monitor capacity in real time so high complexity task allocations are properly accounted for in monthly reviews.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {employees.map((emp) => {
          const empTasks = tasks.filter((t) => t.employee_id === emp.id);
          const completed = empTasks.filter((t) => t.status === "COMPLETED").length;
          const blocked = empTasks.filter((t) => t.status === "BLOCKED").length;
          const highComplexity = empTasks.filter((t) => t.complexity === "HIGH").length;

          const workloadStatus = empTasks.length > 10 ? "OVERLOADED" : empTasks.length > 5 ? "HIGH_WORKLOAD" : "NORMAL";

          return (
            <div key={emp.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-sm font-bold text-white">{emp.full_name}</h3>
                  <div className="text-xs text-slate-400 mt-0.5">{emp.email}</div>
                </div>
                <WorkloadBadge status={workloadStatus} totalTasks={empTasks.length} completedTasks={completed} />
              </div>

              <div className="grid grid-cols-3 gap-2 text-center pt-2">
                <div className="bg-slate-850 p-2 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-slate-400 uppercase font-semibold">Total</div>
                  <div className="text-base font-bold text-white mt-0.5">{empTasks.length}</div>
                </div>
                <div className="bg-slate-850 p-2 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-rose-400 uppercase font-semibold">Blocked</div>
                  <div className="text-base font-bold text-rose-400 mt-0.5">{blocked}</div>
                </div>
                <div className="bg-slate-850 p-2 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-purple-400 uppercase font-semibold">High Comp</div>
                  <div className="text-base font-bold text-purple-400 mt-0.5">{highComplexity}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
