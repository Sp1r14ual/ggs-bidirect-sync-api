from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from app.db.engine import engine
from app.models.house_owner import HouseOwner
from app.models.person import Person
from app.models.organization import Organization


def query_house_owner_by_house(id_house: int):
    """
    владельцы объекта КС
    """
    with Session(engine) as db:
        query = (
            select(
                HouseOwner.id,
                HouseOwner.id_person,
                HouseOwner.id_organization,
                HouseOwner.remark,
                Person.contact_crm_id,
                Organization.company_crm_id
            )
            .outerjoin(Person, Person.id == HouseOwner.id_person)
            .outerjoin(Organization, Organization.id == HouseOwner.id_organization)
            .where(and_(HouseOwner.id_house == id_house, HouseOwner.is_actual == 1))
        )

        result = db.execute(query).first()

        if not result:
            return None

        result_mapping = dict(result._mapping)

        return result_mapping
