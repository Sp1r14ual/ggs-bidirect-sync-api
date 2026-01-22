from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class CrmFields(Base):
    __tablename__ = 'crm_fields'
    
    id = Column(Integer, primary_key=True, nullable=False)
    field_id = Column(Integer)
    entity_id = Column(String(100))
    field_name = Column(String(100))
    field_name_unified = Column(String(100))
    elem_id = Column(Integer)
    elem_value = Column(String(100))
    is_prod = Column(Integer)

