# VYORA — Technical Prerequisites & System Requirements

This document defines all runtime prerequisites, programming language versions, third-party libraries, services, and tooling required to build, test, and run the VYORA platform.

---

## 1. System & Runtime Prerequisites

### Required Runtimes
| Runtime / Tool | Required Version | Status | Purpose |
| :--- | :--- | :--- | :--- |
| **Python** | 3.11+ (Tested on 3.11–3.15) | Mandatory | Core backend services, deterministic scoring, AI orchestration, and tests |
| **Node.js** | 18.18+ or 20+ (Tested on 22+) | Mandatory | Next.js 14 frontend web client runtime |
| **npm / pnpm** | npm 10+ or pnpm 9+ | Mandatory | Frontend package management |
| **PostgreSQL** | 15+ (or SQLite for local dev/testing) | Mandatory | Relational persistence with JSONB and UUID support |
| **Git** | 2.40+ | Mandatory | Source code version control |

### Optional / Recommended Tooling
| Tool | Purpose |
| :--- | :--- |
| **Docker & Docker Compose** | Containerized multi-service development and production deployment |
| **Postman / Insomnia / cURL** | RESTful API endpoint manual testing and exploration |
| **pgAdmin / DBeaver** | Relational database inspection and visual querying |

---

## 2. Backend Dependencies (Python)

Pinned specifications in `backend/requirements.txt`:
```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.8.0
pydantic-settings>=2.4.0
sqlalchemy>=2.0.30
alembic>=1.13.0
psycopg2-binary>=2.9.9
argon2-cffi>=23.1.0
pyjwt>=2.9.0
python-jose[cryptography]>=3.3.0
python-multipart>=0.0.9
httpx>=0.27.0
pytest>=8.2.0
pytest-asyncio>=0.23.0
pandas>=2.2.0
openpyxl>=3.1.0
```

---

## 3. Frontend Dependencies (Node.js / React)

Key specifications in `frontend/package.json`:
- **Core Framework:** Next.js 14+ (App Router), React 18+, TypeScript 5+
- **Styling & UI:** Tailwind CSS 3+, `shadcn/ui` primitives, Lucide React icons
- **State & Data Fetching:** TanStack React Query v5, Axios
- **Form Management:** React Hook Form, Zod
- **Visualizations:** Recharts (accessible responsive charting)

---

## 4. Hardware Requirements

- **Minimum Development Machine:** 2 CPU cores, 4 GB RAM, 2 GB available disk space.
- **Recommended Production Host:** 2 vCPU cores, 4 GB RAM, 20 GB SSD storage (Single-node VM or PaaS).
