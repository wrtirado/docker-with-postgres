from fastapi import FastAPI
from app.database import engine, Base
from app.models.sqlalchemy.locations_alchemy import Location
from app.routers import locations

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(locations.router, prefix="/locations")
