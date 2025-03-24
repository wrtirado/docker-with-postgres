# imports for database interaction
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.pydantic import pydantic_users
from app.models.sqlalchemy import sql_users


def create_user(db: Session, user: pydantic_users.UserCreate):
    # Check if user already exists
    existing_user = (
        db.query(sql_users.User).filter(sql_users.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create the user
    new_user = sql_users.User(email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
