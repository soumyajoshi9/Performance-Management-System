import React from "react";
import { AlertTriangle, Clock, ShieldAlert } from "lucide-react";

interface WorkloadBadgeProps {
  status?: "NORMAL" | "HIGH_WORKLOAD" | "OVERLOADED";
  totalTasks?: number;
  completedTasks?: number;
}

export function WorkloadBadge({ status = "NORMAL", totalTasks = 0, completedTasks = 0 }: WorkloadBadgeProps) {
  const getBadgeStyle = () => {
    switch (status) {
      case "OVERLOADED":
        return {
          bg: "bg-rose-950/80 text-rose-300 border-rose-800",
          icon: <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />,
          label: "Overloaded",
        };
      case "HIGH_WORKLOAD":
        return {
          bg: "bg-amber-950/80 text-amber-300 border-amber-800",
          icon: <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />,
          label: "High Workload",
        };
      case "NORMAL":
      default:
        return {
          bg: "bg-emerald-950/80 text-emerald-300 border-emerald-800",
          icon: <Clock className="w-3.5 h-3.5 text-emerald-400" />,
          label: "Normal",
        };
    }
  };

  const style = getBadgeStyle();

  return (
    <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold border ${style.bg}`}>
      {style.icon}
      <span>{style.label}</span>
      <span className="text-[10px] opacity-75">
        ({completedTasks}/{totalTasks} tasks)
      </span>
    </div>
  );
}

export function ComplexityBadge({ complexity }: { complexity: "LOW" | "MEDIUM" | "HIGH" }) {
  const colors = {
    LOW: "bg-slate-800 text-slate-300 border-slate-700",
    MEDIUM: "bg-indigo-950 text-indigo-300 border-indigo-800",
    HIGH: "bg-purple-950 text-purple-300 border-purple-800",
  };

  return (
    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${colors[complexity]}`}>
      {complexity}
    </span>
  );
}
