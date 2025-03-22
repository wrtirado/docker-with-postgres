from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal, engine
from app.models.pydantic.pydantic_locations import Location, LocationCreate
from app.models.sqlalchemy.sql_locations import Location as DBLocation
from app.queries.locations_queries import (
    get_locations,
    get_location,
    create_location,
    update_location,
    delete_location,
)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[Location])
def read_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    locations = get_locations(db, skip=skip, limit=limit)
    return locations


@router.get("/{location_id}", response_model=Location)
def read_location(db: Session = Depends(get_db), location_id: int = None):
    location = get_location(db, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/", response_model=Location)
def add_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = create_location(db, location)
    return db_location
