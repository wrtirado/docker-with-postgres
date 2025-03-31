from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.email_service import send_email
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.auth.auth_queries import (
    generate_auth_code,
    verify_auth_code,
    verify_refresh_token,
    delete_refresh_token,
    validate_token,
)
from app.auth.auth_pydantic_models import (
    RequestCodeRequest,
    VerifyCodeRequest,
)
from app.models.sqlalchemy.sql_users import User
from app.models.pydantic.pydantic_users import UserCreate
from app.models.pydantic.pydantic_users import User as UserPydantic

router = APIRouter()
security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# The /auth/request-code endpoint will take an email address
# as input and generate an authentication code if the email
# address is registered in the database.
@router.post("/request-code")
def request_code(request: RequestCodeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if user:
        auth_code = generate_auth_code(request.email)
        print(f"Generated auth code: {auth_code}")
        print(
            "Update app/auth/auth_routers -> request_code to restart email send functionality"
        )
        # uncomment the line below to actually send the email
        # send_email(email, auth_code)

    return {
        "message": "If your email is registered, you will receive an authentication code."
    }


# The /auth/verify-code endpoint will take an email address
# and an authentication code as input and verify that the
# authentication code is correct. If the code is correct, a
# JWT token will be returned.
@router.post("/verify-code")
def verify_code(request: VerifyCodeRequest):
    return verify_auth_code(request.email, request.auth_code)


# The /auth/refresh-token endpoint will take a refresh token
# as input and return a new access token if the refresh token
# is valid. This endpoint is useful for refreshing the access
# token without requiring the user to log in again.
@router.post("/refresh-token")
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    authorization = credentials.credentials
    # Validate the token and ensure it's a refresh_token
    token = validate_token(authorization, "refresh")

    # Verify the refresh token and generate a new access token
    return verify_refresh_token(token)


# The /auth/logout endpoint will take a refresh token
# as input and invalidate the refresh token. This endpoint
# is useful for logging out the user and preventing further
# access to the application using the refresh token.
@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Validate the token and ensure it's a refresh token
    authorization = credentials.credentials
    # Validate the token and ensure its a refresh_token
    refresh_token = validate_token(authorization, "refresh")
    # Invalidate the refresh token by deleting
    # it from the database or cache
    return delete_refresh_token(refresh_token)
