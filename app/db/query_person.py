from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from app.models.person import Person
from app.models.house_owner import HouseOwner
from app.models.house import House
from app.models.type_contract import TypeContract
from app.models.contract import Contract
from app.db.engine import engine

def query_person_by_id(id: int):

    with Session(engine) as db:
        query = (select(
            Person.id,
            Person.family_name,
            Person.birthdate,
            Person.phone_number,
            Person.name,
            Person.patronimic_name,
            Person.pasport_serial,
            Person.pasport_number,
            Person.pasport_date,
            Person.pasport_place,
            Person.remark,
            Person.dep_code,
            Person.reg_adress,
            Person.reg_region,
            Person.reg_raion,
            Person.reg_city,
            Person.reg_street,
            Person.reg_house,
            Person.reg_flat,
            Person.postal_index,
            Person.inn,
            Person.ogrn,
            Person.snils,
            Person.email,
            Person.contact_crm_id,
            Person.requisite_crm_id,
            Person.has_crm_address,
            House.id.label("house_id"),
            House.object_ks_crm_id,
            Contract.id.label("contract_id"),
            Contract.contract_crm_id
        )
        .select_from(Person)
        .join(HouseOwner, HouseOwner.id_person == Person.id, isouter=True)
        .join(House, HouseOwner.id_house == House.id, isouter=True)
        .join(TypeContract, TypeContract.id_person == Person.id, isouter=True)
        .join(Contract, Contract.id_type_contract == TypeContract.id, isouter=True)
        .where(Person.id == id))
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
                has_crm_address=int(has_crm_address)
            )
        )

        result = session.execute(query)
        session.commit()