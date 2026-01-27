from sqlalchemy import Column, Integer, BigInteger, Numeric, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class HouseOwner(Base):
    __tablename__ = 'house_owner'

    id = Column(Integer, primary_key=True, nullable=False)
    id_house = Column(Integer, ForeignKey('house.id'))
    id_organization = Column(Integer, ForeignKey('organization.id'))
    id_person = Column(Integer, ForeignKey('person.id'))
    remark = Column(String(1024), nullable=True)
    is_actual = Column(Integer, nullable=False)



