from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.models.house_owner import HouseOwner
from app.models.house import House
from app.models.type_contract import TypeContract
from app.models.contract import Contract
from app.settings import settings
from app.db.engine import engine

def query_organization_by_id(id: int):

    with Session(engine) as db:
        query = (select(
            Organization.id,
            Organization.name,
            Organization.adress_jur,
            Organization.zip_code_jur,
            Organization.adress_fact,
            Organization.zip_code_fact,
            Organization.is_coop,
            Organization.is_pir,
            Organization.is_smr_gvd_gnd,
            Organization.is_smr_vdgo,
            Organization.is_to_gvd_gnd,
            Organization.remark,
            Organization.inn,
            Organization.kpp,
            Organization.bik,
            Organization.korr_acc,
            Organization.calc_acc,
            Organization.bank,
            Organization.is_gro,
            Organization.ogrn,
            Organization.from_1c,
            Organization.to_rg,
            Organization.to_ggs,
            Organization.to_gss,
            Organization.to_ggsi,
            Organization.to_ggss,
            Organization.to_rgs,
            Organization.company_crm_id,
            Organization.requisite_crm_id,
            Organization.bankdetail_requisite_crm_id,
            Organization.has_crm_jur_address,
            Organization.has_crm_fact_address,
            House.id.label("house_id"),
            House.object_ks_crm_id,
            Contract.id.label("contract_id"),
            Contract.contract_crm_id
        )
        .join(HouseOwner, HouseOwner.id_organization == Organization.id, isouter=True)
        .join(House, HouseOwner.id_house == House.id, isouter=True)
        .join(TypeContract, TypeContract.id_organization == Organization.id, isouter=True)
        .join(Contract, Contract.id_type_contract == TypeContract.id, isouter=True)
        .where(Organization.id == id))

        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)
        return result_mapping

def update_organization_with_crm_ids(id: int, company_crm_id: int, requisite_crm_id: int, bankdetail_requisite_crm_id: int, has_address_jur_company: bool, has_address_fact_company: bool):
    with Session(autoflush=False, bind=engine) as session:
        query = (
            update(Organization)
            .where(Organization.id == id)
            .values(
                company_crm_id=company_crm_id,
                requisite_crm_id=requisite_crm_id,
                bankdetail_requisite_crm_id=bankdetail_requisite_crm_id,
                has_crm_jur_address=int(has_address_jur_company),
                has_crm_fact_address=int(has_address_fact_company)
            )
        )

        result = session.execute(query)
        session.commit()