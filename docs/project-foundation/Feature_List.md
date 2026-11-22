# VYORA — Feature Catalog & Priority Matrix
**Smart Performance Management & Employee Development Intelligence Platform**

---

## 1. Document Overview
This document catalogs all functional and technical features of VYORA. Each entry specifies user roles, priority level, MVP inclusion status, architectural dependencies, traceability to SRS requirements, and explicit acceptance criteria.

### Priority Definition
- **P0 — Essential:** Core to MVP validation. System cannot function or demonstrate primary differentiation without this feature.
- **P1 — Important:** High business value. Required for a complete and polished user journey in production.
- **P2 — Useful:** Enhances ergonomics and operational convenience; included in MVP if implementation cost is lean.
- **P3 — Future / Post-MVP:** Explicitly deferred capabilities for future phases.

---

## 2. Feature Catalog

### Category A: Identity, Access & Directory Management

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-A01** | JWT Authentication & Session Rotation | All Roles | **P0** | **MVP** | None | FR-001, FR-002, NFR-008 | Low |
| **FT-A02** | Role-Based Access Control (RBAC) | All Roles | **P0** | **MVP** | FT-A01 | FR-003, NFR-010 | Medium |
| **FT-A03** | Password Reset via Secure Email Token | All Roles | **P1** | **MVP** | FT-A01 | FR-004 | Low |
| **FT-A04** | Department & Job Role Hierarchy Admin | HR, Admin | **P0** | **MVP** | FT-A02 | FR-005 | Low |
| **FT-A05** | Manual Employee Provisioning | HR, Admin | **P0** | **MVP** | FT-A04 | FR-006 | Low |
| **FT-A06** | Bulk CSV/Excel Employee Roster Import | HR, Admin | **P0** | **MVP** | FT-A04 | FR-007, FR-008, FR-009 | Medium |
| **FT-A07** | Single Sign-On (SAML/Google Workspace) | All Roles | **P3** | **Future** | FT-A01 | — | High |

#### Feature Details (Category A)
- **FT-A06 Acceptance Criteria:**
  - HR uploads `.csv` or `.xlsx` matching the standard template.
  - Backend validates email uniqueness, required columns, and department/role FK existence.
  - Valid rows are committed; invalid rows are recorded in `import_batches.error_log` with specific line numbers and error descriptions.
  - Summary modal displays: Total Rows, Processed Successfully, Failed Count.

---

### Category B: Goal Management

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-B01** | Manager Goal Assignment | Manager | **P0** | **MVP** | FT-A02 | FR-010, FR-014 | Low |
| **FT-B02** | Employee Goal Creation & Submission | Employee | **P0** | **MVP** | FT-A02 | FR-011, FR-012 | Low |
| **FT-B03** | Manager Goal Approval Workflow | Manager | **P0** | **MVP** | FT-B02 | FR-012, FR-013 | Low |
| **FT-B04** | Measurable Milestone Progress Tracking | Employee, Manager | **P0** | **MVP** | FT-B01, FT-B03 | FR-014, FR-015 | Medium |
| **FT-B05** | Review Period Goal Filtering | All Roles | **P1** | **MVP** | FT-B04 | FR-014 | Low |
| **FT-B06** | Cascading Organizational OKRs | HR, Exec | **P3** | **Future** | FT-B01 | — | High |

#### Feature Details (Category B)
- **FT-B03 Acceptance Criteria:**
  - When employee creates a goal, status becomes `PENDING_APPROVAL`.
  - Assigned manager sees badge on dashboard.
  - Manager can Approve (transitions to `ACTIVE`) or Reject (requires rejection comment, transitions to `REJECTED`).
  - Employee receives notification banner with status and feedback.

---

