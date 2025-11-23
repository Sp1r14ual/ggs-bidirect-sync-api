from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, nullable=False)
    family_name = Column(String(1024), nullable=True)
    birthdate = Column(DateTime, nullable=True)
    phone_number = Column(String(16), nullable=True)
    name = Column(String(1024), nullable=True)
    patronimic_name = Column(String(1024), nullable=True)
    pasport_serial = Column(String(6), nullable=True)
    pasport_number = Column(String(12), nullable=True)
    pasport_date = Column(DateTime, nullable=True)
    pasport_place = Column(String(512), nullable=True)
    remark = Column(String(512), nullable=True)
    dep_code = Column(String(6), nullable=True)
    reg_adress = Column(String(1024), nullable=True)
    reg_region = Column(String(200), nullable=True)
    reg_raion = Column(String(200), nullable=True)
    reg_city = Column(String(200), nullable=True)
    reg_street = Column(String(200), nullable=True)
    reg_house = Column(String(200), nullable=True)
    reg_flat = Column(String(20), nullable=True)
    postal_index = Column(String(6), nullable=True)
    inn = Column(String(16), nullable=True)
    ogrn = Column(String(32), nullable=True)
    snils = Column(String(32), nullable=True)
    email = Column(String(32), nullable=True)