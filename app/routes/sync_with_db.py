import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.bitrix.contact import add_item_for_db_sync as contact_add_util, update_item_for_db_sync as contact_update_util
from app.bitrix.company import add_item_for_db_sync as company_add_util, update_item_for_db_sync as company_update_util
from app.bitrix.requisite import add_item_for_db_sync as requisite_add_util, update_item_for_db_sync as requisite_update_util
from app.bitrix.requisite_bankdetail import add_item_for_db_sync as requisite_bankdetail_add_util, update_item_for_db_sync as requisite_bankdetail_update_util
from app.bitrix.address import add_item_for_db_sync as address_add_util, update_item_for_db_sync as address_update_util

from app.db.query_contact import query_person_by_id, update_person_with_crm_ids
from app.db.query_company import query_organization_by_id, update_organization_with_crm_ids

from app.enums.db_to_bitrix_fields import HouseToObjectKSFields, HouseToGasificationStageFields, PersonToContactFields, PersonToContactRequisite, PersonToAddress, OrganizationToCompanyFields, OrganizationToAddress, OrganizationToCompanyRequisite, OrganizationToCompanyBankdetailRequisite
from app.enums.object_ks import ObjectKSFields, ClientType, GasificationType, District
from app.enums.gasification_stage import GasificationStageFields, Event, Grs2, Pad, Material
####################################
import app.bitrix.forward_sync as forward_sync_bitrix
import app.utils.object_ks_gs as object_ks_gs_utils
import app.settings as settings
import app.db.query_house as query_house
import app.db.query_house_owner as query_house_owner

router = APIRouter(prefix="/forward_sync", tags=["forward_sync"])

# @router.post("/house/{id}/contract_id/{contract_crm_id}")
@router.post("/house/{id}")
def sync_with_db_house_endpoint(id: int, contract_crm_id: Optional[int] = None) -> dict:
    '''Эндпоинт для синхронизации битрикс-сущностей Объект КС и Этапы газификации с таблицей house'''

    # Получаем house и house_owner из БД
    house = query_house.query_house_by_id(id)
    house_owner = query_house_owner.query_house_owner_by_house(id)

    #если пустой contact_crm_id, но не пустой id_person, то синхроним его и перезапрашиваем
    if house_owner["id_person"] and not house_owner["contact_crm_id"]:
        sync_with_db_person_endpoint(house_owner["id_person"], id)
        house_owner = query_house_owner.query_house_owner_by_house(id)

    # если пустой company_crm_id, но не пустой id_organization, то синхроним его
    if house_owner["id_organization"] and not house_owner["company_crm_id"]:
        sync_with_db_organization_endpoint(house_owner["id_organization"], id)
        house_owner = query_house_owner.query_house_owner_by_house(id)

    house["contact_id"] = house_owner["contact_crm_id"]
    house["company_id"] = house_owner["company_crm_id"]

    # Возвращаем ошибку, если house пустой
    if not house:
        raise HTTPException(status_code=400, detail="House not found")

    # Получаем из house id объекта КС и этапа газификации в битриксе
    object_ks_crm_id, gasification_stage_crm_id = house["object_ks_crm_id"], house["gasification_stage_crm_id"]

    # Собираем payload для Объекта КС и Этапа газификации, который будет отправлен в битрикс
    # object_ks_payload, gasification_stage_payload = build_payloads_object_ks_gs(house)
    object_ks_payload, gasification_stage_payload = object_ks_gs_utils.build_payloads_object_ks_gs2(house)

    # !!! доставать id договора из БД 
    if contract_crm_id:
        object_ks_payload["parentId1078"] = contract_crm_id

    # return {
    #     "object_ks_payload": object_ks_payload,
    #     "gasification_stage_payload": gasification_stage_payload
    # }

    # Если object_ks_crm_id не null, значит объект КС в битриксе существует, вызываем процедуру обновления
    if object_ks_crm_id:
        res = forward_sync_bitrix.update_item(object_ks_crm_id, settings.settings.OBJECT_KS_TYPE_ID, object_ks_payload)
        print(res)
    # Иначе создаем новый Объект КС в битриксе и сохраняем его id
    else:
        object_ks_crm_id = forward_sync_bitrix.add_item(settings.settings.OBJECT_KS_TYPE_ID, object_ks_payload)["id"]

    # Сохраняем id Объекта КС в payload этапа газификации к битриксу
    gasification_stage_payload["parentId1066"] = object_ks_crm_id

    # Если gasification_stage_crm_id не null, значит этап газификации в битриксе существует, вызываем процедуру обновления
    if gasification_stage_crm_id:
        # res = gasification_stage_update_util(gasification_stage_crm_id, gasification_stage_payload)
        res = forward_sync_bitrix.update_item(gasification_stage_crm_id, settings.settings.GASIFICATION_STAGE_TYPE_ID, gasification_stage_payload)
        print(res)
    # Иначе создаем новый этап газификации в битриксе и сохраняем его id
    else:
        # gasification_stage_crm_id = gasification_stage_add_util(gasification_stage_payload)["id"]
        gasification_stage_crm_id = forward_sync_bitrix.add_item(settings.settings.GASIFICATION_STAGE_TYPE_ID, gasification_stage_payload)["id"]

    # Добавляем crm_id в house
    query_house.update_house_with_crm_ids(id, object_ks_crm_id, gasification_stage_crm_id)

    # Возвращаем объект с id-шниками на клиент
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
            ADDRESS_2 += str(value) + ", "
            continue

        bitrix_field_name = PersonToAddress[key].value
        address_payload[bitrix_field_name] = value

    address_payload["ADDRESS_2"] = ADDRESS_2
    
    return address_payload

