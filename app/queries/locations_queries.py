from sqlalchemy.orm import Session
from app.models.pydantic import pydantic_locations
from app.models.sqlalchemy import sql_locations


def get_locations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(sql_locations.Location).offset(skip).limit(limit).all()


def create_location(db: Session, location: pydantic_locations.LocationCreate):
    db_location = sql_locations.Location(name=location.name)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location(
    db: Session, location_id: int, location: pydantic_locations.LocationCreate
):
    db_location = (
        db.query(sql_locations.Location)
        .filter(sql_locations.Location.id == location_id)
        .first()
    )
    if db_location:
        db_location.name = location.name
        db.commit()
        db.refresh(db_location)
    return db_location


def delete_location(db: Session, location_id: int):
    db_location = (
        db.query(sql_locations.Location)
        .filter(sql_locations.Location.id == location_id)
        .first()
    )
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location
