# VYORA — Comprehensive Development Setup Guide
**Smart Performance Management & Employee Development Intelligence Platform**

---

## 1. Development Environment Architecture

VYORA is structured as a **Modular Monolith**:
- **Backend:** Python 3.11+ / FastAPI / SQLAlchemy 2.0 / Alembic.
- **Frontend:** Next.js 14+ / React 18+ / TypeScript / Tailwind CSS / shadcn/ui.
- **Persistence:** PostgreSQL 15+ (with native SQLite support for rapid local development without a database daemon).
- **AI Integration:** Google Gemini API (via isolated backend proxy).

---

## 2. Prerequisites & Verification

Before setting up the project, ensure your environment meets the minimum toolchain requirements:

```powershell
# 1. Check Python version (>= 3.11 required)
python --version

# 2. Check Node.js version (>= 18.18 or >= 20.0 required)
node --version

# 3. Check npm version (>= 10.0 required)
npm --version

# 4. Check Git version (>= 2.40 required)
git --version
```

---

## 3. Repository Configuration & Environment Variables

### 3.1 Initialize Environment Settings
In the repository root, copy the environment template:
```powershell
Copy-Item .env.example .env
```

### 3.2 Key Configuration Parameters
Edit `.env` to configure your local preferences:
- `DATABASE_URL`: 
  - For PostgreSQL: `postgresql://postgres:postgres@localhost:5432/vyora_db`
  - For SQLite local development: `sqlite:///./vyora.db`
- `JWT_SECRET_KEY`: High-entropy secret key for cryptographic JWT signing.
- `GEMINI_API_KEY`: API key for Google Gemini (optional in offline test mode).

---

## 4. Backend Setup & Database Initialization

### 4.1 Install Dependencies
From the repository root:
```powershell
cd backend
python -m pip install -r requirements.txt
```

### 4.2 Initialize Database & Seed Demo Data
Run the built-in database initializer to create all tables and populate initial demo departments, job roles, role KPIs, and test accounts:
```powershell
python -m app.database.init_db
```

### 4.3 Start FastAPI Development Server
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Interactive ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Health Endpoint: [http://127.0.0.1:8000/api/v1/audit/health](http://127.0.0.1:8000/api/v1/audit/health)

---

## 5. Frontend Setup & Startup

### 5.1 Install Node Dependencies
In a separate terminal window:
```powershell
cd frontend
npm install
```

### 5.2 Start Next.js Development Server
```powershell
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your web browser.

---

## 6. Seed Demo Accounts & Credentials

The initialization script provisions 4 default accounts representing each supported system role:

| Role | Email | Password | Primary Capabilities |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin@vyora.local` | `AdminPass123!` | System configuration, health & audit logs |
| **HR Specialist** | `hr@vyora.local` | `HrPass123!` | Company directory, role KPI configs & org analytics |
| **Manager / Team Lead** | `manager@vyora.local` | `ManagerPass123!` | Team roster, goal approvals & review finalization |
| **Employee (Senior Dev)**| `employee@vyora.local`| `EmployeePass123!`| Personal goals, tasks, self-assessments & growth plans |

---

## 7. Running Automated Test Suites

### Backend Tests (Pytest)
```powershell
cd backend
pytest -v
```
Validates:
- Deterministic scoring algorithms and bounded linear normalization.
- Hybrid missing data policy and data coverage auditing.
- RBAC permission guards and tenant scoping.
- PII anonymization and structured AI output validation.

---

## 8. Troubleshooting Common Issues

1. **`ModuleNotFoundError: No module named 'app'`**
   - Ensure you are in the `backend/` directory when running Python commands, or set `PYTHONPATH=.`.
2. **`EPERM: operation not permitted` on Windows**
   - Rerun the command or run PowerShell with standard user permissions.
3. **Database connection failure**
   - Verify `DATABASE_URL` in `.env`. SQLite (`sqlite:///./vyora.db`) requires zero external daemons.
