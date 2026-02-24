from sqlalchemy import create_engine, inspect, text, select, and_
from sqlalchemy.orm import Session
from app.db.engine import engine
from app.models.crm_fields import CrmFields
from app.settings import settings

def create_crm_fields_table():

    inspector = inspect(engine)

    # Если таблица уже есть, дропаем
    if inspector.has_table("crm_fields"):
        CrmFields.__table__.drop(engine)

    # Создаем новую
    CrmFields.__table__.create(engine)
    return True

def fill_info_crm_fields_table(rows: list):
    with Session(engine) as db:
        db.add_all(rows)
        db.commit()
        return True

def query_crm_field_by_ru_label(ru_label: str, entity_id: str):
    with Session(engine) as db:
        # entity_id нужен для избежания коллизий при существовании несколько одноименных полей в разных модулях CRM
        if isinstance(ru_label, tuple):
            ru_label = ru_label[0]
        query = (select('*').where(and_(CrmFields.field_label_ru == ru_label, CrmFields.entity_id == entity_id)))
        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)
        return result_mapping

def query_crm_field_by_iblock_element_value(value: str, entity_id: str):
    with Session(engine) as db:
        # entity_id нужен для избежания коллизий при существовании несколько одноименных полей в разных модулях CRM
        query = (select('*').where(and_(CrmFields.iblock_element_value == value, CrmFields.entity_id == entity_id)))
        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)
        return result_mapping
 

def query_crm_field_by_enum_element_value(value: str, entity_id: str, key: str = None):
    """
    value: значение по которому получать id, например ТО ВДГО
    entity_id: для какой сущности, например CRM_13
    key: доп. уточнение например type_product_name
    """
    with Session(engine) as db:
        if key:
            condition = and_(CrmFields.enum_element_value == value, CrmFields.entity_id == entity_id,
                             CrmFields.field_label_en == key)
        else:
            condition = and_(CrmFields.enum_element_value == value, CrmFields.entity_id == entity_id)
        query = (select('*').where(condition))
        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)
        return result_mapping



