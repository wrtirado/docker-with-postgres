from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, index=True)
