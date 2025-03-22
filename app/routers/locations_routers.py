from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal, engine
from app.models.pydantic.pydantic_locations import Location
from app.models.sqlalchemy.sql_locations import Location as DBLocation
from app.queries.locations_queries import get_locations


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


@router.get("/{location_id}")
def read_location(location_id: int):
    return {"message": f"Storage location {location_id} is working!"}
