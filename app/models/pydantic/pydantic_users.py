from pydantic import BaseModel, ConfigDict


class BaseUser(BaseModel):
    email: str | None = None
    is_active: bool = True


class UserCreate(BaseUser):
    pass


class User(BaseUser):
    id: int
    email: str | None = None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )  # Tells Pydantic to treat the SQLAlchemy model as dict
