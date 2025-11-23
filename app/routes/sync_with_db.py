from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.bitrix.object_ks import add_item_for_db_sync as object_ks_add_util
from app.bitrix.gasification_stage import add_item_for_db_sync as gasification_stage_add_util
from app.bitrix.contact import add_item_for_db_sync as contact_add_util
from app.db.query_object_ks_gs import query_house_by_id, update_house_with_crm_ids
from app.db.query_contact import query_person_by_id
from app.enums.db_to_bitrix_fields import HouseToObjectKSFields, HouseToGasificationStageFields, PersonToContactFields
from app.enums.object_ks import ObjectKSFields, ClientType, GasificationType, District
from app.enums.gasification_stage import GasificationStageFields, Event, Grs2, Pad, Material

router = APIRouter(prefix="/sync_with_db", tags=["db"])

def build_payloads_object_ks_gs(house):
    object_ks_payload = dict()
    gasification_stage_payload = dict()

    for key, value in house.items():

        # pydantic_schema_field_name = HouseToObjectKSFields[key].value
        # bitrix_field_name = ObjectKSFields[pydantic_schema_field_name].value

        if key == "id":
            pydantic_schema_field_name = HouseToObjectKSFields[key].value
            bitrix_field_name = ObjectKSFields[pydantic_schema_field_name].value
            object_ks_payload[bitrix_field_name] = value

        elif key in ("postal_index", "town", "street", "house_number", "corpus_number", "flat_number"):
            continue

        elif key in ("is_to_from_sibgs", "is_double_adress", "is_ods"):
            pydantic_schema_field_name = HouseToObjectKSFields[key].value
            # print(pydantic_schema_field_name)
            bitrix_field_name = ObjectKSFields[pydantic_schema_field_name].value
            # print(bitrix_field_name)
            object_ks_payload[bitrix_field_name] = "Y" if bool(value) else "N"

        elif key == "type_client":
            pydantic_schema_field_name = HouseToObjectKSFields[key].value
            bitrix_field_name = ObjectKSFields[pydantic_schema_field_name].value
            object_ks_payload[bitrix_field_name] = ClientType(value).value

        elif key == "type_house_gazification":
            pydantic_schema_field_name = HouseToObjectKSFields[key].value
            bitrix_field_name = ObjectKSFields[pydantic_schema_field_name].value
            object_ks_payload[bitrix_field_name] = GasificationType(value).value

        elif key == "district":
            pydantic_schema_field_name = HouseToObjectKSFields[key].value
            bitrix_field_name = ObjectKSFields[pydantic_schema_field_name].value
            object_ks_payload[bitrix_field_name] = District(value).value

        elif key in ("cadastr_number", "cadastr_number_oks", "address", "organization"): # Что делать с organization?
            pydantic_schema_field_name = HouseToObjectKSFields[key].value
            bitrix_field_name = ObjectKSFields[pydantic_schema_field_name].value
            object_ks_payload[bitrix_field_name] = value
        
        elif key == "grs":
            pydantic_schema_field_name = HouseToGasificationStageFields[key].value
            bitrix_field_name = GasificationStageFields[pydantic_schema_field_name].value
            gasification_stage_payload[bitrix_field_name] = Grs2(value).value

        elif key == "type_packing":
            pydantic_schema_field_name = HouseToGasificationStageFields[key].value
            bitrix_field_name = GasificationStageFields[pydantic_schema_field_name].value
            gasification_stage_payload[bitrix_field_name] = Pad(value).value

        elif key == "type_pipe_material":
            pydantic_schema_field_name = HouseToGasificationStageFields[key].value
            bitrix_field_name = GasificationStageFields[pydantic_schema_field_name].value
            gasification_stage_payload[bitrix_field_name] = Material(value).value
        
        elif key == "type_spdg_action":
            pydantic_schema_field_name = HouseToGasificationStageFields[key].value
            bitrix_field_name = GasificationStageFields[pydantic_schema_field_name].value
            gasification_stage_payload[bitrix_field_name] = Event(value).value

        else:
            pydantic_schema_field_name = HouseToGasificationStageFields[key].value
            bitrix_field_name = GasificationStageFields[pydantic_schema_field_name].value
            gasification_stage_payload[bitrix_field_name] = value

    
    return object_ks_payload, gasification_stage_payload

@router.get("/house/{id}")
def sync_with_db_house_endpoint(id: int):
    house = query_house_by_id(id)

    if not house:
        raise HTTPException(status_code=400, detail="House not found") 

    object_ks_payload, gasification_stage_payload = build_payloads_object_ks_gs(house)

    object_ks_crm_id = object_ks_add_util(object_ks_payload)["id"]

    gasification_stage_payload["parentId1066"] = object_ks_crm_id

    gasification_stage_crm_id = gasification_stage_add_util(gasification_stage_payload)["id"]

    update_house_with_crm_ids(id, object_ks_crm_id, gasification_stage_crm_id)

    return {
        "house_id": id,
        "object_ks_crm_id": object_ks_crm_id,
        "gasification_stage_crm_id": gasification_stage_crm_id
    }


def build_payload_contact(person):
    contact_payload = {}

    for key, value in person.items():
        if key not in PersonToContactFields.__members__:
            continue

        bitrix_field_name = PersonToContactFields[key].value
        contact_payload[bitrix_field_name] = value
    
    return contact_payload


@router.get("/person/{id}")
def sync_with_db_person_endpoint(id: int):
    person = query_person_by_id(id)

    if not person:
        raise HTTPException(status_code=400, detail="Person not found") 

    contact_payload = build_payload_contact(person)

    bitrix_item = contact_add_util(contact_payload)

    return bitrix_item

@router.get("/organization/{id}")
def sync_with_db_organization_endpoint(id: int):
    pass
