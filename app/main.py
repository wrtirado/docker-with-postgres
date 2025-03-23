# from typing import Annotated
# from fastapi import FastAPI, Depends
# from fastapi.security import OAuth2PasswordBearer
# from app.models.pydantic.pydantic_users import BaseUser
from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.sqlalchemy.sql_locations import Location
from app.routers import locations_routers

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def fake_decode_token(token):
#     return BaseUser(
#       username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user

# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[BaseUser, Depends(get_current_user)]):
#     return current_user


app.include_router(locations_routers.router, prefix="/locations", tags=["locations"])
