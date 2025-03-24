from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.queries.users_queries import create_user
from app.models.sqlalchemy.sql_users import User
from app.models.pydantic.pydantic_users import UserCreate
from app.models.pydantic.pydantic_users import User as UserPydantic

router = APIRouter()

# code for protecting routes...
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/verefy-code")

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return payload["sub"]
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")

# @router.get("/protected-route")
# def protected_route(user: str = Depends(get_current_user)):
#     return {"message": f"Hello, {user}, you have access!"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_data)
    return user
