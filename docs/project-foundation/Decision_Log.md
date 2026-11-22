# VYORA — Project Decision Log & Architecture Register
**Smart Performance Management & Employee Development Intelligence Platform**

---

## 1. Decision Status Register

This register documents all architectural, algorithmic, domain, and scope decisions for VYORA. Statuses strictly follow:
- **`[APPROVED]`**: Explicitly authorized by the project owner. Authoritative and binding.
- **`[PROPOSED — REQUIRES APPROVAL]`**: Architecturally recommended but pending stakeholder confirmation.
- **`[DEFERRED]`**: Formally postponed to a future release cycle.
- **`[REJECTED]`**: Explicitly evaluated and prohibited from implementation.
- **`[TBD — DECISION REQUIRED]`**: Open issue requiring business resolution before completion.

---

## 2. Decision Catalog

### Category A: Relational Database Decisions (DB)

| Decision ID | Date | Category | Status | Summary of Decision |
| :--- | :--- | :--- | :---: | :--- |
| **DEC-DB-01** | 2026-11-21 | Database | **`[APPROVED]`** | **Performance Evaluation Unit:** Evaluations are structured per employee per review period. Goals and tasks provide supporting operational evidence. |
| **DEC-DB-02** | 2026-11-21 | Database | **`[APPROVED]`** | **Simple Org Hierarchy:** Employees belong to a Department and a Job Role. Complex multi-level reporting graphs or matrix teams are excluded. |
| **DEC-DB-03** | 2026-11-21 | Database | **`[APPROVED]`** | **Dual Goal Creation:** Both manager-assigned and employee-created goals are supported. Employee-created goals require manager approval (`PENDING_APPROVAL`). |
| **DEC-DB-04** | 2026-11-21 | Database | **`[APPROVED]`** | **Optional Task-to-Goal Linking:** Tasks can optionally link to goals (`goal_id` nullable). Independent operational tasks are fully valid. |
| **DEC-DB-05** | 2026-11-21 | Database | **`[APPROVED]`** | **Feedback Scope:** Initial feedback includes Manager-to-Employee feedback and Employee self-assessments. 360-degree and peer feedback are excluded. |
| **DEC-DB-06** | 2026-11-21 | Database | **`[APPROVED]`** | **Lightweight Formal Review Entity:** Single formal review entity (`performance_reviews`) storing scores, review period, reviewer, summary, and status. |
| **DEC-DB-07** | 2026-11-21 | Database | **`[APPROVED]`** | **Immutable Finalized Snapshots:** Finalized reviews permanently freeze scores, raw values, applied weights, normalization versions, and evidence counts in `review_metric_snapshots`. |

---

### Category B: Performance Scoring & Analytics Decisions (PS)

| Decision ID | Date | Category | Status | Summary of Decision |
| :--- | :--- | :--- | :---: | :--- |
| **DEC-PS-01** | 2026-11-21 | Scoring | **`[APPROVED]`** | **Evidence-Based Framework:** Overall performance combines task completion, goal progress, quality, consistency, and deadline adherence. |
| **DEC-PS-02** | 2026-11-21 | Scoring | **`[APPROVED]`** | **Role-Specific KPIs:** Shared base framework with role-specific KPI templates. Software engineers, sales, and HR use distinct metric configs. |
| **DEC-PS-03** | 2026-11-21 | Scoring | **`[PROPOSED — REQUIRES APPROVAL]`** | **Scoring Weight Distribution:** Proposed baseline weights (Goal 30%, Task 25%, Deadline 20%, Quality 15%, Consistency 10%). Final weights require formal approval. |
| **DEC-PS-04** | 2026-11-21 | Scoring | **`[APPROVED]`** | **Task Complexity as Context:** Task complexity (Low, Medium, High) provides contextual interpretation of workload and must NOT act as a direct score modifier. |
| **DEC-PS-05** | 2026-11-21 | Scoring | **`[PROPOSED — REQUIRES APPROVAL]`** | **Deadline Scoring Algorithm:** Proposed: On-time delivery rate with grace period for documented external blockers. Final method requires formal approval. |
| **DEC-PS-06** | 2026-11-21 | Scoring | **`[PROPOSED — REQUIRES APPROVAL]`** | **Role-Appropriate Quality Metrics:** Software: defect/rework rate; Support: customer satisfaction; Sales: deal accuracy. Data requirements documented. |
| **DEC-PS-07** | 2026-11-21 | Scoring | **`[APPROVED]`** | **Hybrid Missing Data & Coverage Audit:** Missing data is never treated as zero. Failed thresholds mark KPIs `Not Available`. Coverage <50% triggers `INSUFFICIENT_DATA`. |
| **DEC-PS-08** | 2026-11-21 | Scoring | **`[APPROVED]`** | **Review Cadence:** Monthly formal review finalizations supported by continuous underlying analytics. |

