from pydantic import BaseModel, ConfigDict
from uuid import UUID


class BaseCompany(BaseModel):
    name: str


class CompanyCreate(BaseCompany):
    pass


class CompanyRead(BaseCompany):
    id: UUID
    created_at: str

    model_config = ConfigDict(
        from_attributes=True
    )  # Tells Pydantic to treat the SQLAlchemy model as dict
