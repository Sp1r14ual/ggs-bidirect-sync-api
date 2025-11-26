from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class Town(Base):
    __tablename__ = 'town'
    id = Column(Integer, primary_key=True)
    name = Column(String)