"""
ТО, ремонты
"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.mssql import MONEY


class Base(DeclarativeBase): 
    pass


class WorkOperation(Base):
    __tablename__ = 'work_operation'
    
    id = Column(Integer, primary_key=True, nullable=False)
    id_contract = Column(Integer, ForeignKey('contract.id'))
    id_house = Column(Integer, ForeignKey('house.id'))
    date_appoint = Column(DateTime)
    date_complete = Column(DateTime)
    remark = Column(String(512))
    work_crm_id = Column(Integer)
