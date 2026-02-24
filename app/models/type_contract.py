from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypeContract(Base):
    __tablename__ = 'type_contract'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(512))
    prefix = Column(String(6))
    id_contract_category = Column(Integer, ForeignKey("contract_category.id"))
    id_person = Column(Integer, ForeignKey("person.id"))
    id_organization = Column(Integer, ForeignKey("organization.id"))
    id_type_contract_person_category = Column(Integer, ForeignKey("type_contract_person_category.id"))
    crm_category = Column(String(32))
    id_type_product = Column(Integer, ForeignKey('type_product.id'))