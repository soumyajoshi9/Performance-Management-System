# VYORA — REST API Specification
**Smart Performance Management & Employee Development Intelligence Platform**

---

## 1. API Architecture & Standards

### 1.1 Architectural Style
The VYORA API is engineered as a stateless, resource-oriented RESTful API following OpenAPI 3.1 specifications.
- **Base URL:** `/api/v1`
- **Protocol:** HTTPS / TLS 1.3
- **Data Interchange Format:** JSON (`application/json; charset=utf-8`)
- **Date/Time Standard:** ISO-8601 UTC timestamps (e.g., `2026-11-21T01:30:00Z`).
- **Identifiers:** Standard RFC 4122 Version 4 UUID strings.

### 1.2 Authentication & Authorization
All endpoints (except public `/auth/login` and `/auth/password-reset`) require an HTTP `Authorization` header containing a valid Bearer JWT:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
Role-Based Access Control (RBAC) verifies permissions per route:
- `EMPLOYEE`: Access restricted to self-owned records.
- `MANAGER`: Access to direct reports within assigned team/department.
- `HR`: Access to organization-wide rosters, KPI definitions, and aggregate analytics.
- `ADMIN`: Access to user provisioning, system configurations, and security audit logs.

### 1.3 Standard Response Envelopes

#### Success Envelope
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2026-11-21T01:30:00Z",
    "request_id": "req_8f7b2c9a"
  }
}
```

#### Paginated Success Envelope
```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_records": 142,
    "total_pages": 8
  },
  "meta": {
    "timestamp": "2026-11-21T01:30:00Z",
    "request_id": "req_8f7b2c9a"
  }
}
```

#### Error Envelope
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Task title is required and cannot be blank.",
    "details": [
      {
        "field": "title",
        "issue": "String should have at least 3 characters"
      }
    ]
  },
  "meta": {
    "timestamp": "2026-11-21T01:30:00Z",
    "request_id": "req_8f7b2c9a"
  }
}
```

---

## 2. API Endpoint Catalog

### 2.1 Authentication (`/auth`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/auth/login` | `POST` | Public | Authenticates credentials and returns JWT access & refresh tokens. | FR-001 |
| `/auth/refresh` | `POST` | Public | Exchanges valid refresh token for new access token. | FR-002 |
| `/auth/logout` | `POST` | Authenticated | Revokes current session/refresh token. | FR-002 |
| `/auth/me` | `GET` | Authenticated | Returns profile and role context for authenticated user. | FR-003 |

#### `POST /auth/login`
- **Request Body:**
  ```json
  {
    "email": "sarah.dev@company.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "data": {
      "access_token": "eyJhbGciOi...",
      "token_type": "bearer",
      "expires_in": 3600,
      "user": {
        "id": "c1f7a8e2-4b2e-4b68-9a3b-1d7c3b8e5a10",
        "email": "sarah.dev@company.com",
        "full_name": "Sarah Chen",
        "role": "EMPLOYEE",
        "department_id": "d0a1b2c3-1111-2222-3333-444455556666",
        "job_role_id": "e0a1b2c3-1111-2222-3333-444455556666"
      }
    }
  }
  ```

---

### 2.2 Organizations & Directory (`/organizations`, `/users`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/organizations/departments` | `GET` | All Roles | Lists all active company departments. | FR-005 |
| `/organizations/departments` | `POST` | `HR`, `ADMIN` | Creates a new department. | FR-005 |
| `/organizations/job-roles` | `GET` | All Roles | Lists job roles (filterable by `department_id`). | FR-005 |
| `/organizations/job-roles` | `POST` | `HR`, `ADMIN` | Creates a new job role designation. | FR-005 |
| `/organizations/import/employees` | `POST` | `HR`, `ADMIN` | Multipart file upload (`.csv`/`.xlsx`) for batch onboarding. | FR-007, FR-008 |
| `/users` | `GET` | `MANAGER`, `HR`, `ADMIN` | Lists employees with filtering and pagination. | FR-006 |
| `/users/{id}` | `GET` | Self, `MANAGER`*, `HR` | Fetches detailed employee profile and manager info. | FR-003 |

