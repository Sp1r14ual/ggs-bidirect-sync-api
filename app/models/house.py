from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass

class House(Base):
    __tablename__ = 'house'
    
    id = Column(Integer, primary_key=True)
    is_to_from_sibgs = Column(Integer)
    is_double_adress = Column(Integer)
    postal_index = Column(String)
    house_number = Column(String)
    corpus_number = Column(String)
    flat_number = Column(String)
    is_ods = Column(Integer)
    cadastr_number = Column(String)
    cadastr_number_oks = Column(String)
    date_project_agreement = Column(DateTime)
    project_agreement_remark = Column(String)
    # Поле ГРС (лиды) ?
    start_gas_number = Column(String)
    start_gas_date = Column(DateTime)
    gaz_pusk_date = Column(DateTime)
    gaz_note_date = Column(DateTime)
    mrg_send_note_date = Column(DateTime)
    gaz_off_date = Column(DateTime)
    # Поле Заявка ?
    grs_meters = Column(Numeric(8, 5))
    start_gaz_remark = Column(String)
    ptu_request_date = Column(DateTime)
    ptu_send_date = Column(DateTime)
    # Поле Полученное тех.условие ПТУ?
    # Поле Номер ПТУ?
    # Поле Дата ПТУ?
    # Поле Номер ТУ?
    # Поле Дата ТУ?
    # Поле Код Объекта?
    # Поле Передано в ПТО?
    # Поле Полученное тех.условие?
    spdg_number_protocol = Column(String) # Номер протокола
    spdg_date_protocol = Column(DateTime) # дата
    spdg_number = Column(String) # номер
    spdg_date = Column(DateTime) # дата
    # Поле Мероприятие?
    # Поле Срок исполнения?
    # Поле Перенос?
    # Поле Заявление от?
    # Поле дата?
    # Поле примечание?
    gc_plan = Column(Numeric(8, 5))
    gc_sign = Column(Numeric(8, 5))
    gc_fact = Column(Numeric(8, 5))
    grs_diam = Column(Numeric(8, 5))

    object_ks_crm_id = Column(Integer)
    gasification_stage_crm_id = Column(Integer)

    #Внешние ключи
    id_district = Column(Integer, ForeignKey('district.id'))
    id_street = Column(Integer, ForeignKey('street.id'))
    id_town = Column(Integer, ForeignKey('town.id'))
    id_type_client = Column(Integer, ForeignKey('type_client.id'))
    id_type_house_gazification = Column(Integer, ForeignKey('type_house_gazification.id'))
    id_organization = Column(Integer, ForeignKey('organization.id')) #Есть ли person_id ?
    id_grs = Column(Integer, ForeignKey('grs.id'))
    id_type_packing = Column(Integer, ForeignKey('type_packing.id'))
    id_type_pipe_material = Column(Integer, ForeignKey('type_pipe_material.id'))

