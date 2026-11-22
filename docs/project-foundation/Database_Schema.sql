-- ============================================================================
-- VYORA — Smart Performance Management & Employee Development Intelligence Platform
-- PostgreSQL Relational Database Schema DDL
-- Specification: Version 1.0.0-MVP
-- Supported Engine: PostgreSQL 15+
-- ============================================================================

-- Enable pgcrypto / uuid extensions for gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- 1. ORGANIZATIONAL HIERARCHY TABLES
-- ============================================================================

-- Table: departments
CREATE TABLE departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_departments_name UNIQUE (name),
    CONSTRAINT uq_departments_code UNIQUE (code)
);

COMMENT ON TABLE departments IS 'Core organizational business units (e.g., Engineering, Sales).';
COMMENT ON COLUMN departments.code IS 'Short uppercase department identifier (e.g., ENG).';

-- Table: job_roles
CREATE TABLE job_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    department_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(30) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_job_roles_department FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT,
    CONSTRAINT uq_job_roles_code UNIQUE (code)
);

CREATE INDEX idx_job_roles_department_id ON job_roles(department_id);
COMMENT ON TABLE job_roles IS 'Professional designations mapping to specific departments and role-specific KPIs.';

-- Table: users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(30) NOT NULL,
    department_id UUID,
    job_role_id UUID,
    manager_id UUID,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT ck_users_role CHECK (role IN ('EMPLOYEE', 'MANAGER', 'HR', 'ADMIN')),
    CONSTRAINT fk_users_department FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    CONSTRAINT fk_users_job_role FOREIGN KEY (job_role_id) REFERENCES job_roles(id) ON DELETE SET NULL,
    CONSTRAINT fk_users_manager FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_users_department_id ON users(department_id);
CREATE INDEX idx_users_job_role_id ON users(job_role_id);
CREATE INDEX idx_users_manager_id ON users(manager_id);
CREATE INDEX idx_users_role ON users(role);
COMMENT ON TABLE users IS 'Unified entity storing authentication, profile, RBAC role, and reporting line.';

-- ============================================================================
-- 2. REVIEW PERIODS & KPI DEFINITIONS
-- ============================================================================

-- Table: review_periods
CREATE TABLE review_periods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    review_month VARCHAR(7) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'UPCOMING',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_review_periods_month UNIQUE (review_month),
    CONSTRAINT ck_review_periods_dates CHECK (end_date >= start_date),
    CONSTRAINT ck_review_periods_status CHECK (status IN ('UPCOMING', 'ACTIVE', 'UNDER_REVIEW', 'COMPLETED', 'ARCHIVED'))
);

CREATE INDEX idx_review_periods_status ON review_periods(status);
COMMENT ON TABLE review_periods IS 'Time-bound evaluation cycles (defaults to calendar months e.g., 2026-11).';

-- Table: kpi_definitions
CREATE TABLE kpi_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(30) NOT NULL,
    unit VARCHAR(30) NOT NULL DEFAULT 'percentage',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_kpi_definitions_code UNIQUE (code),
    CONSTRAINT ck_kpi_definitions_category CHECK (category IN ('TASK', 'GOAL', 'QUALITY', 'CONSISTENCY', 'DEADLINE'))
);

CREATE INDEX idx_kpi_definitions_category ON kpi_definitions(category);
COMMENT ON TABLE kpi_definitions IS 'Standard catalog of quantifiable metrics across performance dimensions.';

-- Table: role_kpi_configs
CREATE TABLE role_kpi_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_role_id UUID NOT NULL,
    kpi_definition_id UUID NOT NULL,
    default_weight NUMERIC(5,2) NOT NULL,
    min_evidence_threshold INTEGER NOT NULL DEFAULT 3,
    is_mandatory BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_role_kpi_configs UNIQUE (job_role_id, kpi_definition_id),
    CONSTRAINT fk_role_kpi_configs_role FOREIGN KEY (job_role_id) REFERENCES job_roles(id) ON DELETE CASCADE,
    CONSTRAINT fk_role_kpi_configs_kpi FOREIGN KEY (kpi_definition_id) REFERENCES kpi_definitions(id) ON DELETE RESTRICT,
    CONSTRAINT ck_role_kpi_configs_weight CHECK (default_weight >= 0.00 AND default_weight <= 100.00),
    CONSTRAINT ck_role_kpi_configs_threshold CHECK (min_evidence_threshold >= 1)
);

CREATE INDEX idx_role_kpi_configs_job_role_id ON role_kpi_configs(job_role_id);
COMMENT ON TABLE role_kpi_configs IS 'Template configuring role-specific KPIs, weights, and minimum evidence thresholds.';

-- ============================================================================
-- 3. GOALS & TASKS
-- ============================================================================

