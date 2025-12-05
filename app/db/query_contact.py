from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from app.models.person import Person

engine = create_engine(
    'mssql+pyodbc://DESKTOP-OE5G1EA\\SQLEXPRESS/ggs_stud?driver=SQL+Server+Native+Client+11.0', echo=True)

def query_person_by_id(id: int):

    with Session(engine) as db:
        query = (select('*').where(Person.id == id))
        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)
        return result_mapping
        
def update_person_with_crm_ids(id: int, contact_crm_id: int, requisite_crm_id: int, has_crm_address: bool):
    with Session(autoflush=False, bind=engine) as session:
        query = (
            update(Person)
            .where(Person.id == id)
            .values(
                contact_crm_id=contact_crm_id,
                requisite_crm_id=requisite_crm_id,
                has_crm_address = 1 if has_crm_address else 0
            )
        )

        result = session.execute(query)
        session.commit()