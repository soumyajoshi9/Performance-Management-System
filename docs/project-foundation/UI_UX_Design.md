# VYORA — UI/UX Design Specification
**Smart Performance Management & Employee Development Intelligence Platform**

---

## 1. Design Philosophy & User Experience Principles

### 1.1 Core Principles
VYORA's interface is intentionally designed to counter the psychological dread traditionally associated with HR appraisal software. It is built upon five foundational UX tenets:
1. **Explainability Over Numbers:** Every single score, chart, or badge must provide an immediate, accessible drill-down explaining *how* it was calculated, *what evidence* was audited, and *what limitations* apply.
2. **Context Before Judgment:** Workload metrics, task complexities, and active blocker logs are surfaced alongside performance indicators to prevent superficial misinterpretation.
3. **Collaborative Parity:** Development plans and qualitative feedback are framed as peer coaching dialogues rather than top-down edicts, visually emphasizing mutual agreement and shared ownership.
4. **No Hidden States:** Zero data is never shown as a false low score. Empty states, missing data, and insufficient evidence are presented with distinct visual iconography and supportive messaging.
5. **Ergonomic Simplicity (Lean UI):** High data density without visual clutter, utilizing shadcn/ui clean typography, accessible color contrasts, and predictable keyboard navigation.

---

## 2. Design System & Visual Language

### 2.1 Color Palette
Built using Tailwind CSS semantic color tokens:
- **Primary / Brand:** Deep Slate & Indigo (`#0f172a` background, `#4f46e5` primary accent, `#6366f1` hover). Conveys stability, authority, and modern technical precision.
- **Success / Healthy:** Emerald (`#059669` base, `#10b981` border, `#ecfdf5` background). Used for achieved goals, on-time tasks, and sufficient data coverage.
- **Warning / Contextual Blocker:** Amber (`#d97706` base, `#f59e0b` border, `#fffbeb` background). Used for high workload badges, pending approvals, and moderate delays.
- **Critical / Blocker:** Rose (`#e11d48` base, `#f43f5e` border, `#fff1f2` background). Used for blocked tasks, overdue milestones, and flagged AI insights.
- **Informational / Neutral Context:** Sky Blue (`#0284c7`) and Slate Gray (`#64748b`). Used for informational metrics, N/A indicators, and non-penalizing coverage badges.

### 2.2 Typography & Hierarchy
- **Font Family:** Inter or system sans-serif (`font-sans`). Monospace (`font-mono`) reserved for metric codes, timestamps, and JSON data.
- **Scale:**
  - `Display / Page Title`: 28px (1.75rem), Semi-Bold (600), Line-height 1.2.
  - `Section Header`: 20px (1.25rem), Semi-Bold (600), Line-height 1.3.
  - `Card Header / Metric Title`: 16px (1rem), Medium (500), Line-height 1.4.
  - `Body Text`: 14px (0.875rem), Regular (400), Line-height 1.5.
  - `Captions & Badges`: 12px (0.75rem), Medium (500), Uppercase tracking.

---

## 3. Global Navigation & Layout Architecture

```mermaid
graph TD
    subgraph Global App Shell
        TopNav[Top Header Bar: Org Name, Active Review Period Badge, User Profile, Role Badge]
        SideNav[Sidebar Navigation: Dynamic per Role]
        MainCanvas[Main Content Area: Responsive Container]
    end

    SideNav -->|Employee View| ENav[Overview | Goals & Tasks | Monthly Reviews | Growth & Plans]
    SideNav -->|Manager View| MNav[Team Overview | Review Workbench | Goal Approvals | Team Workload]
    SideNav -->|HR View| HNav[Org Analytics | Employee Directory | KPI Templates | Batch Import]
    SideNav -->|Admin View| ANav[User Accounts | System Settings | Audit Logs | System Health]
```

---

## 4. Screen Inventory & Wireframe Specifications

### 4.1 Screen SC-01: Employee Personal Dashboard (`/dashboard/employee`)
The home dashboard for employees providing immediate situational awareness.

