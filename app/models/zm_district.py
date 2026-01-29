from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class District(Base):
    __tablename__ = 'district'
    __table_args__ = {'schema': 'zm'}
    id = Column(Integer, primary_key=True)
    name = Column(String)