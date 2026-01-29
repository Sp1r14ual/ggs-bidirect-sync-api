from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class Gro(Base):
    __tablename__ = 'gro'
    __table_args__ = {'schema': 'zm'}
    id = Column(Integer, primary_key=True)
    name = Column(String)