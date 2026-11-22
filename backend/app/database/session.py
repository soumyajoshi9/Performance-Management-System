from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from typing import Generator

db_url = settings.effective_database_url
engine_args = {}
if db_url.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}
else:
    # Production-ready PostgreSQL / Supabase pooler configuration
    engine_args["pool_pre_ping"] = True      # Automatically detects disconnected sockets
    engine_args["pool_recycle"] = 300       # Recycles connections every 5 minutes to prevent stale pooler disconnects
    engine_args["pool_size"] = 10           # Base connection pool size
    engine_args["max_overflow"] = 20        # Burst capacity for high concurrency

engine = create_engine(db_url, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for yielding database sessions with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