@router.post("/person/{id}/objectks/{object_ks_id}")
def sync_with_db_person_endpoint(id: int, object_ks_id: Optional[int]) -> dict:
    '''Эндпоинт для синхронизации битрикс-контактов с таблицей person'''

    # Достаем person из БД по id
    person: dict = query_person_by_id(id)

    if not person:
        raise HTTPException(status_code=400, detail="Person not found")

    # Достаем crm id контакта, его реквизиты и наличие адреса
    bitrix_contact_id: int = person["contact_crm_id"]
    requisite_contact_id: int = person["requisite_crm_id"]
    crm_contact_address: bool = person["has_crm_address"]

    #Собираем payload для создания/обновления битрикс-контакта
    contact_payload = build_payload_contact(person)

    if object_ks_id:
        contact_payload["parentId1066"] = object_ks_id

    # Если контакт уже существует в битрикс, то запускаем процедуру обновления
    if bitrix_contact_id:
        res = contact_update_util(bitrix_contact_id, contact_payload)
    # Иначе создаем новый контакт в битриксе 
    else:
        bitrix_contact_id = contact_add_util(contact_payload)

    # Собираем payload реквизитов контакта для отправки в битрикс
    contact_requisite_payload = build_payload_contact_requisite(person, bitrix_contact_id)

    if requisite_contact_id:
        res = requisite_update_util(requisite_contact_id, contact_requisite_payload)
    # Иначе создаем новый контакт в битриксе 
    else:
        requisite_contact_id = requisite_add_util(contact_requisite_payload)

    # Собираем payload адреса, который будет вложен в реквизиты контакта в битриксе
    contact_address_payload = build_payload_contact_address(person, requisite_contact_id)

    # Если адрес уже существует у контакта в битриксе, запускаем процедуру обновления
    if crm_contact_address:
        has_crm_address = address_update_util(contact_address_payload)
    # Иначе создаем новый адрес
    else:
        has_crm_address = address_add_util(contact_address_payload)

    # Обновляем все связные id-шники в таблице organization
    update_person_with_crm_ids(id, bitrix_contact_id, requisite_contact_id, has_crm_address)

    return {
        "person_id": id,
        "contact_id": bitrix_contact_id,
        "requisite_id": requisite_contact_id,
        "has_crm_address": has_crm_address
    }

def build_payload_company(organization: dict) -> (dict, int):
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

