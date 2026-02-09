from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypeBoilClassification(Base):
    __tablename__ = 'type_boil_classification'
    id = Column(Integer, primary_key=True)
    name = Column(String)