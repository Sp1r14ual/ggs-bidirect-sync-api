from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class ContractCategory(Base):
    __tablename__ = 'contract_category'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64))