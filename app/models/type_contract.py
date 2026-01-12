from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypeContract(Base):
    __tablename__ = 'type_contract'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(512))
    prefix = Column(String(6))
    id_contract_category = Column(Integer, ForeignKey("contract_category.id"))
    crm_category = Column(String(32))