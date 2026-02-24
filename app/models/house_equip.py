from sqlalchemy import Column, Integer, BigInteger, Numeric, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class HouseEquip(Base):
    __tablename__ = 'house_equip'

    id = Column(Integer, primary_key=True, nullable=False)
    id_type_house_equip = Column(Integer, ForeignKey('type_house_equip.id'))  
    remark = Column(String(128), nullable=True)
    amount = Column(Integer, nullable=True)
    power = Column(Numeric(precision=6, scale=2), nullable=True)
    meters = Column(Numeric(precision=6, scale=2), nullable=True)
    id_type_cat_house_equip = Column(Integer, ForeignKey('type_cat_house_equip.id')) 
    year_produce = Column(Integer, nullable=True)
    id_type_boil_setup = Column(Integer, ForeignKey('type_boil_setup.id'))
    du = Column(Integer, nullable=True)
    pg = Column(Integer, nullable=True)
    equip_crm_id = Column(Integer, nullable=True)
    id_type_boil_classification = Column(Integer, ForeignKey('type_boil_classification.id'))
    id_house = Column(Integer, ForeignKey('house.id'))


