from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from app.db.engine import engine
from app.models.house_equip import HouseEquip
from app.models.type_house_equip import TypeHouseEquip
from app.models.type_cat_house_equip import TypeCatHouseEquip
from app.models.type_boil_setup import TypeBoilSetup

def query_house_equip_by_id(id: int):

    with Session(engine) as db:
        query = (
            select(
                HouseEquip.id,
                TypeHouseEquip.name.label('equip_name'),          # Марка
                TypeCatHouseEquip.name.label('type_cat_name'),         # Тип оборудования
                TypeBoilSetup.name.label('boil_setup_name'),      # Тип установки
                HouseEquip.year_produce,
                HouseEquip.power,
                HouseEquip.amount,
                HouseEquip.du,
                HouseEquip.meters,
                HouseEquip.pg,
                HouseEquip.equip_crm_id
            )
            .outerjoin(TypeHouseEquip, HouseEquip.id_type_house_equip == TypeHouseEquip.id)
            .outerjoin(TypeCatHouseEquip, HouseEquip.id_type_cat_house_equip == TypeCatHouseEquip.id)
            .outerjoin(TypeBoilSetup, HouseEquip.id_type_boil_setup == TypeBoilSetup.id)
            .where(HouseEquip.id == id)
        )

        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)

        return result_mapping


def query_house_owners_by_id(id: int):

    with Session(engine) as db:
        query = (
            select(
                HouseEquip.id,
                TypeHouseEquip.name.label('equip_name'),          # Марка
                TypeCatHouseEquip.name.label('type_cat_name'),         # Тип оборудования
                TypeBoilSetup.name.label('boil_setup_name'),      # Тип установки
                HouseEquip.year_produce,
                HouseEquip.power,
                HouseEquip.amount,
                HouseEquip.du,
                HouseEquip.meters,
                HouseEquip.pg,
                HouseEquip.equip_crm_id
            )
            .outerjoin(TypeHouseEquip, HouseEquip.id_type_house_equip == TypeHouseEquip.id)
            .outerjoin(TypeCatHouseEquip, HouseEquip.id_type_cat_house_equip == TypeCatHouseEquip.id)
            .outerjoin(TypeBoilSetup, HouseEquip.id_type_boil_setup == TypeBoilSetup.id)
            .where(HouseEquip.id == id)
        )

        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)

        return result_mapping


def update_house_equip_with_crm_ids(id: int, equip_crm_id: int):
    with Session(autoflush=False, bind=engine) as session:
        query = (
            update(HouseEquip)
            .where(HouseEquip.id == id)
            .values(equip_crm_id=equip_crm_id)
        )

        result = session.execute(query)
        session.commit()