#### `POST /organizations/import/employees`
- **Request:** `multipart/form-data` with `file: employees.csv`
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "data": {
      "batch_id": "b9a8c7d6-3333-4444-5555-666677778888",
      "total_rows": 50,
      "successful_rows": 48,
      "failed_rows": 2,
      "errors": [
        {"row": 14, "email": "invalid@company", "error": "Invalid email format."},
        {"row": 32, "email": "alex@company.com", "error": "Department code 'MKTG' does not exist."}
      ]
    }
  }
  ```

---

### 2.3 Review Periods (`/review-periods`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/review-periods` | `GET` | All Roles | Lists review periods with status filter. | BR-001 |
| `/review-periods/active` | `GET` | All Roles | Fetches the current active calendar review period. | BR-001 |
| `/review-periods` | `POST` | `HR`, `ADMIN` | Schedules a new monthly review period. | FR-041 |

---

### 2.4 Goals (`/goals`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/goals` | `GET` | All Roles (scoped) | Lists goals (filters: `employee_id`, `review_period_id`, `status`). | FR-014 |
| `/goals` | `POST` | `EMPLOYEE`, `MANAGER` | Creates goal. If created by employee, triggers approval workflow. | FR-010, FR-011 |
| `/goals/{id}` | `GET` | Scoped Access | Retrieves single goal details with milestone history. | FR-014 |
| `/goals/{id}/progress` | `PATCH` | Owner, `MANAGER` | Updates `current_value` progress. | FR-015 |
| `/goals/{id}/approval` | `POST` | `MANAGER` | Approves or rejects an employee-created goal. | FR-013, BR-003 |

#### `POST /goals/{id}/approval`
- **Request Body:**
  ```json
  {
    "action": "REJECT",
    "rejection_reason": "Target metric needs to specify measurable automated test coverage instead of general quality."
  }
  ```

---

