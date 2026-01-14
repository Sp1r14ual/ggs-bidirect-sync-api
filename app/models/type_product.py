from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.mssql import MONEY

class Base(DeclarativeBase): 
    pass

class TypeProduct(Base):
    __tablename__ = 'type_product'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(512))
    shortname = Column(String(16))