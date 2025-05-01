import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


# class Office(Base):
#     __tablename__ = "offices"

#     id = Column(Integer, primary_key=True, index=True)
#     business_name = Column(String, index=True)


class Office(Base):
    __tablename__ = "offices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
    # Foreign key to the Company model
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    # relationship to the Company model
    company = relationship("Company", back_populates="offices")
