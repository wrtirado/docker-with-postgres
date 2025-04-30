import uuid
from sqlalchemy.orm import Session
from app.models.sqlalchemy.sql_company import Company
from app.models.pydantic.pydantic_company import CompanyCreate
from datetime import datetime, timezone


def create_company(db: Session, company_in: CompanyCreate) -> Company:
    """
    Create a new company in the database.

    Args:
        db (Session): The database session.
        company_in (CompanyCreate): The company data to create.

    Returns:
        Company: The created company.
    """
    company = Company(
        id=str(uuid.uuid4()),  # Generate a UUID for the id
        name=company_in.name,  # Assuming name is a string in CompanyCreate
        created_at=datetime.now(
            timezone.utc
        ).isoformat(),  # Convert datetime to ISO 8601 string
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def get_company_by_id(db: Session, company_id: str) -> Company | None:
    """
    Get a company by its ID.

    Args:
        db (Session): The database session.
        company_id (int): The ID of the company to retrieve.

    Returns:
        Company | None: The company if found, otherwise None.
    """
    return db.query(Company).filter(Company.id == company_id).first()
