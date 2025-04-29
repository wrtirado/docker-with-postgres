from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.queries.company_queries import create_company, get_company_by_id
from app.models.pydantic.pydantic_company import CompanyCreate, CompanyRead

router = APIRouter()


@router.post("/", response_model=CompanyRead)
def create_company_endpoint(company_in: CompanyCreate, db: Session = Depends(get_db)):
    """
    Create a new company.

    Args:
        company_in (CompanyCreate): The company data to create.
        db (Session): The database session.

    Returns:
        CompanyRead: The created company.
    """
    company = create_company(db, company_in)
    return company


@router.get("/{company_id}", response_model=CompanyRead)
def read_company(company_id: str, db: Session = Depends(get_db)):
    """
    Get a company by its ID.

    Args:
        company_id (int): The ID of the company to retrieve.
        db (Session): The database session.

    Returns:
        CompanyRead: The company if found.
    """
    company = get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
