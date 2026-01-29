from sqlalchemy import create_engine, select, join, update
from sqlalchemy.orm import Session, aliased

from app.models.zm_district import District
from app.models.town import Town
from app.models.zm_gro import Gro
from app.models.net import Net
from app.models.type_net_consumer import TypeNetConsumer
from app.models.type_net_status import TypeNetStatus


from app.db.engine import engine


def query_net_by_id(id: int):
    with Session(autoflush=False, bind=engine) as db:

        g = aliased(Gro, name='g')
        t = aliased(Town, name='t')
        tns = aliased(TypeNetStatus, name='tns')
        tnc = aliased(TypeNetConsumer, name='tnc')
        d = aliased(District, name='d')

        query = select(
            Net.id,
            Net.sys_old,
            Net.name,
            g.name.label('gro_name'),  # Используем label для алиасов в результате
            t.name.label('town_name'),
            tns.name.label('status_name'),
            Net.houses_cnt,
            tnc.name.label('consumer_type_name'),
            d.name.label('district_name'),
            Net.remark,
            Net.ground_crm_id
        ).select_from(Net)\
        .outerjoin(g, Net.crm_id_gro == g.id)\
        .outerjoin(t, Net.id_town == t.id)\
        .outerjoin(tns, Net.id_type_net_status == tns.id)\
        .outerjoin(tnc, Net.id_type_net_consumer == tnc.id)\
        .outerjoin(d, Net.crm_id_district == d.id)\
        .where(Net.id == id)

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
