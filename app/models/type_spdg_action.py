from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypeSPDGAction(Base):
    __tablename__ = 'type_spdg_action'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)