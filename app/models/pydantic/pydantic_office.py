from pydantic import BaseModel, ConfigDict
from uuid import UUID


class BaseOffice(BaseModel):
    name: str
    address: str
    company_id: UUID


class OfficeCreate(BaseOffice):
    pass


class Office(BaseOffice):
    id: UUID
    address: str
    created_at: str
    company_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )  # Tells Pydantic to treat the SQLAlchemy model as dict
