from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
import jwt
from app.config import SECRET_KEY
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal, engine
from app.models.pydantic.pydantic_office import Office, OfficeCreate
from app.models.sqlalchemy.sql_office import Office as DBOffice
from app.queries.office_queries import (
    get_offices,
    get_office,
    create_office,
    update_office,
    delete_office,
)
from app.auth.auth_queries import validate_token
from app.db.database import get_db


router = APIRouter()
security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/verefy-code")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/protected-route")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    token = validate_token(token, "access")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": f"Hello, {user}, you have access!"}


@router.get("/", response_model=List[Office])
def read_offices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    offices = get_offices(db, skip=skip, limit=limit)
    return offices


@router.get("/{office_id}", response_model=Office)
def read_office(db: Session = Depends(get_db), office_id: int = None):
    office = get_office(db, office_id)
    if office is None:
        raise HTTPException(status_code=404, detail="Office not found")
    return office


@router.post("/", response_model=Office)
def add_office(office: OfficeCreate, db: Session = Depends(get_db)):
    db_office = create_office(db, office)
    return db_office


@router.put("/{office_id}", response_model=Office)
def change_office(office_id: int, office: OfficeCreate, db: Session = Depends(get_db)):
    db_office = update_office(db, office_id, office)
    if db_office is None:
        raise HTTPException(status_code=404, detail="Office not found")
    return db_office


@router.delete("/{office_id}", response_model=Office)
def remove_office(office_id: int, db: Session = Depends(get_db)):
    db_office = delete_office(db, office_id)
    if db_office is None:
        raise HTTPException(status_code=404, detail="Office not found")
    return db_office
