from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.settings import settings
from app.db.engine import engine

def query_organization_by_id(id: int):

    with Session(engine) as db:
        query = (select('*').where(Organization.id == id))
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