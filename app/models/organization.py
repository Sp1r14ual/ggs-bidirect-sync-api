from sqlalchemy import Column, Integer, String, Text, CHAR
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(1024), nullable=True)
    adress_jur = Column(String(1024), nullable=True)
    zip_code_jur = Column(String(6), nullable=True)
    adress_fact = Column(String(1024), nullable=True)
    zip_code_fact = Column(String(6), nullable=True)
    is_coop = Column(Integer, nullable=True)
    is_pir = Column(Integer, nullable=True)
    is_smr_gvd_gnd = Column(Integer, nullable=True)
    is_smr_vdgo = Column(Integer, nullable=True)
    is_to_gvd_gnd = Column(Integer, nullable=True)
    remark = Column(String(1024), nullable=True)
    inn = Column(CHAR(12), nullable=True)
    kpp = Column(CHAR(9), nullable=True)
    bik = Column(CHAR(9), nullable=True)
    korr_acc = Column(CHAR(20), nullable=True)
    calc_acc = Column(CHAR(20), nullable=True)
    bank = Column(String(128), nullable=True)
    is_gro = Column(Integer, nullable=True)
    ogrn = Column(String(32), nullable=True)
    from_1c = Column(Integer, nullable=True)
    to_rg = Column(Integer, nullable=True)
    to_ggs = Column(Integer, nullable=True)
    to_gss = Column(Integer, nullable=True)
    to_ggsi = Column(Integer, nullable=True)
    to_ggss = Column(Integer, nullable=True)
    to_rgs = Column(Integer, nullable=True)
    company_crm_id = Column(Integer, nullable=True)
    requisite_crm_id = Column(Integer, nullable=True)
    bankdetail_requisite_crm_id = Column(Integer, nullable=True)
    has_crm_jur_address = Column(Integer, nullable=True)
    has_crm_fact_address = Column(Integer, nullable=True)