### 2.5 Tasks (`/tasks`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/tasks` | `GET` | Scoped Access | Lists operational tasks (filters: `status`, `priority`, `goal_id`, `period`). | FR-016 |
| `/tasks` | `POST` | `EMPLOYEE`, `MANAGER` | Creates task (optional `goal_id`). Tagged with priority & complexity. | FR-016, BR-004 |
| `/tasks/{id}/status` | `PATCH` | Assignee, `MANAGER` | Updates status (`TODO`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`). | FR-017, FR-018 |

#### `PATCH /tasks/{id}/status` (Marking Blocked)
- **Request Body:**
  ```json
  {
    "status": "BLOCKED",
    "blocked_reason": "Waiting on security audit credentials from IT compliance team."
  }
  ```

---

### 2.6 KPI Catalog & Scoring (`/kpis`, `/scoring`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/kpis/definitions` | `GET` | All Roles | Lists active KPI metric catalog. | FR-021 |
| `/kpis/role-configs/{job_role_id}` | `GET` | `HR`, `MANAGER` | Fetches role KPI template, weights, and thresholds. | FR-022 |
| `/kpis/role-configs/{job_role_id}` | `PUT` | `HR` | Updates role KPI template configuration. | FR-022 |
| `/scoring/preview` | `POST` | `MANAGER`, `HR` | Runs deterministic calculation engine for an employee & period. | FR-023, FR-027 |

#### `POST /scoring/preview`
- **Request Body:**
  ```json
  {
    "employee_id": "c1f7a8e2-4b2e-4b68-9a3b-1d7c3b8e5a10",
    "review_period_id": "a5e8c1b2-9999-8888-7777-666655554444"
  }
  ```
- **Response `200 OK` (Sufficient Data Case):**
  ```json
  {
    "success": true,
    "data": {
      "score_status": "CALCULATED",
      "calculated_score": 86.40,
      "data_coverage_percentage": 100.00,
      "workload_context": {
        "active_tasks_count": 8,
        "high_complexity_count": 3,
        "status": "NORMAL"
      },
      "metrics": [
        {
          "kpi_code": "KPI_TASK_COMPLETION",
          "kpi_name": "Task Completion Rate",
          "raw_value": 92.00,
          "normalized_score": 92.00,
          "applied_weight": 25.00,
          "evidence_count": 12,
          "status": "AVAILABLE"
        },
        {
          "kpi_code": "KPI_DEADLINE_ADHERENCE",
          "kpi_name": "On-Time Delivery Rate",
          "raw_value": 85.00,
          "normalized_score": 85.00,
          "applied_weight": 25.00,
          "evidence_count": 12,
          "status": "AVAILABLE"
        }
      ]
    }
  }
  ```

---

### 2.7 Feedback & Reviews (`/feedbacks`, `/reviews`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/feedbacks` | `POST` | `EMPLOYEE`, `MANAGER` | Submits self-assessment or manager feedback for a review period. | FR-032, FR-033 |
| `/feedbacks` | `GET` | Scoped Access | Retrieves feedback for specified employee and period. | FR-034 |
| `/reviews` | `GET` | Scoped Access | Lists formal performance reviews. | FR-041 |
| `/reviews/{id}` | `GET` | Scoped Access | Retrieves review details, score breakdown, and snapshot. | FR-042 |
| `/reviews/{id}/finalize` | `POST` | `MANAGER` | Finalizes review and creates immutable historical snapshot. | FR-043, FR-044 |

#### `POST /reviews/{id}/finalize`
- **Request Body:**
  ```json
  {
    "manager_summary": "Exceptional sprint velocity and proactive technical mentoring across Q4."
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "data": {
      "review_id": "r1a2b3c4-5555-6666-7777-888899990000",
      "status": "FINALIZED",
      "final_score": 86.40,
      "finalized_at": "2026-11-21T01:30:00Z",
      "snapshot_items_created": 4
    }
  }
  ```

---

### 2.8 AI Intelligence (`/ai`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/ai/insights/generate` | `POST` | `MANAGER`, `HR` | Initiates backend AI narrative synthesis for an employee review. | FR-037, FR-038 |
| `/ai/insights/{id}` | `GET` | Scoped Access | Fetches validated structured AI insight. | FR-037 |
| `/ai/insights/{id}/flag` | `POST` | `EMPLOYEE`, `MANAGER` | Flags an insight as inaccurate or biased with mandatory explanation. | FR-040, AI-8 |

#### `POST /ai/insights/{id}/flag`
- **Request Body:**
  ```json
  {
    "flag_reason": "Insight attributes a missed deadline in task #402 to poor planning, but the task was explicitly blocked by external server outage."
  }
  ```

---

### 2.9 Collaborative Development Plans (`/development-plans`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/development-plans` | `GET` | Scoped Access | Lists development plans. | FR-046 |
| `/development-plans` | `POST` | `MANAGER` | Creates proposed development plan (assisted by AI suggestions). | FR-046 |
| `/development-plans/{id}/agreement` | `POST` | `EMPLOYEE`, `MANAGER` | Records digital agreement to activate proposed plan. | FR-047, FR-048 |
| `/development-plans/{id}/action-items/{item_id}` | `PATCH` | Assignee, `MANAGER` | Updates completion state of specific action item milestone. | FR-049 |

---

### 2.10 Governance & Audit (`/audit`)

| Endpoint | Method | Role Access | Description | Related SRS |
| :--- | :--- | :--- | :--- | :--- |
| `/audit/logs` | `GET` | `ADMIN` | Queries immutable security and administrative audit records. | NFR-013 |
| `/audit/health` | `GET` | Public / Monitoring | System health check (PostgreSQL connectivity, API uptime). | NFR-005 |

---
*End of REST API Specification.*
