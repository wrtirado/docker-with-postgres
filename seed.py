from app.db.database import SessionLocal
from app.queries import locations_queries
from app.models.pydantic import pydantic_locations

db = SessionLocal()

sample_items = ["Refrigerator", "Freezer", "Pantry", "Bread Basket"]

for item in sample_items:
    locations_queries.create_location(db, pydantic_locations.LocationCreate(name=item))

db.close()
