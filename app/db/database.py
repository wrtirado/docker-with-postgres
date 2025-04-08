from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.models.sqlalchemy import sql_users, sql_office
from app.db.base import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://myuser:mypassword@db:5432/mydatabase"
)
TESTING = os.getenv("TESTING", "False").lower() == "true"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    if TESTING:
        # During testing, yield a MagicMock instead of a real DB session
        from unittest.mock import MagicMock

        print("✅ TESTING ACTIVE: Yielding mock DB session")
        db = MagicMock()
        yield db
    else:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
