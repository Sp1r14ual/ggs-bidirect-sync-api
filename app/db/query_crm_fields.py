from sqlalchemy import create_engine, inspect, text, select
from sqlalchemy.orm import Session
from app.db.engine import engine
from app.models.crm_fields import CrmFields

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

def query_crm_field_by_elem_value(value: str):
    with Session(engine) as db:
        query = (select('*').where(CrmFields.elem_value == value))
        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)
        return result_mapping



