# VYORA — Smart Performance Management & Employee Development Intelligence Platform

> *"Don't just measure employee performance. Understand it, explain it, identify risks early, and help people improve."*

---

## 1. What is VYORA?

**VYORA** is an AI-assisted, web-based employee performance evaluation and personalized growth platform built specifically for Small and Medium-Sized Businesses (SMBs). 

Traditional performance management relies on backward-looking, subjective annual reviews where managers assign arbitrary scores. VYORA fundamentally transforms this dynamic into a continuous, evidence-grounded, workload-aware, and explainable feedback loop.

### Core Value Proposition:
$$\text{Measurable Performance} + \text{Context} + \text{Explainability} + \text{Early Signals} + \text{Actionable Development} + \text{Human Oversight}$$

---

## 2. Key Capabilities & Differentiators

- **Evidence-Based Evaluation:** Connects daily tasks and strategic goals directly with monthly formal performance reviews.
- **Deterministic Scoring Engine:** Mathematical scores are calculated 100% deterministically by the backend. The AI never calculates or alters official scores.
- **Workload & Complexity Context:** Displays active task load and complexity distributions alongside metrics without arbitrary numerical score distortions.
- **Hybrid Missing Data Policy:** Missing data is never defaulted to zero. Unmeasured metrics are marked `Not Available`. If overall data coverage is $<50\%$, numerical scoring is suppressed, transitioning the review to an explicit `INSUFFICIENT_DATA` state.
- **Privacy-Preserving AI Coaching:** Large Language Models (Google Gemini) operate behind a strict anonymization proxy (stripping names, emails, and UUIDs) to generate structured narrative summaries, observed strengths, and recommended training resources.
- **Collaborative Development Plans:** Bilateral growth plans that require digital agreement from both the Employee and the Manager before activation.
- **Immutable Historical Snapshots:** When a review is finalized, an immutable snapshot of all metrics, weights, and evidence counts is permanently frozen.

---

## 3. Supported User Roles

1. **Employee:** View expectations, track goals/tasks, view score breakdowns and workload context, submit monthly self-assessments, and participate in collaborative development plans.
2. **Manager / Team Leader:** Oversee assigned team members, review/approve goals, assign tasks, log qualitative feedback, conduct monthly formal reviews, and guide development plans.
3. **HR Specialist:** Manage organization hierarchy (departments, job roles), configure role-specific KPI templates, schedule review periods, conduct CSV/Excel bulk onboarding, and analyze company-wide trends.
4. **System Administrator:** Manage user accounts, authentication policies, system settings, and inspect security audit logs. Administrators have zero automatic access to sensitive employee review narratives.

---

## 4. Technology Stack

- **Frontend:** Next.js 14+ (App Router), React 18+, TypeScript (strict), Tailwind CSS, shadcn/ui, Recharts.
- **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, Uvicorn.
- **Persistence:** PostgreSQL 15+ (with SQLite support for lightweight local development and testing).
- **Security:** Argon2id password hashing, stateless 60-min JWT access tokens, rotating `HttpOnly` refresh cookies, and RBAC middleware.
- **Architecture:** **Modular Monolith** in a single unified repository.

---

## 5. Quickstart Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ or 20+
- PostgreSQL 15+ (or SQLite)

### 1. Configure Environment
```powershell
Copy-Item .env.example .env
```

### 2. Run Backend API
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.database.init_db
uvicorn app.main:app --reload --port 8000
```
- Interactive API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Run Frontend Web Client
```powershell
cd frontend
npm install
npm run dev
```
- Web Application: [http://localhost:3000](http://localhost:3000)

### Default Demo Credentials:
- **Admin:** `admin@vyora.local` / `AdminPass123!`
- **HR:** `hr@vyora.local` / `HrPass123!`
- **Manager:** `manager@vyora.local` / `ManagerPass123!`
- **Employee:** `employee@vyora.local` / `EmployeePass123!`

---

## 6. Project Documentation Links
Detailed authoritative documentation is located in `docs/project-foundation/`:
- [`Project_Summary.md`](docs/project-foundation/Project_Summary.md) — Comprehensive Master Context Document
- [`Project_Overview.md`](docs/project-foundation/Project_Overview.md) — Product Vision, Problem & Boundaries
- [`Project_Requirements_SRS.md`](docs/project-foundation/Project_Requirements_SRS.md) — Software Requirements Specification
- [`Feature_List.md`](docs/project-foundation/Feature_List.md) — Complete Feature Catalog & Priority Matrix
- [`System_Architecture.md`](docs/project-foundation/System_Architecture.md) — Modular Monolith Architecture
- [`Database_Design.md`](docs/project-foundation/Database_Design.md) — 15-Entity Relational Design
- [`Database_ERD.png`](docs/project-foundation/Database_ERD.png) — Rendered ER Diagram Image
- [`Database_Schema.sql`](docs/project-foundation/Database_Schema.sql) — PostgreSQL 15+ DDL
- [`API_Documentation.md`](docs/project-foundation/API_Documentation.md) — OpenAPI RESTful Contracts
- [`UI_UX_Design.md`](docs/project-foundation/UI_UX_Design.md) — Visual Design & Wireframes
- [`Authentication_and_Security.md`](docs/project-foundation/Authentication_and_Security.md) — RBAC & AI Safety
- [`AI_Project_Instructions.md`](docs/project-foundation/AI_Project_Instructions.md) — Rules for AI Coding Agents
- [`Decision_Log.md`](docs/project-foundation/Decision_Log.md) — Approved Decisions Register
- [`Development_Progress.md`](docs/project-foundation/Development_Progress.md) — Implementation Progress Tracker
