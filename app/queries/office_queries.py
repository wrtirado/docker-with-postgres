from sqlalchemy.orm import Session
from app.models.pydantic import pydantic_office
from app.models.sqlalchemy import sql_office


def get_offices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(sql_office.Office).offset(skip).limit(limit).all()


def get_office(db: Session, office_id: int):
    return db.query(sql_office.Office).filter(sql_office.Office.id == office_id).first()


def create_office(db: Session, office: pydantic_office.OfficeCreate):
    db_office = sql_office.Office(business_name=office.business_name)
    db.add(db_office)
    db.commit()
    db.refresh(db_office)
    return db_office


def update_office(db: Session, office_id: int, office: pydantic_office.OfficeCreate):
    db_office = (
        db.query(sql_office.Office).filter(sql_office.Office.id == office_id).first()
    )
    if db_office:
        db_office.business_name = office.business_name
        db.commit()
        db.refresh(db_office)
    return db_office


def delete_office(db: Session, office_id: int):
    db_office = (
        db.query(sql_office.Office).filter(sql_office.Office.id == office_id).first()
    )
    if db_office:
        db.delete(db_office)
        db.commit()
    return db_office
