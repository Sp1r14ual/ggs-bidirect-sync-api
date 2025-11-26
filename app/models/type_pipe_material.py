from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class TypePipeMaterial(Base):
    __tablename__ = 'type_pipe_material'
    id = Column(Integer, primary_key=True)
    name = Column(String)