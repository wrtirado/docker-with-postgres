from app.database import SessionLocal
from app.queries import locations_queries
from app.models.pydantic import locations_models

db = SessionLocal()

sample_items = ["Refrigerator", "Freezer", "Pantry", "Bread Basket"]

for item in sample_items:
    locations_queries.create_location(db, locations_models.LocationCreate(name=item))

db.close()
