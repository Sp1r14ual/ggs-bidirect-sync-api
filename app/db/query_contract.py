from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session, aliased
from app.db.engine import engine
from app.models.contract_category import ContractCategory
from app.models.contract import Contract
from app.models.type_contract import TypeContract
from app.models.type_contract_status import TypeContractStatus
from app.models.type_product import TypeProduct
from app.models.type_contract_person_category import TypeContractPersonCategory
from app.models.organization import Organization
from app.models.person import Person
from app.models.house import House
from app.models.net import Net


def query_contract_by_id(id: int):

    with Session(engine) as db:
        Organization1 = aliased(Organization, name='o1')
        Organization2 = aliased(Organization, name='o2')
        Person1 = aliased(Person, name='p1')
        Person2 = aliased(Person, name='p2')
        # Organization = aliased(Organization, name='o')
        # Person = aliased(Person, name='p')

        query = select(
            Contract.id,
            Contract.number,
            TypeContract.name.label('type_contract_name'),
            TypeContract.prefix.label('type_contract_prefix'),
            TypeContract.crm_category,
            Organization1.company_crm_id.label('id_organization1'),
            Organization2.company_crm_id.label('id_organization2'),
            Person1.contact_crm_id.label('id_person1'),
            Person2.contact_crm_id.label('id_person2'),
            Contract.id_house,
            House.object_ks_crm_id,
            Contract.id_net,
            Net.ground_crm_id,
            TypeContract.id_person,
            TypeContract.id_organization,
            Person.contact_crm_id,
            Organization.company_crm_id,
            TypeContractStatus.name.label('type_contract_status_name'),
            TypeContractPersonCategory.name.label('type_contract_person_category_name'),
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
            Organization, TypeContract.id_organization == Organization.id
        ).outerjoin(
            Person, TypeContract.id_person == Person.id
        ).outerjoin(
            TypeContractPersonCategory, TypeContract.id_type_contract_person_category == TypeContractPersonCategory.id
        ).outerjoin(
            House, Contract.id_house == House.id
        ).outerjoin(
            TypeContractStatus, Contract.id_type_contract_status == TypeContractStatus.id
        ).outerjoin(
            ContractCategory, TypeContract.id_contract_category == ContractCategory.id
        ).outerjoin(
            Net, House.id_net == Net.id
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
    