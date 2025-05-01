import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.pydantic.pydantic_office import OfficeCreate

# from app.models.sqlalchemy import sql_office
from app.models.sqlalchemy.sql_office import Office
from datetime import datetime, timezone


def get_offices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Office).offset(skip).limit(limit).all()


def get_office_by_id(db: Session, office_id: str):
    return db.query(Office).filter(Office.id == office_id).first()


def create_office(db: Session, office_in: OfficeCreate):
    """
    Create a new office.

    Args:
        db (Session): The database session.
        office (OfficeCreate): The office data to create.

    Returns:
        Office: The created office.
    """
    office = Office(
        id=str(uuid.uuid4()),  # Generate a UUID for the id
        name=office_in.name,  # Assuming name is a string in CompanyCreate
        address=office_in.address,  # Assuming address is a string in OfficeCreate
        company_id=office_in.company_id,  # Assuming company_id is a string in OfficeCreate
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    db.add(office)
    db.commit()
    db.refresh(office)
    return office


def update_office(db: Session, office_id: str, office_update: OfficeCreate):
    office = db.query(Office).filter(Office.id == office_id).first()
    # if db_office:
    #     db_office.name = office.name
    #     db.commit()
    #     db.refresh(db_office)
    # return db_office
    if office:
        office.name = office_update.name
        office.address = office_update.address
        office.company_id = office_update.company_id
        db.commit()
        db.refresh(office)
    return office


def delete_office(db: Session, office_id: str):
    db_office = db.query(Office).filter(Office.id == office_id).first()
    if db_office:
        db.delete(db_office)
        db.commit()
        return {"message": "Office deleted successfully"}
    raise HTTPException(status_code=404, detail="Office not found")


# def get_offices(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(sql_office.Office).offset(skip).limit(limit).all()


# def get_office_by_id(db: Session, office_id: int):
#     return db.query(sql_office.Office).filter(sql_office.Office.id == office_id).first()


# def create_office(db: Session, office: pydantic_office.OfficeCreate):
#     """
#     Create a new office.

#     Args:
#         db (Session): The database session.
#         office (pydantic_office.OfficeCreate): The office data to create.

#     Returns:
#         sql_office.Office: The created office.
#     """
#     db_office = sql_office.Office(name=office.name)
#     db.add(db_office)
#     db.commit()
#     db.refresh(db_office)
#     return db_office


# def update_office(db: Session, office_id: int, office: pydantic_office.OfficeCreate):
#     db_office = (
#         db.query(sql_office.Office).filter(sql_office.Office.id == office_id).first()
#     )
#     if db_office:
#         db_office.name = office.name
#         db.commit()
#         db.refresh(db_office)
#     return db_office


# def delete_office(db: Session, office_id: int):
#     db_office = (
#         db.query(sql_office.Office).filter(sql_office.Office.id == office_id).first()
#     )
#     if db_office:
#         db.delete(db_office)
#         db.commit()
#     return db_office