#### Layout Wireframe
```
+---------------------------------------------------------------------------------------+
|  VYORA   [Acme Corp]   Period: November 2026 (10 days left)    [Sarah Chen (Employee)]|
+---------------------------------------------------------------------------------------+
| [Overview]   |  WELCOME BACK, SARAH                                                   |
| Goals        |  Role: Senior Backend Engineer | Dept: Engineering | Mgr: David Miller |
| Tasks        |                                                                        |
| Reviews      | +------------------+ +------------------+ +--------------------------+ |
| Growth Plan  | | GOALS IN FLIGHT  | | MONTHLY TASKS    | | WORKLOAD CONTEXT         | |
|              | | 3 Active (82%)   | | 12 Done / 2 Open | | NORMAL (8 Tasks)         | |
|              | +------------------+ +------------------+ +--------------------------+ |
|              |                                                                        |
|              | PERFORMANCE TREND (Past 6 Months)                                      |
|              | [ Line Chart: Aug (84) -> Sep (88) -> Oct (86) -> Nov (Preview: 89) ]   |
|              |                                                                        |
|              | ACTIVE DEVELOPMENT PLAN                                                |
|              | "Distributed Caching & Async Pipelines" (2 of 4 milestones completed)  |
|              | [Progress Bar: 50%]                                  [View Plan ->]    |
+---------------------------------------------------------------------------------------+
```

### 4.2 Screen SC-02: Manager Review Workbench (`/dashboard/manager/reviews`)
The review workbench where managers inspect calculated metrics, qualitative feedback, and AI narrative drafts before finalization.

#### Layout Wireframe
```
+---------------------------------------------------------------------------------------+
| REVIEW WORKBENCH: Sarah Chen (November 2026)                      Status: DRAFT       |
+---------------------------------------------------------------------------------------+
| [1. EVIDENCE & METRICS]            [2. FEEDBACK & CONTEXT]    [3. AI EXPLANATION]     |
| Data Coverage: 100% [Complete]     Self-Assessment: Submitted  Model: Gemini-1.5-Pro  |
|                                                                                       |
| KPI BREAKDOWN (Deterministic)                                                         |
| Metric Name            Raw Value   Norm Score   Weight   Evidence   Status            |
| Task Completion Rate   92%         92.0         25%      12 tasks   Available [OK]    |
| On-Time Delivery       85%         85.0         25%      12 tasks   Available [OK]    |
| Goal Milestone Prog    80%         80.0         30%      3 goals    Available [OK]    |
| Code Review Quality    4.5/5       90.0         20%      8 reviews  Available [OK]    |
|                                                                                       |
| COMPOSITE CALCULATED SCORE: 86.4 / 100  (All metrics verified)                        |
|                                                                                       |
| AI SYNTHESIS (Draft - Advisory Only)                                                  |
| "Demonstrated sustained velocity across core microservice migration. Successfully    |
| unblocked 3 downstream deliverables. Evidence indicates high architectural focus."   |
| Strengths: Proactive dependency management (Cited: KPI_TASK_COMPLETION).              |
| Recommended Focus: Standardize API error contracts for team junior engineers.        |
|                                                                                       |
| MANAGER REVIEW REMARKS (Required for Finalization)                                    |
| [ Text Area: "Sarah continues to lead by example..."                               ] |
|                                                                                       |
| [ Save Draft ]                                             [ FINALIZE REVIEW (Lock) ] |
+---------------------------------------------------------------------------------------+
```

### 4.3 Screen SC-03: Insufficient Data Review State
When evidence count falls below the required threshold (<50% coverage).

#### Layout Wireframe
```
+---------------------------------------------------------------------------------------+
| REVIEW WORKBENCH: Alex Rivera (November 2026)              Status: INSUFFICIENT DATA  |
+---------------------------------------------------------------------------------------+
|  (!) INSUFFICIENT EVIDENCE DETECTED (Data Coverage: 35%)                              |
|  Employee joined mid-period (Nov 18). Insufficient task logs to generate a valid      |
|  composite score without statistical distortion.                                      |
|                                                                                       |
|  Metric Breakdown:                                                                    |
|  - Task Completion Rate: 100% (2 tasks) -> [Not Available: Requires min 5 tasks]      |
|  - On-Time Delivery: 100% (2 tasks)     -> [Not Available: Requires min 5 tasks]      |
|  - Goal Progress: N/A (No active goals) -> [Not Available]                            |
|                                                                                       |
|  Numerical Composite Score is SUPPRESSED to ensure fairness (BR-007).                 |
|  Please conduct a qualitative onboarding review in the Manager Remarks below.         |
|                                                                                       |
|  [ Submit Qualitative Onboarding Assessment ]                                         |
+---------------------------------------------------------------------------------------+
```

