# imports forgenerate_auth_code function
import random
import redis
from datetime import timedelta

# imports for database interaction
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.pydantic import pydantic_users
from app.models.sqlalchemy import sql_users

# imports for auth code verification and JWT generation/send
import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY

# Function to generate an auth code and store it in Redis
# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


def generate_auth_code(email: str) -> str:
    # Generate a random 6-digit number
    auth_code = str(random.randint(100000, 999999))
    # Store the auth code in Redis with a 5-minute expiration
    redis_client.setex(f"auth_code:{email}", timedelta(minutes=5), auth_code)
    return auth_code


def verify_auth_code(email: str, auth_code: str) -> bool:
    # Retrieve the auth code from Redis
    stored_auth_code = redis_client.get(f"auth_code:{email}")

    # raise an error if the auth code is not found or is expired
    if not stored_auth_code or stored_auth_code != auth_code:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    # Delete the auth code from Redis
    redis_client.delete(f"auth_code:{email}")

    # generate a JWT token
    payload = {"sub": email, "exp": datetime.utcnow() + timedelta(minutes=10)}
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": jwt_token, "token_type": "bearer"}


# Route Specific Queries
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
