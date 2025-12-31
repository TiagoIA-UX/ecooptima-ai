from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from .db import Base
import datetime

class CarbonCredit(Base):
    __tablename__ = "carbon_credits"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)  # kgCO2
    price = Column(Float, nullable=False)   # valor em moeda
    currency = Column(String, default="BRL")
    country = Column(String, default="BR")
    status = Column(String, default="disponível")  # disponível, vendido, reservado
    verified = Column(String, default="pendente")  # pendente, verificado, rejeitado
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CarbonTransaction(Base):
    __tablename__ = "carbon_transactions"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, nullable=False)
    seller_id = Column(Integer, nullable=False)
    credit_id = Column(Integer, ForeignKey("carbon_credits.id"), nullable=False)
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="BRL")
    country = Column(String, default="BR")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
