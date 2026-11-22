# VYORA — Local Development & Setup Guide
**Smart Performance Management & Employee Development Intelligence Platform**

---

## 1. Quick Overview

VYORA is structured as a **Modular Monolith**:
- `backend/`: FastAPI REST API with SQLAlchemy 2.0 and deterministic scoring engine.
- `frontend/`: Next.js 14+ SPA with TypeScript, Tailwind CSS, and shadcn/ui.
- `docs/`: Comprehensive project documentation.

---

## 2. Prerequisites Check

Verify your local environment has the required runtimes installed:
```powershell
python --version    # Expected: Python 3.11+
node --version      # Expected: v18+ or v20+ or v22+
npm --version       # Expected: 10+
git --version       # Expected: 2.40+
```

---

## 3. Step-by-Step Installation

### Step 1: Clone Repository & Setup Environment File
```powershell
# In the project root:
Copy-Item .env.example .env
```
Open `.env` and verify settings. For local testing without a running PostgreSQL instance, SQLite is supported out of the box by setting:
```env
DATABASE_URL=sqlite:///./vyora.db
```

### Step 2: Backend Setup & Dependency Installation
```powershell
# Navigate to backend directory:
cd backend

# (Optional but recommended) Create virtual environment:
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required dependencies:
pip install -r requirements.txt
```

### Step 3: Run Database Migrations & Seed Demo Data
```powershell
# Apply database migrations via Alembic:
alembic upgrade head

# Or run the built-in database initializer and seeder:
python -m app.database.init_db
```

### Step 4: Start the Backend API Server
```powershell
# From the backend directory:
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive OpenAPI documentation will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- API Health Endpoint: [http://127.0.0.1:8000/api/v1/audit/health](http://127.0.0.1:8000/api/v1/audit/health)

---

## 4. Frontend Setup & Startup

### Step 1: Install Dependencies
Open a second terminal window:
```powershell
cd frontend
npm install
```

### Step 2: Start Frontend Development Server
```powershell
npm run dev
```
Access the application at: [http://localhost:3000](http://localhost:3000)

---

## 5. Seed Demo Accounts & Roles

The initialization script seeds 4 standard test accounts corresponding to all 4 system roles:

| Role | Email | Password | Scope |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin@vyora.local` | `AdminPass123!` | System configuration & audit logs |
| **HR Specialist** | `hr@vyora.local` | `HrPass123!` | Org-wide analytics, roster & KPI configs |
| **Manager / Team Lead** | `manager@vyora.local` | `ManagerPass123!` | Engineering team management & reviews |
| **Employee (Senior Dev)**| `employee@vyora.local`| `EmployeePass123!`| Personal goals, tasks, reviews & growth |

---

## 6. Running Test Suites

### Backend Unit & Integration Tests
```powershell
# From the backend directory:
pytest
```
- Includes tests for deterministic scoring, bounded normalization, hybrid missing data handling, and RBAC authentication guards.

---

## 7. Troubleshooting

- **Database Connection Error:** Verify your `DATABASE_URL` in `.env`. If PostgreSQL is not running locally, use `sqlite:///./vyora.db` for development.
- **Port In Use (8000 or 3000):** Kill the lingering process or specify an alternative port via `--port 8001` or `npm run dev -- -p 3001`.
- **CORS Errors:** Ensure `ALLOWED_ORIGINS` in `.env` includes `http://localhost:3000`.
