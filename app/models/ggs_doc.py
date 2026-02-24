from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): 
    pass


class GgsDoc(Base):
    __tablename__ = 'ggs_doc'
    id = Column(Integer, primary_key=True)
    doc_num = Column(String)
    doc_date = Column(DateTime)
    is_actual = Column(Integer)
    id_type_ggs_doc = Column(Integer,  ForeignKey('type_ggs_doc.id'))
    id_house = Column(Integer,  ForeignKey('house.id'))