-- Table: goals
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID NOT NULL,
    created_by_id UUID NOT NULL,
    review_period_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL DEFAULT 'PROJECT',
    target_metric VARCHAR(100) NOT NULL,
    start_value NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    target_value NUMERIC(10,2) NOT NULL,
    current_value NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    unit VARCHAR(30) NOT NULL DEFAULT 'percent',
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    approval_status VARCHAR(30) NOT NULL DEFAULT 'APPROVED',
    approved_by_id UUID,
    rejection_reason TEXT,
    due_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_goals_employee FOREIGN KEY (employee_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_goals_created_by FOREIGN KEY (created_by_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_goals_review_period FOREIGN KEY (review_period_id) REFERENCES review_periods(id) ON DELETE RESTRICT,
    CONSTRAINT fk_goals_approved_by FOREIGN KEY (approved_by_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT ck_goals_status CHECK (status IN ('DRAFT', 'PENDING_APPROVAL', 'ACTIVE', 'COMPLETED', 'CANCELLED')),
    CONSTRAINT ck_goals_approval_status CHECK (approval_status IN ('PENDING', 'APPROVED', 'REJECTED'))
);

CREATE INDEX idx_goals_employee_period ON goals(employee_id, review_period_id);
CREATE INDEX idx_goals_approval_status ON goals(approval_status);
COMMENT ON TABLE goals IS 'Measurable targets supporting dual-origin (manager vs. employee) creation.';

-- Table: tasks
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID NOT NULL,
    assigned_by_id UUID NOT NULL,
    goal_id UUID,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'TODO',
    priority VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    complexity VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    due_date TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    is_reopened BOOLEAN NOT NULL DEFAULT FALSE,
    blocked_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_tasks_employee FOREIGN KEY (employee_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_tasks_assigned_by FOREIGN KEY (assigned_by_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_tasks_goal FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE SET NULL,
    CONSTRAINT ck_tasks_status CHECK (status IN ('TODO', 'IN_PROGRESS', 'BLOCKED', 'COMPLETED', 'CANCELLED')),
    CONSTRAINT ck_tasks_priority CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'URGENT')),
    CONSTRAINT ck_tasks_complexity CHECK (complexity IN ('LOW', 'MEDIUM', 'HIGH'))
);

CREATE INDEX idx_tasks_employee_id ON tasks(employee_id);
CREATE INDEX idx_tasks_goal_id ON tasks(goal_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
COMMENT ON TABLE tasks IS 'Day-to-day operational evidence items. goal_id is optionally nullable.';

-- ============================================================================
-- 4. QUALITATIVE FEEDBACK & PERFORMANCE REVIEWS
-- ============================================================================

-- Table: feedbacks
CREATE TABLE feedbacks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID NOT NULL,
    author_id UUID NOT NULL,
    review_period_id UUID NOT NULL,
    feedback_type VARCHAR(30) NOT NULL,
    content TEXT NOT NULL,
    strengths TEXT,
    growth_areas TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_feedbacks_employee FOREIGN KEY (employee_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_feedbacks_author FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_feedbacks_period FOREIGN KEY (review_period_id) REFERENCES review_periods(id) ON DELETE RESTRICT,
    CONSTRAINT ck_feedbacks_type CHECK (feedback_type IN ('MANAGER_TO_EMPLOYEE', 'SELF_ASSESSMENT'))
);

CREATE INDEX idx_feedbacks_employee_period ON feedbacks(employee_id, review_period_id);
COMMENT ON TABLE feedbacks IS 'Structured qualitative manager feedback and employee self-assessments.';

-- Table: performance_reviews
CREATE TABLE performance_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID NOT NULL,
    reviewer_id UUID NOT NULL,
    review_period_id UUID NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'DRAFT',
    score_status VARCHAR(30) NOT NULL DEFAULT 'CALCULATED',
    calculated_score NUMERIC(5,2),
    final_score NUMERIC(5,2),
    data_coverage_percentage NUMERIC(5,2) NOT NULL,
    manager_summary TEXT,
    employee_remarks TEXT,
    finalized_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_performance_reviews_emp_period UNIQUE (employee_id, review_period_id),
    CONSTRAINT fk_performance_reviews_employee FOREIGN KEY (employee_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_performance_reviews_reviewer FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_performance_reviews_period FOREIGN KEY (review_period_id) REFERENCES review_periods(id) ON DELETE RESTRICT,
    CONSTRAINT ck_performance_reviews_status CHECK (status IN ('DRAFT', 'SUBMITTED', 'FINALIZED')),
    CONSTRAINT ck_performance_reviews_score_status CHECK (score_status IN ('CALCULATED', 'INSUFFICIENT_DATA'))
);

CREATE INDEX idx_performance_reviews_reviewer ON performance_reviews(reviewer_id);
CREATE INDEX idx_performance_reviews_period ON performance_reviews(review_period_id);
CREATE INDEX idx_performance_reviews_status ON performance_reviews(status);
COMMENT ON TABLE performance_reviews IS 'Formal evaluation records per employee per review period.';

-- Table: review_metric_snapshots
CREATE TABLE review_metric_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    performance_review_id UUID NOT NULL,
    kpi_code VARCHAR(50) NOT NULL,
    kpi_name VARCHAR(150) NOT NULL,
    category VARCHAR(30) NOT NULL,
    raw_value NUMERIC(10,2),
    normalized_score NUMERIC(5,2),
    applied_weight NUMERIC(5,2) NOT NULL,
    evidence_count INTEGER NOT NULL,
    is_sufficient BOOLEAN NOT NULL,
    data_status VARCHAR(20) NOT NULL,
    snapshot_data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_snapshots_review FOREIGN KEY (performance_review_id) REFERENCES performance_reviews(id) ON DELETE CASCADE,
    CONSTRAINT ck_snapshots_status CHECK (data_status IN ('AVAILABLE', 'NOT_AVAILABLE', 'INSUFFICIENT'))
);

CREATE INDEX idx_snapshots_review_id ON review_metric_snapshots(performance_review_id);
CREATE INDEX idx_snapshots_kpi_code ON review_metric_snapshots(kpi_code);
COMMENT ON TABLE review_metric_snapshots IS 'Frozen historical snapshot table preserving exact metric scores and weights upon review finalization.';

-- ============================================================================
-- 5. AI INTELLIGENCE & DEVELOPMENT PLANS
-- ============================================================================

-- Table: ai_insights
CREATE TABLE ai_insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID NOT NULL,
    performance_review_id UUID,
    review_period_id UUID NOT NULL,
    prompt_version VARCHAR(50) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    structured_output JSONB NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'GENERATED',
    flag_reason TEXT,
    flagged_by_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_ai_insights_employee FOREIGN KEY (employee_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_ai_insights_review FOREIGN KEY (performance_review_id) REFERENCES performance_reviews(id) ON DELETE SET NULL,
    CONSTRAINT fk_ai_insights_period FOREIGN KEY (review_period_id) REFERENCES review_periods(id) ON DELETE RESTRICT,
    CONSTRAINT fk_ai_insights_flagged_by FOREIGN KEY (flagged_by_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT ck_ai_insights_status CHECK (status IN ('GENERATED', 'FLAGGED', 'REVIEWED'))
);

CREATE INDEX idx_ai_insights_employee_period ON ai_insights(employee_id, review_period_id);
COMMENT ON TABLE ai_insights IS 'Structured, schema-validated AI narrative insights and coaching recommendations.';

-- Table: development_plans
CREATE TABLE development_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID NOT NULL,
    manager_id UUID NOT NULL,
    review_period_id UUID,
    ai_insight_id UUID,
    title VARCHAR(255) NOT NULL,
    objective TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'DRAFT',
    employee_agreed BOOLEAN NOT NULL DEFAULT FALSE,
    manager_agreed BOOLEAN NOT NULL DEFAULT FALSE,
    action_items JSONB NOT NULL DEFAULT '[]'::jsonb,
    start_date DATE NOT NULL,
    target_completion_date DATE NOT NULL,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_dev_plans_employee FOREIGN KEY (employee_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_dev_plans_manager FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_dev_plans_period FOREIGN KEY (review_period_id) REFERENCES review_periods(id) ON DELETE SET NULL,
    CONSTRAINT fk_dev_plans_ai_insight FOREIGN KEY (ai_insight_id) REFERENCES ai_insights(id) ON DELETE SET NULL,
    CONSTRAINT ck_dev_plans_status CHECK (status IN ('DRAFT', 'PROPOSED', 'IN_PROGRESS', 'COMPLETED', 'REJECTED')),
    CONSTRAINT ck_dev_plans_dates CHECK (target_completion_date >= start_date)
);

CREATE INDEX idx_dev_plans_employee_id ON development_plans(employee_id);
CREATE INDEX idx_dev_plans_manager_id ON development_plans(manager_id);
CREATE INDEX idx_dev_plans_status ON development_plans(status);
COMMENT ON TABLE development_plans IS 'Collaborative growth platform requiring bilateral digital agreement.';

-- ============================================================================
-- 6. SYSTEM AUDIT & IMPORT LOGGING
-- ============================================================================

-- Table: import_batches
CREATE TABLE import_batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    imported_by_id UUID NOT NULL,
    entity_type VARCHAR(50) NOT NULL DEFAULT 'EMPLOYEE',
    file_name VARCHAR(255) NOT NULL,
    total_rows INTEGER NOT NULL,
    successful_rows INTEGER NOT NULL,
    failed_rows INTEGER NOT NULL,
    error_log JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_import_batches_user FOREIGN KEY (imported_by_id) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE INDEX idx_import_batches_user_id ON import_batches(imported_by_id);
COMMENT ON TABLE import_batches IS 'Audit ledger for CSV/Excel bulk employee onboarding runs.';

-- Table: audit_logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID,
    ip_address VARCHAR(45),
    changes JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_audit_logs_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
COMMENT ON TABLE audit_logs IS 'Immutable administrative and security audit trail.';

-- ============================================================================
-- End of DDL
-- ============================================================================
