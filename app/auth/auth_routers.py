from fastapi import APIRouter, Depends, HTTPException, status
from app.services.email_service import send_email
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.auth.queries import generate_auth_code, create_user
from app.models.sqlalchemy.sql_users import User
from app.models.pydantic.pydantic_users import UserCreate
from app.models.pydantic.pydantic_users import User as UserPydantic

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/request-code")
def request_code(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if user:
        auth_code = generate_auth_code(email)
        send_email(email, auth_code)

    return {
        "message": "If your email is registered, you will receive an authentication code."
    }


@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_data)
    return user
