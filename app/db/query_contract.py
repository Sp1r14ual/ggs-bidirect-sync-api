from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session, aliased
from app.db.engine import engine
from app.models.contract_category import ContractCategory
from app.models.contract import Contract
from app.models.type_contract import TypeContract
from app.models.type_contract_status import TypeContractStatus
from app.models.type_product import TypeProduct
from app.models.organization import Organization
from app.models.person import Person


def query_contract_by_id(id: int):

    with Session(engine) as db:
        Organization1 = aliased(Organization, name='o1')
        Organization2 = aliased(Organization, name='o2')
        Person1 = aliased(Person, name='p1')
        Person2 = aliased(Person, name='p2')

        query = select(
            Contract.id,
            Contract.number,
            TypeContract.name.label('type_contract_name'),
            TypeContract.prefix.label('type_contract_prefix'),
            TypeContract.crm_category,
            TypeProduct.name.label('type_product_name'),
            Organization1.name.label('organization1_name'),
            Organization2.name.label('organization2_name'),
            Person1.name.label('person1_name'),
            Person2.name.label('person2_name'),
            TypeContractStatus.name.label('type_contract_status_name'),
            ContractCategory.name.label('contract_category_name'),
            Contract.date,
            Contract.start,
            Contract.finish,
            Contract.subject,
            Contract.remark,
            Contract.summ,
            Contract.act_signed,
            Contract.cancel_remark,
            Contract.cancel_date,
            Contract.project_date,
            Contract.contract_crm_id
        ).select_from(Contract
        ).outerjoin(
            TypeContract, Contract.id_type_contract == TypeContract.id
        ).outerjoin(
            TypeProduct, Contract.id_type_product == TypeProduct.id
        ).outerjoin(
            Organization1, Contract.id_organization1 == Organization1.id
        ).outerjoin(
            Organization2, Contract.id_organization2 == Organization2.id
        ).outerjoin(
            Person1, Contract.id_person1 == Person1.id
        ).outerjoin(
            Person2, Contract.id_person2 == Person2.id
        ).outerjoin(
            TypeContractStatus, Contract.id_type_contract_status == TypeContractStatus.id
        ).outerjoin(
            ContractCategory, TypeContract.id_contract_category == ContractCategory.id
        ).where(
            Contract.id == id
        )

        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)

        return result_mapping

def update_contract_with_crm_id(id: int, contract_crm_id: int):
    with Session(autoflush=False, bind=engine) as session:
        query = (
            update(Contract)
            .where(Contract.id == id)
            .values(contract_crm_id=contract_crm_id)
        )

        result = session.execute(query)
        session.commit()
    