---

### Category C: AI System & Safety Decisions (AI)

| Decision ID | Date | Category | Status | Summary of Decision |
| :--- | :--- | :--- | :---: | :--- |
| **DEC-AI-01** | 2026-11-21 | AI | **`[APPROVED]`** | **AI Responsibilities:** Explaining scores, summarizing feedback, identifying strengths/growth areas, suggesting training, drafting development plans. |
| **DEC-AI-02** | 2026-11-21 | AI | **`[APPROVED]`** | **Data Minimization:** LLM receives aggregated metrics, goals, tasks, feedback, and workload context. Passwords, tokens, and unrelated data are never sent. |
| **DEC-AI-03** | 2026-11-21 | AI | **`[APPROVED]`** | **PII Anonymization:** Employee names, emails, and direct UUIDs are stripped and mapped to ephemeral pseudonyms (`SUBJECT_A`) before LLM API calls. |
| **DEC-AI-04** | 2026-11-21 | AI | **`[APPROVED]`** | **Fact Grounding & Citation:** Project-specific assertions must cite supplied metric codes (`evidence_references`). Hallucinations are flagged by backend validator. |
| **DEC-AI-05** | 2026-11-21 | AI | **`[APPROVED]`** | **Structured JSON Output:** AI outputs must strictly conform to Pydantic `AIInsightOutputSchema`. Free-form conversational text is rejected. |
| **DEC-AI-06** | 2026-11-21 | AI | **`[APPROVED]`** | **Bilateral Development Plan Agreement:** AI drafts growth plans, but both Employee and Manager must review, edit, and digitally agree before activation. |
| **DEC-AI-07** | 2026-11-21 | AI | **`[APPROVED]`** | **Prohibited Autonomous Actions:** AI is strictly forbidden from calculating scores or recommending termination, promotion, salary, or disciplinary action. |
| **DEC-AI-08** | 2026-11-21 | AI | **`[APPROVED]`** | **User Controls & Dispute Logging:** Users can flag inaccurate AI insights with mandatory explanations. System displays supporting evidence alongside insights. |

---

### Category D: MVP Scope & Product Boundaries (MVP)

