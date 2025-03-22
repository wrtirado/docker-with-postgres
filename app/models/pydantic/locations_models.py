from pydantic import BaseModel


class BaseLocation(BaseModel):
    name: str


class LocationCreate(BaseLocation):
    pass


class Location(BaseLocation):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as dict
