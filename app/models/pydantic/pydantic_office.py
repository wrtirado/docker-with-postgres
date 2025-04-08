from pydantic import BaseModel, ConfigDict


class BaseOffice(BaseModel):
    business_name: str


class OfficeCreate(BaseOffice):
    pass


class Office(BaseOffice):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )  # Tells Pydantic to treat the SQLAlchemy model as dict
