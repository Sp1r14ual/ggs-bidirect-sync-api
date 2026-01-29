from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypeContractPersonCategory(Base):
    __tablename__ = 'type_contract_person_category'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(256))