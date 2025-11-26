from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.bitrix.object_ks import add_item_for_db_sync as object_ks_add_util
from app.bitrix.gasification_stage import add_item_for_db_sync as gasification_stage_add_util
from app.bitrix.contact import add_item_for_db_sync as contact_add_util
from app.bitrix.company import add_item_for_db_sync as company_add_util
from app.bitrix.requisite import add_item_for_db_sync as requisite_add_util
from app.bitrix.requisite_bankdetail import add_item_for_db_sync as requisite_bankdetail_add_util
from app.bitrix.address import add_item_for_db_sync as address_add_util
from app.db.query_object_ks_gs import query_house_by_id, update_house_with_crm_ids
from app.db.query_contact import query_person_by_id, update_person_with_crm_ids
from app.db.query_company import query_organization_by_id, update_organization_with_crm_ids
from app.enums.db_to_bitrix_fields import HouseToObjectKSFields, HouseToGasificationStageFields, PersonToContactFields, PersonToContactRequisite, PersonToAddress, OrganizationToCompanyFields, OrganizationToCompanyRequisite, OrganizationToCompanyBankdetailRequisite
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

    #Добавить конвертацию bool полей
    for key, value in person.items():
        if key not in PersonToContactFields.__members__:
            continue

        bitrix_field_name = PersonToContactFields[key].value
        contact_payload[bitrix_field_name] = value
    
    return contact_payload

def build_payload_contact_requisite(person, contact_id):
    requisite_payload = {"ENTITY_TYPE_ID": 3, 
                        "ENTITY_ID": contact_id, 
                        "PRESET_ID": 3,
                        "NAME": " ".join([person["family_name"], person["name"], person["patronimic_name"]])}

    for key, value in person.items():
        if key not in PersonToContactRequisite.__members__:
            continue

        bitrix_field_name = PersonToContactRequisite[key].value
        requisite_payload[bitrix_field_name] = value
    
    return requisite_payload

def build_payload_contact_address(person, requisite_id):
    address_payload = {
        "TYPE_ID": 4, # Адрес регистраци
        "ENTITY_TYPE_ID": 8, # Реквизиты
        "ENTITY_ID": requisite_id
    }

    ADDRESS_2 = ""

    for key, value in person.items():
        if key not in PersonToAddress.__members__:
            continue
        
        if key == "reg_address":
            bitrix_field_name = PersonToAddress[key].value
            reg_address_payload[bitrix_field_name] = value
            continue

        if key in ("reg_street", "reg_house", "reg_house"):
            ADDRESS_2 += value + ", "
            continue

        bitrix_field_name = PersonToAddress[key].value
        address_payload[bitrix_field_name] = value

    address_payload["ADDRESS_2"] = ADDRESS_2
    
    return address_payload

@router.get("/person/{id}")
def sync_with_db_person_endpoint(id: int):
    person = query_person_by_id(id)

    if not person:
        raise HTTPException(status_code=400, detail="Person not found") 

    contact_payload = build_payload_contact(person)
    bitrix_contact_id = contact_add_util(contact_payload)

    contact_requisite_payload = build_payload_contact_requisite(person, bitrix_contact_id)
    requisite_contact_id = requisite_add_util(contact_requisite_payload)

    contact_address_payload = build_payload_contact_address(person, requisite_contact_id)
    address_contact_id = address_add_util(contact_address_payload)

    update_person_with_crm_ids(id, bitrix_contact_id, requisite_contact_id)

    return {
        "person_id": id,
        "company_id": bitrix_contact_id,
        "requisite_id": requisite_contact_id,
        # "address_id": address_contact_id
    }

def build_payload_company(organization):
    company_payload = {}

    preset_id = 1

    for key, value in organization.items():
        if key not in OrganizationToCompanyFields.__members__:
            continue

        if key == "name" and "ИП" in value:
            preset_id = 2

        bitrix_field_name = OrganizationToCompanyFields[key].value
        company_payload[bitrix_field_name] = value
    
    return company_payload, preset_id

def build_payload_company_requisite(organization, company_id, preset_id):
    requisite_payload = {"ENTITY_TYPE_ID": 4, 
                        "ENTITY_ID": company_id, 
                        "PRESET_ID": preset_id,
                        "NAME": organization["name"]}

    for key, value in organization.items():
        if key not in OrganizationToCompanyRequisite.__members__:
            continue

        bitrix_field_name = OrganizationToCompanyRequisite[key].value
        requisite_payload[bitrix_field_name] = value
    
    return requisite_payload

def build_payload_company_bankdetail_requisite(organization, requisite_id):
    bankdetail_requisite_payload = {"ENTITY_ID": requisite_id, "NAME": organization["name"]}

    for key, value in organization.items():
        if key not in OrganizationToCompanyBankdetailRequisite.__members__:
            continue

        bitrix_field_name = OrganizationToCompanyBankdetailRequisite[key].value
        bankdetail_requisite_payload[bitrix_field_name] = value
    
    return bankdetail_requisite_payload

@router.get("/organization/{id}")
def sync_with_db_organization_endpoint(id: int):
    organization = query_organization_by_id(id)

    if not organization:
        raise HTTPException(status_code=400, detail="Organization not found") 

    company_payload, preset_id = build_payload_company(organization)
    bitrix_company_id = company_add_util(company_payload)

    company_requisite_payload = build_payload_company_requisite(organization, bitrix_company_id, preset_id)
    requisite_company_id = requisite_add_util(company_requisite_payload)

    company_bankdetail_requisite_payload = build_payload_company_bankdetail_requisite(organization, requisite_company_id)
    bankdetail_requisite_company_id = requisite_bankdetail_add_util(company_bankdetail_requisite_payload)

    update_organization_with_crm_ids(id, bitrix_company_id, requisite_company_id, bankdetail_requisite_company_id)

    return {
        "organization_id": id,
        "company_id": bitrix_company_id,
        "requisite_id": requisite_company_id,
        "bankdetail_requisite_id": bankdetail_requisite_company_id
    }