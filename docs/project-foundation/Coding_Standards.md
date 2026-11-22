# VYORA — Engineering & Coding Standards
**Smart Performance Management & Employee Development Intelligence Platform**

---

## 1. General Principles
VYORA maintains rigorous engineering standards to ensure the codebase remains maintainable, secure, testable, and lean:
1. **KISS & YAGNI Over Cleverness:** Prefer simple, readable, testable code over intricate meta-programming or premature abstractions.
2. **Explicit Over Implicit:** Avoid implicit side effects, magic numbers, or hidden monkey-patching.
3. **Strict Separation of Concerns:**
   - Routers only parse requests, validate DTOs, and delegate to services.
   - Services execute business rules and orchestrate persistence.
   - Repositories/Models handle database interactions.
   - Analytics modules contain pure deterministic calculation logic without network or database dependencies.
4. **Single Source of Truth:** Schema and type contracts must remain synchronized across backend (Pydantic/SQLAlchemy) and frontend (TypeScript/Zod).

---

## 2. Python Coding Standards (Backend)

### 2.1 Style & Formatting
- **Standard:** Strict conformance with **PEP 8**.
- **Formatter & Linter:** **Ruff** (or Black + Flake8 + isort). 
  - Max line length: 100 characters.
  - Double quotes for strings (`"hello"`).
- **Imports Sorting:** Standard library first, third-party libraries second, internal application modules last. Enforced via isort/Ruff.

### 2.2 Type Annotations
- **Strict Typing:** All function signatures (arguments and return values) must be explicitly typed using standard Python 3.10+ syntax:
  ```python
  # Good
  def calculate_data_coverage(
      metrics: list[MetricResult], 
      min_threshold: int = 3
  ) -> tuple[float, bool]:
      ...
  
  # Prohibited
  def calculate_data_coverage(metrics, min_threshold=3):
      ...
  ```
- Use `typing.Optional` (or `T | None`), `typing.Literal`, and custom Pydantic models for structured types.

### 2.3 Exception Handling
- **No Bare Excepts:** Catching bare `except:` or `except Exception:` without logging and re-raising is strictly forbidden.
- **Domain Exceptions:** Raise domain-specific exceptions extending from `VyoraBaseException` located in `backend/app/core/exceptions.py`:
  ```python
  class EntityNotFoundError(VyoraBaseException):
      """Raised when a requested resource does not exist in persistence."""
      def __init__(self, entity_name: str, entity_id: str):
          super().__init__(f"{entity_name} with ID '{entity_id}' not found.")
          self.code = "ENTITY_NOT_FOUND"
  ```
- **FastAPI Exception Handlers:** Map domain exceptions to standard HTTP error envelopes in `backend/app/main.py`.

### 2.4 SQLAlchemy 2.0 Conventions
- **Declarative Modern Syntax:** Use SQLAlchemy 2.0 `select()` syntax exclusively. Legacy query chaining (`session.query(Model)...`) is prohibited:
  ```python
  # Good (SQLAlchemy 2.0)
  stmt = (
      select(Task)
      .where(Task.employee_id == employee_id)
      .where(Task.status == TaskStatus.COMPLETED)
      .order_by(Task.due_date.desc())
  )
  result = await session.scalars(stmt)
  return result.all()
  ```
- **Explicit Transactions:** Wrap multi-step mutations in explicit database transactions:
  ```python
  async with session.begin():
      await session.execute(update_stmt)
      session.add(snapshot_record)
  ```

### 2.5 Structured Logging
- Use standard Python `logging` or `structlog` outputting machine-readable JSON in production.
- Include contextual correlation IDs (`request_id`, `user_id`, `review_period_id`):
  ```python
  logger.info(
      "Review finalized successfully",
      extra={
          "review_id": str(review.id),
          "employee_id": str(review.employee_id),
          "final_score": float(review.final_score),
          "coverage_pct": float(review.data_coverage_percentage),
      }
  )
  ```

---

## 3. TypeScript & React Standards (Frontend)

### 3.1 Strict TypeScript
- **`tsconfig.json`:** `"strict": true` must be enforced across all packages.
- **Prohibition of `any`:** The use of `any` is strictly prohibited in production code. Use `unknown` with explicit type guards or declare comprehensive interfaces.
  ```typescript
  // Prohibited
  const handleData = (data: any) => { ... }

  // Good
  const handleData = (data: ScoreBreakdownResponse): void => { ... }
  ```

