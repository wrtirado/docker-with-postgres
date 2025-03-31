# imports for generate_auth_code function
import random
import redis
from datetime import timedelta

# imports for database interaction
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

# imports for auth code verification and JWT generation/send
import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY

# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


def generate_auth_code(email: str) -> str:
    # Generate a random 6-digit number
    auth_code = str(random.randint(100000, 999999))
    # Store the auth code in Redis with a 5-minute expiration
    redis_client.setex(f"auth_code:{email}", timedelta(minutes=5), auth_code)
    return auth_code


def verify_auth_code(email: str, auth_code: str):
    # Retrieve the auth code from Redis
    stored_auth_code = redis_client.get(f"auth_code:{email}")

    # raise an error if the auth code is not found or is expired
    if not stored_auth_code or stored_auth_code != auth_code:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    # Delete the auth code from Redis
    redis_client.delete(f"auth_code:{email}")

    # Generate access token (short-lived)
    access_payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=10),
        "token_type": "access",
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")

    # Generate refresh token (longer-lived)
    refresh_payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(days=30),
        "token_type": "refresh",
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")

    # Store the refresh token in Redis (optional, for invalidation)
    redis_client.setex(f"refresh_token:{email}", timedelta(days=30), refresh_token)

    # Return the tokens
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def verify_refresh_token(refresh_token: str):
    # Decode the refresh token
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        email = payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Check if the refresh token is stored in Redis
    stored_refresh_token = redis_client.get(f"refresh_token:{email}")
    if not stored_refresh_token or stored_refresh_token != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    # Generate a new access token
    access_payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=10),
        "token_type": "access",
    }
    new_access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": new_access_token, "token_type": "bearer"}


def delete_refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        email = payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Check if the refresh token is stored in Redis
    stored_refresh_token = redis_client.get(f"refresh_token:{email}")
    if not stored_refresh_token or stored_refresh_token != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    # Delete the refresh token from Redis
    # This will invalidate the refresh token
    # and prevent further access to the application
    # using this refresh token
    redis_client.delete(f"refresh_token:{email}")
    return {"message": "Refresh token deleted successfully"}


def validate_token(authorization: str, expected_token_type: str):
    # Check if there is an Authorization header
    # and if the Authorization header starts with "Bearer "
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Check if the token is an access token
        if payload.get("token_type") != expected_token_type:
            raise HTTPException(status_code=401, detail="Invalid token type")
        return token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
