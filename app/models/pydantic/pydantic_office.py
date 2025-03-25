from pydantic import BaseModel


class BaseOffice(BaseModel):
    business_name: str


class OfficeCreate(BaseOffice):
    pass


class Office(BaseOffice):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as dict
