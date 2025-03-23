from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str | None = None
    is_active: bool = True


class UserCreate(BaseUser):
    pass


class User(BaseUser):
    id: int
    email: str | None = None
    is_active: bool

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as dict
