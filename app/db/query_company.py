from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from app.models.organization import Organization

engine = create_engine(
    'mssql+pyodbc://DESKTOP-OE5G1EA\\SQLEXPRESS/ggs_stud?driver=SQL+Server+Native+Client+11.0', echo=True)

def query_organization_by_id(id: int):

    with Session(engine) as db:
        query = (select('*').where(Organization.id == id))
        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)
        return result_mapping

def update_organization_with_crm_ids(id: int, company_crm_id: int, requisite_crm_id: int, bankdetail_requisite_crm_id: int):
    with Session(autoflush=False, bind=engine) as session:
        query = (
            update(Organization)
            .where(Organization.id == id)
            .values(
                company_crm_id=company_crm_id,
                requisite_crm_id=requisite_crm_id,
                bankdetail_requisite_crm_id=bankdetail_requisite_crm_id
            )
        )

        result = session.execute(query)
        session.commit()