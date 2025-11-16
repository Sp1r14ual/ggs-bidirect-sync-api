from sqlalchemy import create_engine, select, join, update
from sqlalchemy.orm import Session

from app.models.house import House
from app.models.district import District
from app.models.street import Street
from app.models.town import Town
from app.models.type_client import TypeClient
from app.models.type_house_gazification import TypeHouseGazification
from app.models.organization import Organization
from app.models.grs import Grs
from app.models.type_packing import TypePacking
from app.models.type_pipe_material import TypePipeMaterial


engine = create_engine(
    'mssql+pyodbc://DESKTOP-8F7T81O\\SQLEXPRESS/ggs_stud?driver=SQL+Server+Native+Client+11.0', echo=True)

def clean_result(result):
    result_dict = dict(result)

    # Склеиваем компоненты адреса в одну строку
    result_dict["address"] = ", ".join([
        result_dict["postal_index"] if result_dict["postal_index"] else "",
        result_dict["town"] if result_dict["town"] else "",
        result_dict["street"] if result_dict["street"] else "", 
        result_dict["house_number"] if result_dict["house_number"] else "", 
        result_dict["corpus_number"] if result_dict["corpus_number"] else "", 
        result_dict["flat_number"] if result_dict["flat_number"] else ""
    ])

    # result_dict.pop("postal_index", "default")
    # result_dict.pop("town", "default")
    # result_dict.pop("street", "default")
    # result_dict.pop("house_number", "default")
    # result_dict.pop("corpus_number", "default")
    # result_dict.pop("flat_number", "default")

    return result_dict



def query_house_by_id(id: int):
    with Session(autoflush=False, bind=engine) as session:

        query = (
            select(
                # Объект КС
                House.id,
                House.is_to_from_sibgs,
                House.is_double_adress,
                # Адрес
                House.postal_index,
                Town.name.label('town'),
                Street.name.label('street'),
                House.house_number,
                House.corpus_number,
                House.flat_number,
                #
                TypeClient.name.label('type_client'),
                TypeHouseGazification.name.label('type_house_gazification'),
                District.name.label('district'),
                House.is_ods,
                House.cadastr_number,
                House.cadastr_number_oks,
                Organization.name.label('organization'),
                # Этапы газификации
                House.date_project_agreement,
                House.project_agreement_remark,
                House.start_gas_number,
                House.start_gas_date,
                House.gaz_pusk_date,
                House.gaz_note_date,
                House.mrg_send_note_date,
                House.gaz_off_date,
                House.grs_meters,
                House.start_gaz_remark,
                House.ptu_request_date,
                House.ptu_send_date,
                Grs.name.label('grs'),
                House.spdg_number_protocol,
                House.spdg_date_protocol,
                House.spdg_number,
                House.spdg_date,
                House.gc_plan,
                House.gc_sign,
                House.gc_fact,
                TypePacking.name.label('type_packing'),
                TypePipeMaterial.name.label('type_pipe_material'),
                House.grs_diam
            )
            .select_from(House)
            .join(District, House.id_district == District.id, isouter=True)
            .join(Street, House.id_street == Street.id, isouter=True)
            .join(Town, House.id_town == Town.id, isouter=True)
            .join(TypeClient, House.id_type_client == TypeClient.id, isouter=True)
            .join(TypeHouseGazification, House.id_type_house_gazification == TypeHouseGazification.id, isouter=True)
            .join(Organization, House.id_organization == Organization.id, isouter=True)
            .join(Grs, House.id_grs == Grs.id, isouter=True)
            .join(TypePacking, House.id_type_packing == TypePacking.id, isouter=True)
            .join(TypePipeMaterial, House.id_type_pipe_material == TypePipeMaterial.id, isouter=True)
            .where(House.id == id)
        )

        # Выполнение запроса
        result = session.execute(query).first()._mapping

        result_dict = clean_result(result)

        return result_dict

def update_house_with_crm_ids(id: int, object_ks_crm_id: int, gasification_stage_crm_id: int):
    with Session(autoflush=False, bind=engine) as session:
        query = (
            update(House)
            .where(House.id == id)
            .values(
                object_ks_crm_id=object_ks_crm_id,
                gasification_stage_crm_id=gasification_stage_crm_id
            )
        )

        result = session.execute(query)
        session.commit()