| Decision ID | Date | Category | Status | Summary of Decision |
| :--- | :--- | :--- | :---: | :--- |
| **DEC-MVP-01** | 2026-11-21 | Scope | **`[APPROVED]`** | **Target Market:** Small and Medium-Sized Businesses (SMBs) with 20 to 500 knowledge workers. |
| **DEC-MVP-02** | 2026-11-21 | Scope | **`[APPROVED]`** | **Supported Roles:** Exactly 4 system roles: Employee, Manager / Team Leader, HR Specialist, and System Administrator. |
| **DEC-MVP-03** | 2026-11-21 | Scope | **`[APPROVED]`** | **Employee Onboarding:** Manual creation and batch CSV/Excel import with row-by-row validation and partial commit error logging. |
| **DEC-MVP-04** | 2026-11-21 | Scope | **`[REJECTED]`** | **Payroll & Attendance Exclusion:** Payroll, salary calculation, biometric tracking, timesheets, and leave management are strictly out of scope. |
| **DEC-MVP-05** | 2026-11-21 | Scope | **`[REJECTED]`** | **Recruitment / ATS Exclusion:** Applicant tracking, job postings, and candidate pipelines are strictly out of scope. |
| **DEC-MVP-06** | 2026-11-21 | Scope | **`[REJECTED]`** | **Full LMS Platform Exclusion:** No video course hosting or SCORM engines. Curated skill suggestions and external resource links only. |
| **DEC-MVP-07** | 2026-11-21 | Scope | **`[DEFERRED]`** | **Live External Integrations:** Bi-directional sync with Jira, GitHub, Slack, and HRIS platforms is deferred to post-MVP (CSV/Excel only). |
| **DEC-MVP-08** | 2026-11-21 | Architecture | **`[APPROVED]`** | **Architecture Pattern:** Modular Monolith using FastAPI, Next.js, and PostgreSQL. Microservices and Kubernetes are strictly prohibited. |
| **DEC-MVP-09** | 2026-11-21 | Scope | **`[REJECTED]`** | **Employee Surveillance Exclusion:** Keystroke monitoring, screenshot capture, webcam access, and intrusive background tracking are prohibited. |

---

## 3. Detailed Decision Records

### Detailed Record: DEC-PS-03 (Scoring Weights Model)
- **Status:** **`[PROPOSED — REQUIRES APPROVAL]`**
- **Context:** While PS-1 establishes that scores combine task completion, goal progress, quality, consistency, and deadline adherence, the exact numerical weights have NOT been approved.
- **Options Considered:**
  1. *Equal Weighting:* 20% across all 5 dimensions. (Too rigid; devalues major project goals).
  2. *Proposed Differentiated Weighting:* Goal Achievement 30%, Task Completion 25%, Deadline Adherence 20%, Quality 15%, Consistency 10%.
  3. *Role-Configurable Weights:* HR defines weights per Job Role in `role_kpi_configs`.
- **Decision / Recommendation:** Adopt Option 3 (Role-Configurable Weights) with Option 2 as the initial default template. 
- **Consequence:** Documentation must explicitly display weights with `[NOT FINALIZED — REQUIRES VALIDATION AND APPROVAL]` until stakeholder sign-off.

---

### Detailed Record: DEC-PS-05 (Deadline Scoring Method)
- **Status:** **`[PROPOSED — REQUIRES APPROVAL]`**
- **Context:** Measuring deadline adherence fairly requires handling external delays, task cancellations, and approved date changes without penalizing workers.
- **Options Considered:**
  1. *Binary On-Time Rate:* Completed on or before due date = 100%, late = 0%. (Penalizes minor 1-hour delays equally with 2-week delays).
  2. *Grace-Period & Blocker-Aware Scoring:* Tasks completed within a 24-hour grace window count as on-time. If a task was marked `BLOCKED` with an approved reason, the blocker duration is subtracted from the overdue duration.
- **Decision / Recommendation:** Propose Option 2 (Blocker-Aware Deadline Scoring).
- **Consequence:** Requires tracking blocker timestamps in `tasks.blocked_reason` and auditing manager notes. Clearly document this limitation.

---

### Detailed Record: DEC-DB-07 (Review Immutability)
- **Status:** **`[APPROVED]`**
- **Context:** When an employee receives a formal performance evaluation, future modifications to their current tasks or subsequent changes to company-wide KPI templates must not alter finalized review records.
- **Decision:** When a review is finalized, all metrics, normalized scores, applied weights, normalization versions, evidence counts, and narrative summaries are written to `review_metric_snapshots`. The review is locked.
- **Consequence:** Full point-in-time explainability is guaranteed indefinitely. Historical audits can reconstruct the exact evaluation without re-running modern scoring algorithms.

---
*End of Project Decision Log & Architecture Register.*