### 4.4 Screen SC-04: Collaborative Development Plan (`/dashboard/growth/plans/{id}`)
Enforces bilateral agreement between Employee and Manager.

#### Layout Wireframe
```
+---------------------------------------------------------------------------------------+
| DEVELOPMENT PLAN: Advanced System Observability & Tracing                             |
| Status: PROPOSED (Awaiting Employee Agreement)                                        |
+---------------------------------------------------------------------------------------+
| Objective: Build mastery in OpenTelemetry instrumentation and distributed tracing.     |
| Timeline: Dec 01, 2026 -> Jan 31, 2027 (60 Days)                                      |
|                                                                                       |
| ACTION ITEMS & MILESTONES:                                                            |
| [ ] 1. Complete OpenTelemetry Python SDK Practitioner Course (Target: Dec 15)         |
| [ ] 2. Draft RFC for centralized tracing spans in core auth gateway (Target: Jan 10)  |
| [ ] 3. Implement tracing middleware in staging environment (Target: Jan 25)           |
|                                                                                       |
| DIGITAL AGREEMENT AUDIT:                                                              |
| [X] Manager Agreed: David Miller on 2026-11-20T14:30:00Z                              |
| [ ] Employee Agreement:                                                               |
|     [ ] "I have reviewed these growth goals and agree to this action plan."           |
|                                                                                       |
| [ Request Revisions ]                                        [ AGREE & ACTIVATE PLAN ]|
+---------------------------------------------------------------------------------------+
```

---

## 5. Specialized UX Interaction Workflows

### 5.1 AI Insight Verification & Flagging Workflow
1. User (Employee or Manager) views the AI Narrative card on their review.
2. Every generated claim displays a small pill link referencing the supporting metric (e.g., `[Evidence: KPI_TASK_COMPLETION]`).
3. Hovering the pill displays a tooltip with the exact metric value, date range, and task counts.
4. If an assertion is inaccurate, the user clicks the "Flag Insight" button.
5. A modal opens with required field: "Please explain the factual inaccuracy".
6. Submitting the flag updates `ai_insights.status` to `FLAGGED` and records the reason in `ai_insights.flag_reason`. A warning icon indicates the insight is under dispute.

### 5.2 Bulk Employee CSV Onboarding Workflow
1. HR clicks "Import Employees" in Directory screen.
2. A modal displays: "Download Standard CSV Template" link + Drag-and-Drop file area.
3. Upon file selection, frontend checks file extension (`.csv` or `.xlsx`) and size (<5MB).
4. User clicks "Validate & Import".
5. Backend executes row-by-row validation.
6. Results Card renders:
   - Success badge with count of imported records.
   - If errors exist: Warning banner with an expandable table displaying:
     - `Row Number` | `Supplied Email` | `Validation Error Description`.
   - HR can download the error ledger as a filtered `.csv` for quick correction.

---

## 6. Accessibility & State Management

### 6.1 State Envelopes (Loading, Empty, Error)
- **Loading Skeleton:** Custom pulse skeleton components (`shadcn/skeleton`) matching the exact shape of cards and tables to prevent layout shift.
- **Empty State:** Clean SVG illustration, friendly title (e.g., "No Active Tasks"), descriptive subtext ("You have completed all scheduled tasks for this week"), and a distinct CTA button ("Create New Task").
- **Error State:** Descriptive inline alert card with retry action button and unique correlation `request_id` for technical support.

### 6.2 Accessibility Standards (WCAG 2.1 AA)
- Minimum color contrast ratio of 4.5:1 for normal text and 3:1 for large graphical elements against background.
- Full keyboard focus rings (`focus-visible:ring-2 focus-visible:ring-indigo-500`).
- Screen reader accessibility using ARIA attributes (`aria-expanded`, `aria-describedby`, `role="status"`).

---
*End of UI/UX Design Specification.*
