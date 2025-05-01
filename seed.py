import uuid
from app.db.database import SessionLocal
from app.queries import company_queries, office_queries
from app.models.pydantic import pydantic_company, pydantic_office
from app.models.sqlalchemy.sql_company import Company
from datetime import datetime, timezone

db = SessionLocal()


# Check if the company already exists
company_name = "Generic Umbrella Company"
existing_company = db.query(Company).filter(Company.name == company_name).first()
company_uuid = None

if existing_company:
    # Use the existing company's ID
    company_uuid = existing_company.id
    print(f"Company '{company_name}' already exists with ID: {company_uuid}")
else:
    # Create the company if it doesn't exist
    company_uuid = str(uuid.uuid4())  # Generate a UUID for the id
    company_queries.create_company(
        db,
        pydantic_company.CompanyCreate(
            id=company_uuid,  # Generate a UUID for the id
            name=company_name,  # Assuming name is a string in CompanyCreate
            created_at=datetime.now(timezone.utc).isoformat(),
        ),
    )
    # Explicitly commit the company to the database
    db.commit()
    print(f"Created new company '{company_name}' with ID: {company_uuid}")

# Explicitly commit the company to the database
db.commit()

sample_offices = [
    "Peakview Sport and Spine",
    "Get Back To Work Occupational Therapists",
    "Dr. HT Physical Therapy",
    "Crunchin' Chiropractic",
]

for office in sample_offices:
    office_queries.create_office(
        db,
        pydantic_office.OfficeCreate(
            id=str(uuid.uuid4()),  # Generate a UUID for the id
            name=office,  # Assuming name is a string in CompanyCreate
            address="123 Address Street",  # Assuming address is a string in OfficeCreate
            company_id=company_uuid,  # Assuming company_id is a string in OfficeCreate
            created_at=datetime.now(timezone.utc).isoformat(),
        ),
    )

# Commit the offices to the database
db.commit()

db.close()
