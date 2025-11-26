from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypePacking(Base):
    __tablename__ = 'type_packing'
    id = Column(Integer, primary_key=True)
    name = Column(String)