### Category C: Task Management & Context Tracking

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-C01** | Task Creation & Assignment (Manager/Self) | Employee, Manager | **P0** | **MVP** | FT-A02 | FR-016 | Low |
| **FT-C02** | Optional Goal Linking (`goal_id` nullable) | Employee, Manager | **P0** | **MVP** | FT-C01, FT-B04 | FR-016 | Low |
| **FT-C03** | Task Priority & Complexity Tagging | Employee, Manager | **P0** | **MVP** | FT-C01 | FR-016, BR-006 | Low |
| **FT-C04** | Task Lifecycle & Blocked State with Reason | Employee, Manager | **P0** | **MVP** | FT-C01 | FR-017, FR-018 | Medium |
| **FT-C05** | Reopened Task Tracking (`is_reopened`) | Manager | **P1** | **MVP** | FT-C04 | FR-020 | Low |
| **FT-C06** | Kanban-style Interactive Task Board | Employee, Manager | **P2** | **MVP** | FT-C04 | FR-017 | Medium |
| **FT-C07** | Automated Jira/GitHub Task Sync | All Roles | **P3** | **Future** | FT-C01 | — | High |

#### Feature Details (Category C)
- **FT-C04 Acceptance Criteria:**
  - Transitioning task to `BLOCKED` displays a required text field: "Reason for Blocker".
  - System captures blocker timestamp and explanation.
  - Unblocking clears the active blocker and records blocker duration for contextual review.

---

### Category D: Deterministic Scoring & Metric Intelligence

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-D01** | KPI Catalog & Definition Registry | HR | **P0** | **MVP** | FT-A04 | FR-021 | Low |
| **FT-D02** | Role-Specific KPI Configuration Templates | HR | **P0** | **MVP** | FT-D01 | FR-022 | Medium |
| **FT-D03** | Deterministic Raw Metric Calculator | Backend Engine | **P0** | **MVP** | FT-B04, FT-C04 | FR-023 | Medium |
| **FT-D04** | Bounded Metric Normalization Engine | Backend Engine | **P0** | **MVP** | FT-D03 | FR-024 | Low |
| **FT-D05** | Evidence Threshold & Data Coverage Audit | Backend Engine | **P0** | **MVP** | FT-D04 | FR-025, FR-026 | Medium |
| **FT-D06** | Hybrid Weight Redistribution / Insufficient Data | Backend Engine | **P0** | **MVP** | FT-D05 | FR-027, FR-028, BR-007 | Medium |
| **FT-D07** | Score Breakdown & Explanation Inspector | All Roles | **P0** | **MVP** | FT-D06 | FR-027, NFR-014 | Medium |

#### Feature Details (Category D)
- **FT-D06 Acceptance Criteria:**
  - If a KPI lacks minimum evidence counts, it is marked `Not Available`.
  - If total valid evidence coverage $\ge 50\%$, weights are redistributed across available metrics and a composite score is computed.
  - If coverage $< 50\%$, numerical composite score is suppressed, displaying `INSUFFICIENT_DATA` badge with explanation.
  - Under no circumstances is missing data calculated as a zero score.

---

### Category E: Workload Contextualization

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-E01** | Active Task & Complexity Distribution Counter | Backend Engine | **P0** | **MVP** | FT-C03, FT-C04 | FR-029 | Low |
| **FT-E02** | Workload Status Badge (`NORMAL`, `HIGH`, `OVERLOAD`) | All Roles | **P0** | **MVP** | FT-E01 | FR-030, BR-006 | Low |
| **FT-E03** | Team Workload Distribution Heatmap | Manager, HR | **P1** | **MVP** | FT-E02 | FR-051 | Medium |
| **FT-E04** | Workload vs. Completion Correlation Analysis | HR | **P2** | **MVP** | FT-E03, FT-D03 | FR-052 | Medium |

---

### Category F: Qualitative Feedback & Self-Assessment

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-F01** | Monthly Employee Self-Assessment Form | Employee | **P0** | **MVP** | FT-A02 | FR-032 | Low |
| **FT-F02** | Structured Manager-to-Employee Feedback | Manager | **P0** | **MVP** | FT-A02 | FR-033 | Low |
| **FT-F03** | Historical Feedback Thread Viewer | Employee, Manager | **P1** | **MVP** | FT-F01, FT-F02 | FR-034 | Low |
| **FT-F04** | 360-Degree Peer Feedback System | All Roles | **P3** | **Future** | FT-F02 | — | High |

---

