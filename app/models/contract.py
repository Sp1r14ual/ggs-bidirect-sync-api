from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.mssql import MONEY

class Base(DeclarativeBase): 
    pass

class Contract(Base):
    __tablename__ = 'contract'
    
    id = Column(Integer, primary_key=True, nullable=False)
    number = Column(String(256))
    id_type_contract = Column(Integer, ForeignKey('type_contract.id'))
    id_type_product = Column(Integer, ForeignKey('type_product.id'))
    id_organization1 = Column(Integer, ForeignKey('organization.id'))
    id_organization2 = Column(Integer, ForeignKey('organization.id'))
    id_person1 = Column(Integer, ForeignKey('person.id'))
    id_person2 = Column(Integer, ForeignKey('person.id'))
    id_house = Column(Integer, ForeignKey('house.id'))
    date = Column(DateTime)
    start = Column(DateTime)
    finish = Column(DateTime)
    subject = Column(String(4000))
    remark = Column(String(512))
    summ = Column(MONEY)
    act_signed = Column(DateTime)
    cancel_remark = Column(String(512))
    cancel_date = Column(DateTime)
    id_type_contract_status = Column(Integer)
    project_date = Column(Date)
    contract_crm_id = Column(Integer)