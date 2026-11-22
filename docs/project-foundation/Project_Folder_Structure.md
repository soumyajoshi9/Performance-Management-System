# VYORA — Project Repository & Directory Architecture
**Smart Performance Management & Employee Development Intelligence Platform**

---

## 1. Architectural Philosophy
VYORA is structured as a **Modular Monolith** stored in a single unified Git repository.
The directory organization adheres to strict separation of concerns, domain-driven modularity, clean architecture boundaries, and maximum developer ergonomic clarity.

```
performance-management-system/
├── backend/                  # Python 3.11+ / FastAPI Modular Monolith Backend
├── frontend/                 # Next.js 14+ / React / TypeScript Web Client
├── docs/                     # Authoritative Project Documentation Foundation
├── deploy/                   # Production Deployment Configurations & Scripts
├── scripts/                  # Developer Utilities, Seeders, & Migration Helpers
├── .gitignore                # Git Exclusion Configuration
├── README.md                 # Project Overview & Quickstart Guide
└── docker-compose.yml        # Local Development Multi-Container Composition
```

---

## 2. Backend Directory Structure (`backend/`)

The backend is built with FastAPI, SQLAlchemy 2.0 (async/sync), Pydantic v2, and Alembic.

```
backend/
├── alembic/                          # Alembic Database Migration Scripts
│   ├── versions/                     # Linear migration revision scripts
│   └── env.py                        # Alembic migration environment runtime
├── app/
│   ├── api/                          # HTTP Routing & API Layer
│   │   ├── v1/                       # API Version 1 Routers
│   │   │   ├── auth.py               # Authentication & token endpoints
│   │   │   ├── organizations.py      # Departments, job roles, batch imports
│   │   │   ├── users.py              # Employee roster and profile routes
│   │   │   ├── review_periods.py     # Monthly period schedules
│   │   │   ├── goals.py              # Goal CRUD and approval endpoints
│   │   │   ├── tasks.py              # Task lifecycle and blocker endpoints
│   │   │   ├── kpis.py               # KPI catalog and role template endpoints
│   │   │   ├── scoring.py            # Scoring preview and breakdown endpoints
│   │   │   ├── feedbacks.py          # Qualitative feedback & self-assessment
│   │   │   ├── reviews.py            # Review finalization & snapshot endpoints
│   │   │   ├── ai.py                 # AI narrative synthesis & flagging
│   │   │   ├── development_plans.py  # Development plans and mutual agreement
│   │   │   └── audit.py              # System health and audit log endpoints
│   │   ├── dependencies.py           # FastAPI dependency injection (DB, Auth, RBAC)
│   │   └── router.py                 # Aggregated v1 APIRouter registration
│   │
│   ├── core/                         # Core Infrastructure & Configuration
│   │   ├── config.py                 # Pydantic Settings (Environment variables)
│   │   ├── security.py               # Password hashing (Argon2), JWT encoding/decoding
│   │   ├── exceptions.py             # Domain-specific custom exception classes
│   │   └── logging.py                # Structured JSON logging configuration
│   │
│   ├── database/                     # Relational Persistence Layer
│   │   ├── session.py                # SQLAlchemy engine and sessionmaker
│   │   └── base.py                   # Declarative base model class
│   │
│   ├── models/                       # SQLAlchemy ORM Relational Models
│   │   ├── organization.py           # Department, JobRole entities
│   │   ├── user.py                   # User entity with RBAC roles
│   │   ├── review_period.py          # ReviewPeriod entity
│   │   ├── goal.py                   # Goal entity with approval state
│   │   ├── task.py                   # Task entity with complexity and blockers
│   │   ├── kpi.py                    # KPIDefinition, RoleKPIConfig entities
│   │   ├── feedback.py               # Feedback entity (manager and self)
│   │   ├── review.py                 # PerformanceReview, ReviewMetricSnapshot
│   │   ├── ai_insight.py             # AIInsight entity
│   │   ├── development_plan.py       # DevelopmentPlan entity
│   │   ├── import_batch.py           # ImportBatch ledger entity
│   │   └── audit_log.py              # AuditLog entity
│   │
│   ├── schemas/                      # Pydantic Request/Response Data Contracts
│   │   ├── auth.py                   # Login, Token, Refresh schemas
│   │   ├── organization.py           # Department, JobRole, BatchImport schemas
│   │   ├── user.py                   # UserRead, UserCreate, Profile schemas
│   │   ├── goal.py                   # GoalCreate, GoalUpdate, GoalResponse schemas
│   │   ├── task.py                   # TaskCreate, TaskStatusUpdate schemas
│   │   ├── kpi.py                    # KPIDefinition, RoleConfig schemas
│   │   ├── scoring.py                # ScoreBreakdown, MetricScore schemas
│   │   ├── feedback.py               # FeedbackCreate, SelfAssessment schemas
│   │   ├── review.py                 # ReviewFinalize, SnapshotRead schemas
│   │   ├── ai.py                     # AIInsightOutputSchema, FlagInsight schemas
│   │   └── development_plan.py       # PlanCreate, Milestone schemas
│   │
│   ├── services/                     # Business Logic & Domain Services
│   │   ├── auth_service.py           # Credential validation, token issuance
│   │   ├── organization_service.py   # Hierarchy management, CSV parsing & validation
│   │   ├── goal_service.py           # Goal lifecycle, approval business rules
│   │   ├── task_service.py           # Task management, blocker tracking
│   │   ├── review_service.py         # Review orchestration, snapshot freezing
│   │   ├── development_service.py    # Bilateral plan agreement logic
│   │   └── audit_service.py          # Append-only security audit dispatcher
│   │
│   ├── analytics/                    # Deterministic Scoring & Analytics Engine
│   │   ├── engine.py                 # Main scoring coordinator
│   │   ├── metrics.py                # Individual KPI calculation algorithms
│   │   ├── normalizer.py             # Bounded linear normalization algorithms
│   │   ├── coverage.py               # Evidence threshold auditor & coverage %
│   │   └── workload.py               # Workload context & complexity indexer
│   │
│   ├── ai/                           # AI Integration & Governance Layer
│   │   ├── client.py                 # Google Gemini API client integration
│   │   ├── anonymizer.py             # PII stripping & pseudonymous mapping
│   │   ├── prompt_templates.py       # Versioned prompt strings and contracts
│   │   ├── validator.py              # Pydantic schema validation & retry loop
│   │   └── grounding_audit.py        # Evidence citation verifier against metrics
│   │
│   └── main.py                       # FastAPI application entrypoint and middleware
│
├── tests/                            # Automated Test Suites (Pytest)
│   ├── conftest.py                   # Pytest fixtures, test DB, mock clients
│   ├── unit/                         # Unit Tests
│   │   ├── test_scoring_engine.py    # Deterministic scoring & weight redistribution
│   │   ├── test_normalizer.py        # Boundary math tests
│   │   ├── test_anonymizer.py        # PII stripping verification
│   │   └── test_ai_validator.py      # Schema enforcement & citation checker
│   ├── integration/                  # Integration Tests
│   │   ├── test_auth_api.py          # JWT login, refresh, RBAC access
│   │   ├── test_csv_import.py        # Batch import parser & error reporting
│   │   ├── test_goal_approval.py     # Approval workflow state transitions
│   │   └── test_review_snapshot.py   # Finalization snapshot immutability
│   └── e2e/                          # Critical End-to-End Test Journeys
│       └── test_monthly_cycle.py     # Full cycle: Task -> Score -> AI -> Review -> Plan
│
├── alembic.ini                       # Alembic Database Migration Configuration
├── pyproject.toml                    # Poetry / Pip dependencies and project metadata
└── requirements.txt                  # Pinned Python package dependencies
```

