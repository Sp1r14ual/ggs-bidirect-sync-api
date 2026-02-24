from sqlalchemy import create_engine, select, update, literal
from sqlalchemy.orm import Session, aliased
from app.db.engine import engine
from app.models.contract import Contract
from app.models.house import House
from app.models.work_operation import WorkOperation

def query_work_by_id(id: int):

    with Session(engine) as db:

        query = select(
            WorkOperation.id,
            Contract.number.label('contract_number'),
            Contract.id_house,
            WorkOperation.remark,
            WorkOperation.date_appoint,
            WorkOperation.date_complete,
            House.object_ks_crm_id
        ).select_from(WorkOperation
        ).outerjoin(
            Contract, WorkOperation.id_contract == Contract.id
        ).outerjoin(
            House, WorkOperation.id_house == House.id
        ).where(
            WorkOperation.id == id
        )

        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)

        return result_mapping


def update_work_with_crm_id(id: int, work_crm_id: int):
    with Session(autoflush=False, bind=engine) as session:
        query = (
            update(WorkOperation)
            .where(WorkOperation.id == id)
            .values(work_crm_id=work_crm_id)
        )

        result = session.execute(query)
        session.commit()
    