### 3.2 Component Architecture (React 18+ / Next.js)
- **Functional Components:** Use functional components exclusively with React Hooks.
- **Explicit Props Contracts:** Define explicit interfaces for every component's props:
  ```typescript
  interface MetricRowProps {
    kpiCode: string;
    kpiName: string;
    rawScore: number | null;
    appliedWeight: number;
    evidenceCount: number;
    status: "AVAILABLE" | "NOT_AVAILABLE" | "INSUFFICIENT";
    onInspectEvidence?: (kpiCode: string) => void;
  }

  export const MetricRow: React.FC<MetricRowProps> = ({
    kpiCode,
    kpiName,
    rawScore,
    appliedWeight,
    evidenceCount,
    status,
    onInspectEvidence,
  }) => {
    ...
  };
  ```
- **Separation of Concerns:** Keep UI components purely presentation-focused. Extract data fetching, mutations, and caching into custom hooks utilizing TanStack Query (`useReview`, `useGoals`, `useTasks`).

### 3.3 State Management & Forms
- **Server State:** Use TanStack Query (React Query) for server caching, background re-validation, and optimistic updates.
- **Form State & Validation:** Use `react-hook-form` paired with **Zod** schema validation contracts matching backend Pydantic schemas.

---

## 4. Testing Standards & Quality Gates

### 4.1 Test Hierarchy
1. **Unit Tests (Backend):**
   - Pure mathematical testing of scoring algorithms, linear normalization formulas, and evidence coverage counters.
   - PII pseudonymization and de-anonymization validation.
   - AI JSON schema validation and retry behaviors.
2. **Integration Tests (Backend API):**
   - Testing FastAPI endpoints against a real PostgreSQL test database (Docker container or temporary test DB).
   - Validation of RBAC permission boundaries (e.g., verifying an Employee receives `403 Forbidden` when attempting to access another employee's review).
   - CSV batch import testing with valid and malformed files.
3. **Component Tests (Frontend):**
   - Jest / React Testing Library verifying that score breakdowns, badges, and warning states render accurately.

### 4.2 Pytest Execution Standards
- Fixtures must be isolated and clean up state after execution.
- External services (Google Gemini API) must be mocked using `pytest-mock` or VCR cassettes. Real network calls during automated test runs are prohibited.
- Minimum test coverage for the deterministic scoring engine: **100% branch coverage**.

---

## 5. Git Conventions & Contribution Workflow

### 5.1 Branch Naming Convention
- `feat/feature-name` (e.g., `feat/scoring-engine-weight-redistribution`)
- `fix/bug-description` (e.g., `fix/csv-import-duplicate-email-handling`)
- `docs/doc-update` (e.g., `docs/update-decision-log-ps-weights`)
- `refactor/scope` (e.g., `refactor/pydantic-v2-schema-migration`)
- `test/test-scope` (e.g., `test/unit-tests-workload-indexer`)

### 5.2 Commit Message Standards (Conventional Commits)
All commit messages must follow the Conventional Commits specification:
```
<type>(<scope>): <short descriptive imperative summary>

[optional body explaining motivation and context]

[optional footer referencing issue/requirement ID]
```
- **Allowed Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
- **Examples:**
  - `feat(scoring): implement bounded linear normalization for task KPIs (FR-024)`
  - `fix(auth): prevent horizontal privilege escalation in team review route (NFR-010)`
  - `docs(erd): generate high-resolution PNG entity relationship diagram`

### 5.3 Code Review Checklist
Before any PR is approved, the reviewer must verify:
- [ ] Requirements traceability: Does the code map to an approved SRS ID?
- [ ] No scope creep: Are any excluded features (payroll, ATS, LMS, chat) introduced?
- [ ] Security audit: Are all queries parameterized? Is RBAC checked?
- [ ] Privacy check: Is any PII leaked to logs or external LLM API payloads?
- [ ] Immutability: Are finalized review records protected against mutation?
- [ ] Test verification: Do all unit and integration tests pass cleanly?

---
*End of Engineering & Coding Standards.*
