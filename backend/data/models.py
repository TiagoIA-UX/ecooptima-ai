from sqlalchemy import Column, Integer, String, Float, DateTime
from .db import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class EnergyRecord(Base):
    __tablename__ = "energy_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
