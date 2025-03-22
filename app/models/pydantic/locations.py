from pydantic import BaseModel


class LocationBase(BaseModel):
    name: str


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as dict