def build_payload_company_address(organization: dict, requisite_id: int) -> (dict, dict):
    jur_address_payload = {
        "TYPE_ID": 6, # Юридический адрес
        "ENTITY_TYPE_ID": 8, # Реквизиты
        "ENTITY_ID": requisite_id
    }

    fact_address_payload = {
        "TYPE_ID": 1, # Фактический адрес
        "ENTITY_TYPE_ID": 8, # Реквизиты
        "ENTITY_ID": requisite_id
    }

    for key, value in organization.items():
        if key not in OrganizationToAddress.__members__:
            continue

        if key in ("adress_jur", "zip_code_jur"):
            bitrix_field_name = OrganizationToAddress[key].value
            jur_address_payload[bitrix_field_name] = value
            continue
        
        if key in ("adress_fact", "zip_code_fact"):
            bitrix_field_name = OrganizationToAddress[key].value
            fact_address_payload[bitrix_field_name] = value
            continue
    
    return jur_address_payload, fact_address_payload

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

@router.post("/organization/{id}/objectks/{object_ks_id}")
def sync_with_db_organization_endpoint(id: int, object_ks_id: Optional[int]):

    # Достаём организацию из БД по id
    organization: dict = query_organization_by_id(id)

    if not organization:
        raise HTTPException(status_code=400, detail="Organization not found") 

    # Достаём id-шники из organization
    bitrix_company_id: int = organization["company_crm_id"]
    requisite_company_id: int = organization["requisite_crm_id"]
    bankdetail_requisite_company_id: int = organization["bankdetail_requisite_crm_id"]
    has_address_jur_company: int = organization["has_crm_jur_address"]
    has_address_fact_company: int = organization["has_crm_fact_address"]

    # Собираем payload компании для отправки в битрикс
    company_payload, preset_id = build_payload_company(organization)

    if object_ks_id:
        company_payload["parentId1066"] = object_ks_id

    # Если компания в битриксе уже существует, то обновляем
    if bitrix_company_id:
        res = company_update_util(bitrix_company_id, company_payload)
    # Иначе создаем новую компанию
    else:
        bitrix_company_id = company_add_util(company_payload)

    # Собираем payload для универсальных реквизитов компании
    company_requisite_payload = build_payload_company_requisite(organization, bitrix_company_id, preset_id)

    # Если реквизиты компании в битриксе уже существуют, то обновляем
    if requisite_company_id:
        res = requisite_update_util(requisite_company_id, company_requisite_payload)
    # Иначе создаем новые
    else:
        requisite_company_id = requisite_add_util(company_requisite_payload)

    # Собираем payload для банковских реквизитов компании для отправки в битрикс
    company_bankdetail_requisite_payload = build_payload_company_bankdetail_requisite(organization, requisite_company_id)
    
    # Если банковские реквизиты компании уже существуют, то обновляем
    if bankdetail_requisite_company_id:
        res = requisite_bankdetail_update_util(bankdetail_requisite_company_id, company_bankdetail_requisite_payload)
    # Иначе создаем новые
    else:
        bankdetail_requisite_company_id = requisite_bankdetail_add_util(company_bankdetail_requisite_payload)

    # Собираем payload-ы для юридического и фактического адресов компании для отправки в битрикс
    address_jur_payload, address_fact_payload = build_payload_company_address(organization, requisite_company_id)
    
    # Если юридический адрес уже есть, то обновляем
    if has_address_jur_company:
        res = address_update_util(address_jur_payload)
    # Иначе создаем
    else:
        has_address_jur_company = address_add_util(address_jur_payload)

    # Если фактический адрес уже есть, то обновляем
    if has_address_fact_company:
        res = address_update_util(address_fact_payload)
    # Иначе создаем
    else:
        has_address_fact_company = address_add_util(address_fact_payload)

    # Обновляем все crm id-шники в БД
    update_organization_with_crm_ids(id, bitrix_company_id, requisite_company_id, bankdetail_requisite_company_id, has_address_jur_company, has_address_fact_company)

    return {
        "organization_id": id,
        "company_id": bitrix_company_id,
        "requisite_id": requisite_company_id,
        "bankdetail_requisite_id": bankdetail_requisite_company_id,
        "has_address_jur_company": has_address_jur_company,
        "has_address_fact_company": has_address_fact_company
    }