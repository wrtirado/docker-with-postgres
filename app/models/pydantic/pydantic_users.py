from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserCreate(BaseUser):
    pass


class User(BaseUser):
    id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as dict
