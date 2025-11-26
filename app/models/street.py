from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class Street(Base):
    __tablename__ = 'street'
    id = Column(Integer, primary_key=True)
    name = Column(String)