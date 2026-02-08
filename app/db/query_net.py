from sqlalchemy import create_engine, select, join, update
from sqlalchemy.orm import Session, aliased

from app.models.zm_district import District
from app.models.town import Town
from app.models.zm_gro import Gro
from app.models.net import Net
from app.models.type_net_consumer import TypeNetConsumer
from app.models.type_net_status import TypeNetStatus
from app.models.house import House
from app.models.contract import Contract


from app.db.engine import engine


def query_net_by_id(id: int):
    with Session(autoflush=False, bind=engine) as db:

        query = select(
            Net.id,
            Net.sys_old,
            Net.name,
            Gro.name.label('gro_name'),  # Используем label для алиасов в результате
            Town.name.label('town_name'),
            TypeNetStatus.name.label('status_name'),
            Net.houses_cnt,
            TypeNetConsumer.name.label('consumer_type_name'),
            District.name.label('district_name'),
            Net.remark,
            Net.ground_crm_id,
            House.id.label("house_id"),
            House.object_ks_crm_id,
            Contract.id.label("contract_id"),
            Contract.contract_crm_id
        ).select_from(Net).outerjoin(
            Gro, Net.crm_id_gro == Gro.id
        ).outerjoin(
            Town, Net.id_town == Town.id
        ).outerjoin(
            TypeNetStatus, Net.id_type_net_status == TypeNetStatus.id
        ).outerjoin(
            TypeNetConsumer, Net.id_type_net_consumer == TypeNetConsumer.id
        ).outerjoin(
            District, Net.crm_id_district == District.id
        ).outerjoin(
            House, House.id_net == Net.id
        ).outerjoin(
            Contract, Contract.id_net == Net.id
        ).where(Net.id == id)

        # Выполнение запроса
        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)

        return result_mapping

def update_net_with_crm_id(id: int, ground_crm_id: int):
    with Session(autoflush=False, bind=engine) as session:
        query = (
            update(Net)
            .where(Net.id == id)
            .values(
                ground_crm_id=ground_crm_id
            )
        )

        result = session.execute(query)
        session.commit()
