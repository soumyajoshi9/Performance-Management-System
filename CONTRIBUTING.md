# Contributing to VYORA

Thank you for contributing to VYORA! To maintain high code quality, security, and traceability, please follow these guidelines.

---

## 1. Core Principles
- **No Scope Creep:** Do NOT implement features outside the approved MVP scope (no payroll, attendance, ATS, full LMS, or employee surveillance).
- **Deterministic Authority:** Scoring formulas must be 100% deterministic backend calculations. AI must never calculate scores or make autonomous employment decisions.
- **Bilateral Development Plans:** Growth plans require digital agreement from both Employee and Manager.
- **Immutable Snapshots:** Finalized performance reviews must freeze snapshots in `review_metric_snapshots`.

---

## 2. Git Workflow & Conventions
- Create feature branches from `main`: `feat/feature-name`, `fix/bug-name`, `docs/doc-name`.
- Use **Conventional Commits**:
  - `feat(module): description`
  - `fix(module): description`
  - `docs(module): description`
  - `test(module): description`
  - `refactor(module): description`

---

## 3. Code Standards
- **Python:** Strictly follow PEP 8 and Python 3.11+ type annotations. Use SQLAlchemy 2.0 `select()` syntax.
- **TypeScript:** Enforce `"strict": true`. The use of `any` is strictly prohibited.
- **Tests:** All new logic and API endpoints must include automated tests in `backend/tests/`.
