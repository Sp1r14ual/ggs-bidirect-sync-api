from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class CrmFields(Base):
    __tablename__ = 'crm_fields'
    
    id = Column(Integer, primary_key=True, nullable=False)
    field_id = Column(Integer)
    user_type_id = Column(String(100))
    entity_id = Column(String(100))
    iblock_id = Column(Integer)
    field_label_ru = Column(String(100))
    field_label_en = Column(String(100))
    field_name = Column(String(100))
    field_name_unified = Column(String(100))
    enum_element_id = Column(Integer)
    enum_element_value = Column(String(100))
    iblock_element_id = Column(Integer)
    iblock_element_value = Column(String(100))
    is_prod = Column(Integer)

