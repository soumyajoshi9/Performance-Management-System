import io
import csv
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.organization import Department, JobRole
from app.models.user import User
from app.models.audit_log import ImportBatch
from app.schemas.organization import (
    DepartmentCreate, DepartmentRead, JobRoleCreate, JobRoleRead,
    EmployeeCreate, EmployeeRead, BatchImportResponse, ImportRowError
)
from app.core.security import hash_password
from app.core.exceptions import EntityNotFoundError, ConflictError, ValidationError

class OrganizationService:
    @staticmethod
    def create_department(db: Session, data: DepartmentCreate) -> Department:
        existing = db.query(Department).filter(
            (Department.name == data.name) | (Department.code == data.code)
        ).first()
        if existing:
            raise ConflictError(f"Department with name '{data.name}' or code '{data.code}' already exists.")
        dept = Department(**data.model_dump())
        db.add(dept)
        db.commit()
        db.refresh(dept)
        return dept

    @staticmethod
    def get_departments(db: Session) -> List[Department]:
        return db.query(Department).filter(Department.is_active == True).all()

    @staticmethod
    def create_job_role(db: Session, data: JobRoleCreate) -> JobRole:
        dept = db.query(Department).filter_by(id=data.department_id, is_active=True).first()
        if not dept:
            raise EntityNotFoundError("Department", data.department_id)
        existing = db.query(JobRole).filter_by(code=data.code).first()
        if existing:
            raise ConflictError(f"Job role with code '{data.code}' already exists.")
        role = JobRole(**data.model_dump())
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    @staticmethod
    def get_job_roles(db: Session, department_id: str = None) -> List[JobRole]:
        query = db.query(JobRole).filter(JobRole.is_active == True)
        if department_id:
            query = query.filter(JobRole.department_id == department_id)
        return query.all()

    @staticmethod
    def create_employee(db: Session, data: EmployeeCreate) -> User:
        existing = db.query(User).filter_by(email=data.email).first()
        if existing:
            raise ConflictError(f"Employee with email '{data.email}' already exists.")
            
        if data.department_id:
            dept = db.query(Department).filter_by(id=data.department_id, is_active=True).first()
            if not dept:
                raise EntityNotFoundError("Department", data.department_id)
                
        if data.job_role_id:
            role = db.query(JobRole).filter_by(id=data.job_role_id, is_active=True).first()
            if not role:
                raise EntityNotFoundError("JobRole", data.job_role_id)
                
        if data.manager_id:
            mgr = db.query(User).filter_by(id=data.manager_id, is_active=True).first()
            if not mgr:
                raise EntityNotFoundError("Manager (User)", data.manager_id)

        user = User(
            email=data.email,
            password_hash=hash_password(data.password or "DefaultPass123!"),
            full_name=data.full_name,
            role=data.role,
            department_id=data.department_id,
            job_role_id=data.job_role_id,
            manager_id=data.manager_id,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def import_employees_csv(db: Session, file_content: bytes, file_name: str, imported_by_id: str) -> BatchImportResponse:
        """Parses CSV, validates row-by-row, commits valid records, logs errors."""
        decoded = file_content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(decoded))
        
        required_headers = {"email", "full_name", "role", "department_code"}
        if not required_headers.issubset(set(reader.fieldnames or [])):
            raise ValidationError(f"CSV missing mandatory headers: {required_headers - set(reader.fieldnames or [])}")
        
        successful_count = 0
        errors: List[ImportRowError] = []
        
        # Cache departments and roles for fast in-memory lookup
        departments = {d.code.upper(): d.id for d in db.query(Department).filter_by(is_active=True).all()}
        job_roles = {r.code.upper(): r.id for r in db.query(JobRole).filter_by(is_active=True).all()}
        users_by_email = {u.email.lower(): u.id for u in db.query(User).filter_by(is_active=True).all()}
        
        row_num = 1
        for row in reader:
            row_num += 1
            email = (row.get("email") or "").strip().lower()
            full_name = (row.get("full_name") or "").strip()
            role = (row.get("role") or "EMPLOYEE").strip().upper()
            dept_code = (row.get("department_code") or "").strip().upper()
            job_role_code = (row.get("job_role_code") or "").strip().upper()
            mgr_email = (row.get("manager_email") or "").strip().lower()
            
            if not email or "@" not in email:
                errors.append(ImportRowError(row_number=row_num, email=email, error="Invalid email address."))
                continue
                
            if email in users_by_email:
                errors.append(ImportRowError(row_number=row_num, email=email, error=f"Email '{email}' already registered."))
                continue
                
            if role not in ("EMPLOYEE", "MANAGER", "HR", "ADMIN"):
                errors.append(ImportRowError(row_number=row_num, email=email, error=f"Invalid role '{role}'."))
                continue
                
            dept_id = departments.get(dept_code)
            if not dept_id:
                errors.append(ImportRowError(row_number=row_num, email=email, error=f"Department code '{dept_code}' not found."))
                continue
                
            job_role_id = job_roles.get(job_role_code) if job_role_code else None
            mgr_id = users_by_email.get(mgr_email) if mgr_email else None
            
            # Create user
            new_user = User(
                email=email,
                password_hash=hash_password("WelcomeVYORA123!"),
                full_name=full_name,
                role=role,
                department_id=dept_id,
                job_role_id=job_role_id,
                manager_id=mgr_id,
                is_active=True
            )
            db.add(new_user)
            db.flush()
            users_by_email[email] = new_user.id
            successful_count += 1
            
        # Log batch run
        batch = ImportBatch(
            imported_by_id=imported_by_id,
            entity_type="EMPLOYEE",
            file_name=file_name,
            total_rows=row_num - 1,
            successful_rows=successful_count,
            failed_rows=len(errors),
            error_log=[e.model_dump() for e in errors]
        )
        db.add(batch)
        db.commit()
        db.refresh(batch)
        
        return BatchImportResponse(
            batch_id=batch.id,
            file_name=file_name,
            total_rows=batch.total_rows,
            successful_rows=batch.successful_rows,
            failed_rows=batch.failed_rows,
            errors=errors
        )
