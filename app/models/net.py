from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class Net(Base):
    __tablename__ = 'net'

    id = Column(Integer, primary_key=True)
    sys_old = Column(BigInteger)
    name = Column(String(256))
    houses_cnt = Column(Integer)
    remark = Column(String(512))
    crm_id_gro = Column(Integer, ForeignKey('zm.gro.id'))
    crm_id_district = Column(Integer, ForeignKey('zm.district.id'))
    id_town = Column(Integer, ForeignKey('town.id'))
    id_type_net_status = Column(Integer, ForeignKey('type_net_status.id'))
    id_type_net_consumer = Column(Integer, ForeignKey('type_net_consumer.id'))
    ground_crm_id = Column(Integer)



