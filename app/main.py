from fastapi import FastAPI
from app.db.database import engine
from app.models.sqlalchemy.sql_office import Office
from app.routers import company_routers, office_routers, users_routers
from app.auth import auth_routers

# Initialize DB tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(company_routers.router, prefix="/companies", tags=["companies"])
app.include_router(office_routers.router, prefix="/offices", tags=["offices"])
app.include_router(auth_routers.router, prefix="/auth", tags=["authentication"])
app.include_router(users_routers.router, prefix="/users", tags=["users"])