---

## 3. Frontend Directory Structure (`frontend/`)

The frontend is built with Next.js 14+ (App Router), React 18+, TypeScript, Tailwind CSS, and shadcn/ui.

```
frontend/
├── public/                           # Static assets, brand logos, icons
├── src/
│   ├── app/                          # Next.js App Router Pages & Layouts
│   │   ├── (auth)/                   # Authentication route group
│   │   │   ├── login/                # Login screen
│   │   │   └── reset-password/       # Password recovery screen
│   │   ├── (dashboard)/              # Authenticated application shell
│   │   │   ├── layout.tsx            # Global dashboard layout with sidebar
│   │   │   ├── employee/             # Employee portal screens
│   │   │   │   ├── page.tsx          # Personal overview dashboard
│   │   │   │   ├── goals/            # Goal tracker & submission
│   │   │   │   ├── tasks/            # Task management & Kanban board
│   │   │   │   ├── reviews/          # Monthly reviews & score inspector
│   │   │   │   └── growth/           # Collaborative development plans
│   │   │   ├── manager/              # Manager coaching hub
│   │   │   │   ├── page.tsx          # Team overview dashboard
│   │   │   │   ├── reviews/          # Review workbench & finalization
│   │   │   │   ├── approvals/        # Goal approval queue
│   │   │   │   └── workload/         # Team workload distribution heatmap
│   │   │   ├── hr/                   # Human Resources governance hub
│   │   │   │   ├── page.tsx          # Organization-wide analytics
│   │   │   │   ├── directory/        # Employee roster & batch CSV import
│   │   │   │   ├── kpi-templates/    # Role-specific KPI configurations
│   │   │   │   └── periods/          # Review period scheduling
│   │   │   └── admin/                # System administration
│   │   │       ├── users/            # User account provisioning
│   │   │       └── audit-logs/       # Security & operational audit inspector
│   │   ├── globals.css               # Tailwind CSS base styles & CSS variables
│   │   └── layout.tsx                # Root HTML layout with font providers
│   │
│   ├── components/                   # Reusable UI Component Library
│   │   ├── ui/                       # shadcn/ui primitives (button, dialog, card, etc.)
│   │   ├── charts/                   # Recharts wrappers (Radar, Trends, Distributions)
│   │   ├── scoring/                  # ScoreBreakdownCard, CoverageBadge, MetricRow
│   │   ├── ai/                       # AINarrativeCard, EvidencePill, FlagInsightModal
│   │   ├── workload/                 # WorkloadBadge, ComplexityTag, BlockerAlert
│   │   └── layout/                   # TopNav, Sidebar, RoleSwitcher, UserMenu
│   │
│   ├── hooks/                        # Custom React Hooks
│   │   ├── use-auth.ts               # Auth context, user profile, role guard
│   │   ├── use-review.ts             # Review fetching, scoring preview, finalization
│   │   └── use-goals-tasks.ts        # Task status transitions, goal progress
│   │
│   ├── lib/                          # Client Utilities & HTTP Clients
│   │   ├── api-client.ts             # Axios / Fetch client with Bearer interceptors
│   │   ├── utils.ts                  # Classnames merger (cn), formatting helpers
│   │   └── validators.ts             # Zod form validation schemas
│   │
│   └── types/                        # TypeScript Interface & Type Definitions
│       ├── api.ts                    # API standard response envelopes
│       ├── user.ts                   # User, Department, JobRole types
│       ├── review.ts                 # PerformanceReview, MetricSnapshot, KPI types
│       ├── goal-task.ts              # Goal, Task, Priority, Complexity types
│       └── ai.ts                     # AIInsight, DevelopmentPlan types
│
├── package.json                      # Node.js dependencies and build scripts
├── tailwind.config.ts                # Tailwind CSS design token configuration
├── tsconfig.json                     # TypeScript strict compilation configuration
└── next.config.mjs                   # Next.js runtime configuration
```

