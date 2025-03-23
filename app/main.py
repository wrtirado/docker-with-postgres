from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.sqlalchemy.sql_locations import Location
from app.routers import locations_routers
from app.auth import auth_routers

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(locations_routers.router, prefix="/locations", tags=["locations"])
app.include_router(auth_routers.router, prefix="/auth", tags=["authentication"])
