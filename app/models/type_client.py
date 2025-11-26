from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypeClient(Base):
    __tablename__ = 'type_client'
    id = Column(Integer, primary_key=True)
    name = Column(String)