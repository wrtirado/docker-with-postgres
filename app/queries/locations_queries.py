from sqlalchemy.orm import Session
from app.models.pydantic import locations_models
from app.models.sqlalchemy import locations_alchemy


def get_locations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(locations_alchemy.Location).offset(skip).limit(limit).all()


def create_location(db: Session, location: locations_models.LocationCreate):
    db_location = locations_alchemy.Location(name=location.name)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location(
    db: Session, location_id: int, location: locations_models.LocationCreate
):
    db_location = (
        db.query(locations_alchemy.Location)
        .filter(locations_alchemy.Location.id == location_id)
        .first()
    )
    if db_location:
        db_location.name = location.name
        db.commit()
        db.refresh(db_location)
    return db_location


def delete_location(db: Session, location_id: int):
    db_location = (
        db.query(locations_alchemy.Location)
        .filter(locations_alchemy.Location.id == location_id)
        .first()
    )
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location
