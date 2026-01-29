from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypeNetStatus(Base):
    __tablename__ = 'type_net_status'
    id = Column(Integer, primary_key=True)
    name = Column(String)