### Category G: AI Performance Intelligence & Explanation

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-G01** | Context Bundle Assembly & PII Pseudonymization | Backend Engine | **P0** | **MVP** | FT-D06, FT-F02 | FR-035, FR-036 | Medium |
| **FT-G02** | Structured LLM Narrative Generation (Schema Validated) | Backend Engine | **P0** | **MVP** | FT-G01 | FR-037, FR-038 | High |
| **FT-G03** | Evidence Reference & Hallucination Verifier | Backend Engine | **P0** | **MVP** | FT-G02 | FR-039 | Medium |
| **FT-G04** | Strengths & Improvement Area Extractor | Employee, Manager | **P0** | **MVP** | FT-G02 | FR-037 | Medium |
| **FT-G05** | Skill & Training Resource Recommendations | Employee, Manager | **P1** | **MVP** | FT-G04 | FR-037 | Medium |
| **FT-G06** | User Flagging of Inaccurate Insights | Employee, Manager | **P1** | **MVP** | FT-G02 | FR-040 | Low |
| **FT-G07** | Regenerate Insights (Non-destructive) | Manager | **P2** | **MVP** | FT-G02 | FR-040 | Medium |

#### Feature Details (Category G)
- **FT-G03 Acceptance Criteria:**
  - AI outputs must reference valid metric keys (e.g., `METRIC_TASK_COMPLETION`).
  - Backend verifies that all keys cited in `evidence_references` exist in the supplied context.
  - If ungrounded assertions are detected, the backend marks the insight `PARTIALLY_GROUNDED` and appends a verification disclaimer.

---

### Category H: Performance Review & Historical Snapshots

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-H01** | Monthly Review Period Orchestration | HR | **P0** | **MVP** | FT-A04 | FR-041 | Low |
| **FT-H02** | Draft Review Compilation & Score Preview | Manager | **P0** | **MVP** | FT-D06, FT-G02 | FR-042 | Medium |
| **FT-H03** | Manager Review Finalization & Remarks | Manager | **P0** | **MVP** | FT-H02 | FR-043 | Low |
| **FT-H04** | Immutable Review Snapshot Storage (`review_metric_snapshots`) | Backend Engine | **P0** | **MVP** | FT-H03 | FR-044, FR-045, BR-008 | Medium |
| **FT-H05** | Historical Performance Trend Visualizer | Employee, Manager | **P0** | **MVP** | FT-H04 | FR-050, FR-051 | Medium |
| **FT-H06** | Official Review PDF / CSV Export | Manager, HR | **P1** | **MVP** | FT-H04 | FR-044 | Low |

---

### Category I: Collaborative Development Planning

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-I01** | AI-Assisted Development Plan Drafting | Manager | **P0** | **MVP** | FT-G05 | FR-046 | Medium |
| **FT-I02** | Bilateral Review & Mutual Digital Agreement | Employee, Manager | **P0** | **MVP** | FT-I01 | FR-047, FR-048, BR-010 | Medium |
| **FT-I03** | Action Item Milestone Tracking | Employee, Manager | **P0** | **MVP** | FT-I02 | FR-049 | Low |
| **FT-I04** | Development Plan Completion Review | Manager | **P1** | **MVP** | FT-I03 | FR-049 | Low |

---

### Category J: Dashboards & Governance Reporting

| Feature ID | Feature Name | Target Role | Priority | Scope | Dependencies | Related SRS IDs | Est. Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FT-J01** | Employee Personal Performance & Growth Portal | Employee | **P0** | **MVP** | FT-D07, FT-I03 | FR-050 | Medium |
| **FT-J02** | Manager Team Performance & Coaching Hub | Manager | **P0** | **MVP** | FT-E03, FT-H02 | FR-051 | Medium |
| **FT-J03** | HR Organization Health & Compliance Dashboard | HR | **P0** | **MVP** | FT-D06, FT-H04 | FR-052 | Medium |
| **FT-J04** | System Audit Log Inspector | Admin | **P1** | **MVP** | FT-A02 | NFR-013 | Low |
| **FT-J05** | Advanced Cross-Department Statistical Bias Audits | HR | **P3** | **Future** | FT-J03 | — | High |

---
*End of Feature Catalog.*
