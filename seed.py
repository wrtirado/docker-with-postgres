from app.db.database import SessionLocal
from app.queries import office_queries
from app.models.pydantic import pydantic_office

db = SessionLocal()

sample_offices = [
    "Peakview Sport and Spine",
    "Get Back To Work Occupational Therapists",
    "Dr. HT Physical Therapy",
    "Crunchin' Chiropractic",
]

for office in sample_offices:
    office_queries.create_office(db, pydantic_office.OfficeCreate(business_name=office))

db.close()
