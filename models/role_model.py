from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())  #  Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())