---

## 4. Documentation & Operational Infrastructure (`docs/`, `deploy/`)

```
docs/
├── project-foundation/               # Authoritative Project Foundation (16 Documents)
│   ├── Project_Overview.md           # Vision, problem, scope, boundaries
│   ├── Project_Requirements_SRS.md   # Formal functional & non-functional requirements
│   ├── Feature_List.md               # Feature catalog with priority & complexity
│   ├── System_Architecture.md        # Modular monolith C4 architecture & data flow
│   ├── Database_Design.md            # Relational design, data dictionary, normalization
│   ├── Database_ERD.png              # High-resolution rendered ER diagram
│   ├── Database_Schema.sql           # Production PostgreSQL DDL statements
│   ├── API_Documentation.md          # REST API OpenAPI contracts & payloads
│   ├── UI_UX_Design.md               # Visual design, wireframes, interaction workflows
│   ├── Project_Folder_Structure.md   # Repository structure & responsibilities
│   ├── Coding_Standards.md           # Engineering guidelines (Python, TypeScript, Git)
│   ├── Authentication_and_Security.md# RBAC, encryption, prompt injection defense
│   ├── AI_Project_Instructions.md    # Rulebook for future AI coding agents
│   ├── Development_Progress.md       # Honest milestone & task tracker
│   ├── Decision_Log.md               # Approved, proposed, and deferred decisions
│   └── Project_Summary.md            # Standalone comprehensive onboarding summary

deploy/
├── nginx/                            # Production Nginx reverse proxy configuration
│   └── default.conf                  # SSL termination, static routing, API proxying
├── Dockerfile.backend                # Optimized Python 3.11 FastAPI container
├── Dockerfile.frontend               # Multi-stage standalone Next.js container
└── docker-compose.prod.yml           # Production-ready single-node orchestrator
```

---
*End of Project Repository & Directory Architecture.*
