from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.config import SECRET_KEY
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/verefy-code")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/protected-route")
def protected_route(user: str = Depends(get_current_user)):
    return {"message": f"Hello, {user}, you have access!"}


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


@router.put("/{location_id}", response_model=Location)
def change_location(
    location_id: int, location: LocationCreate, db: Session = Depends(get_db)
):
    db_location = update_location(db, location_id, location)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@router.delete("/{location_id}", response_model=Location)
def remove_location(location_id: int, db: Session = Depends(get_db)):
    db_location = delete_location(db, location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location
