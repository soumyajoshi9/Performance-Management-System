export type UserRole = "EMPLOYEE" | "MANAGER" | "HR" | "ADMIN";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  department_id?: string | null;
  job_role_id?: string | null;
  manager_id?: string | null;
  is_active: boolean;
  department?: { id: string; name: string; code: string } | null;
  job_role?: { id: string; title: string; level: string } | null;
}

export interface ReviewPeriod {
  id: string;
  name: string;
  start_date: string;
  end_date: string;
  status: "UPCOMING" | "ACTIVE" | "EVALUATION" | "CLOSED";
}

export interface Goal {
  id: string;
  employee_id: string;
  title: string;
  category: "PROJECT" | "DEVELOPMENT" | "OPERATIONAL";
  target_metric: string;
  start_value: number;
  target_value: number;
  current_value: number;
  progress_percentage: number;
  due_date: string;
  status: "ACTIVE" | "COMPLETED" | "CANCELLED" | "PENDING_APPROVAL" | "REJECTED";
  approval_status: "PENDING" | "APPROVED" | "REJECTED";
}

export interface Task {
  id: string;
  employee_id: string;
  title: string;
  status: "TODO" | "IN_PROGRESS" | "BLOCKED" | "COMPLETED";
  priority: "LOW" | "MEDIUM" | "HIGH" | "URGENT";
  complexity: "LOW" | "MEDIUM" | "HIGH";
  due_date: string;
  completed_at?: string | null;
  blocker_reason?: string | null;
  goal_id?: string | null;
}

export interface MetricScoreBreakdown {
  kpi_code: string;
  kpi_name: string;
  raw_value: number | null;
  normalized_score: number | null;
  assigned_weight: number;
  applied_weight: number;
  data_sufficient: boolean;
  insufficient_reason?: string | null;
  unit: string;
}

export interface ScorePreview {
  employee_id: string;
  review_period_id: string;
  calculated_score: number | null;
  score_status: "CALCULATED" | "INSUFFICIENT_DATA" | "PENDING";
  data_coverage_percentage: number;
  metrics: MetricScoreBreakdown[];
  workload_context?: {
    total_tasks: number;
    completed_tasks: number;
    avg_complexity_weight: number;
    workload_status: "NORMAL" | "HIGH_WORKLOAD" | "OVERLOADED";
  };
}

export interface AIInsightOutput {
  summary: string;
  strengths: string[];
  growth_areas: string[];
  recommendations: string[];
  evidence_references: string[];
  data_confidence: string;
  disclaimer: string;
}

export interface AIInsight {
  id: string;
  employee_id: string;
  review_period_id: string;
  status: "GENERATED" | "FLAGGED" | "SUPERSEDED";
  model_version: string;
  structured_output: AIInsightOutput;
  created_at: string;
}

export interface ActionItem {
  id: string;
  title: string;
  description?: string;
  target_date?: string;
  is_completed: boolean;
}

export interface DevelopmentPlan {
  id: string;
  employee_id: string;
  manager_id: string;
  review_period_id?: string;
  title: string;
  objective: string;
  status: "PROPOSED" | "IN_PROGRESS" | "COMPLETED" | "ABANDONED";
  manager_agreed: boolean;
  employee_agreed: boolean;
  start_date: string;
  target_completion_date: string;
  action_items: ActionItem[];
}

export interface AuditLog {
  id: string;
  timestamp: string;
  actor_id?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  details?: Record<string, any>;
  ip_address?: string;
}
