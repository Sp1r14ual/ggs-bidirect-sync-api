from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypeContractStatus(Base):
    __tablename__ = 'type_contract_status'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64))