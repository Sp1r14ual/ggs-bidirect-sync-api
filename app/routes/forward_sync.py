import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

import app.bitrix.forward_sync as forward_sync_bitrix
import app.utils.object_ks_gs as object_ks_gs_utils
import app.utils.contact as contact_utils
import app.utils.company as company_utils
import app.utils.equip as equip_utils
import app.utils.contract as contract_utils
import app.utils.ground as ground_utils
import app.settings as settings
import app.db.query_house as query_house
import app.db.query_house_owner as query_house_owner
import app.db.query_person as query_person
import app.db.query_organization as query_organization
import app.db.query_equip as query_equip
import app.db.query_house_equip as query_house_equip
import app.db.query_contract as query_contract
import app.db.query_net as query_net

router = APIRouter(prefix="/forward_sync", tags=["forward_sync"])

@router.post("/house/{id}")
def forward_sync_house_endpoint(id: int) -> dict:
    '''Эндпоинт для синхронизации битрикс-сущностей Объект КС и Этапы газификации с таблицей house'''

    # Получаем house, house_owner, net из БД
    house = query_house.query_house_by_id(id)
    house_owner = query_house_owner.query_house_owner_by_house(id)

    net = None
    if house["id_net"]:
        net = query_net.query_net_by_id(house["id_net"])

    contract = None
    if house["contract_id"]:
        contract = query_contract.query_contract_by_id(house["contract_id"])

    #если пустой contact_crm_id, но не пустой id_person, то синхроним его и перезапрашиваем
    if house_owner["id_person"] and not house_owner["contact_crm_id"]:
        forward_sync_person_endpoint(house_owner["id_person"], id)
        house_owner = query_house_owner.query_house_owner_by_house(id)

    # если пустой company_crm_id, но не пустой id_organization, то синхроним его
    if house_owner["id_organization"] and not house_owner["company_crm_id"]:
        forward_sync_organization_endpoint(house_owner["id_organization"], id)
        house_owner = query_house_owner.query_house_owner_by_house(id)

    # Если площадка существует, но при этом она не синхронизирована с crm, то синхроним
    if net and not net["ground_crm_id"]:
        forward_sync_ground_endpoint(net["id"])
        net = query_net.query_net_by_id(house["id_net"])

    if contract and not contract["contract_crm_id"]:
        forward_sync_contract_endpoint(contract["id"])
        contract = query_contract.query_contract_by_id(house["contract_id"])

    house["contact_id"] = house_owner["contact_crm_id"]
    house["company_id"] = house_owner["company_crm_id"]

    # Возвращаем ошибку, если house пустой
    if not house:
        raise HTTPException(status_code=400, detail="House not found")

    # Получаем из house id объекта КС и этапа газификации в битриксе
    object_ks_crm_id, gasification_stage_crm_id = house["object_ks_crm_id"], house["gasification_stage_crm_id"]

    # Собираем payload для Объекта КС и Этапа газификации, который будет отправлен в битрикс
    object_ks_payload, gasification_stage_payload = object_ks_gs_utils.build_payloads_object_ks_gs(house)

    # Добавляем id договора в payload перед отправкой
    if contract["contract_crm_id"]:
        object_ks_payload["parentId1078"] = contract["contract_crm_id"]

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

    # Добавляем id Объекта КС в payload этапа газификации перед отправкой
    gasification_stage_payload["parentId1066"] = object_ks_crm_id

    # Если gasification_stage_crm_id не null, значит этап газификации в битриксе существует, вызываем процедуру обновления
    if gasification_stage_crm_id:
        res = forward_sync_bitrix.update_item(gasification_stage_crm_id, settings.settings.GASIFICATION_STAGE_TYPE_ID, gasification_stage_payload)
        print(res)
    # Иначе создаем новый этап газификации в битриксе и сохраняем его id
    else:
        gasification_stage_crm_id = forward_sync_bitrix.add_item(settings.settings.GASIFICATION_STAGE_TYPE_ID, gasification_stage_payload)["id"]

    # Добавляем crm_id в house
    query_house.update_house_with_crm_ids(id, object_ks_crm_id, gasification_stage_crm_id)

    # Возвращаем объект с id-шниками на клиент
    return {
        "house_id": id,
        "object_ks_crm_id": object_ks_crm_id,
        "gasification_stage_crm_id": gasification_stage_crm_id
    }

# @router.post("/person/{id}/objectks/{object_ks_id}")
@router.post("/person/{id}")
def forward_sync_person_endpoint(id: int, object_ks_id: Optional[int] = None) -> dict:
    '''Эндпоинт для синхронизации битрикс-контактов с таблицей person'''

    # Достаем person из БД по id
    person: dict = query_person.query_person_by_id(id)

    if not person:
        raise HTTPException(status_code=400, detail="Person not found")

    # Достаем crm id контакта, его реквизиты и наличие адреса
    bitrix_contact_id: int = person["contact_crm_id"]
    requisite_contact_id: int = person["requisite_crm_id"]
    crm_contact_address: bool = person["has_crm_address"]

    #Собираем payload для создания/обновления битрикс-контакта
    contact_payload = contact_utils.build_payload_contact(person)

    # !!! Сделать получение id домовладения из БД
    if object_ks_id:
        contact_payload["parentId1066"] = object_ks_id

    # Если контакт уже существует в битрикс, то запускаем процедуру обновления
    if bitrix_contact_id:
        res = forward_sync_bitrix.update_contact(bitrix_contact_id, contact_payload)
    # Иначе создаем новый контакт в битриксе 
    else:
        bitrix_contact_id = forward_sync_bitrix.add_contact(contact_payload)

    # Собираем payload реквизитов контакта для отправки в битрикс
    contact_requisite_payload = contact_utils.build_payload_contact_requisite(person, bitrix_contact_id)

    # Если реквизит существует, то обновляем
    if requisite_contact_id:
        res = forward_sync_bitrix.update_requisite(requisite_contact_id, contact_requisite_payload)
    # Иначе создаем новый
    else:
        requisite_contact_id = forward_sync_bitrix.add_requisite(contact_requisite_payload)

    # Собираем payload адреса, который будет вложен в реквизиты контакта в битриксе
    contact_address_payload = contact_utils.build_payload_contact_address(person, requisite_contact_id)

    # Если адрес уже существует у контакта в битриксе, запускаем процедуру обновления
    if crm_contact_address:
        has_crm_address = forward_sync_bitrix.update_address(contact_address_payload)
    # Иначе создаем новый адрес
    else:
        has_crm_address = forward_sync_bitrix.add_address(contact_address_payload)

    # Обновляем все связные id-шники в таблице organization
    query_person.update_person_with_crm_ids(id, bitrix_contact_id, requisite_contact_id, has_crm_address)

    return {
        "person_id": id,
        "contact_id": bitrix_contact_id,
        "requisite_id": requisite_contact_id,
        "has_crm_address": has_crm_address
    }

# @router.post("/organization/{id}/objectks/{object_ks_id}")
@router.post("/organization/{id}")
def forward_sync_organization_endpoint(id: int, object_ks_id: Optional[int] = None):

    # Достаём организацию из БД по id
    organization: dict = query_organization.query_organization_by_id(id)

    if not organization:
        raise HTTPException(status_code=400, detail="Organization not found") 

    # Достаём id-шники из organization
    bitrix_company_id: int = organization["company_crm_id"]
    requisite_company_id: int = organization["requisite_crm_id"]
    bankdetail_requisite_company_id: int = organization["bankdetail_requisite_crm_id"]
    has_address_jur_company: int = organization["has_crm_jur_address"]
    has_address_fact_company: int = organization["has_crm_fact_address"]

    # Собираем payload компании для отправки в битрикс
    company_payload, preset_id = company_utils.build_payload_company(organization)

    # !!! Доставать из БД
    if object_ks_id:
        company_payload["parentId1066"] = object_ks_id

    # Если компания в битриксе уже существует, то обновляем
    if bitrix_company_id:
        res = forward_sync_bitrix.update_company(bitrix_company_id, company_payload)
    # Иначе создаем новую компанию
    else:
        bitrix_company_id = forward_sync_bitrix.add_company(company_payload)

    # Собираем payload для универсальных реквизитов компании
    company_requisite_payload = company_utils.build_payload_company_requisite(organization, bitrix_company_id, preset_id)

    # Если реквизиты компании в битриксе уже существуют, то обновляем
    if requisite_company_id:
        res = forward_sync_bitrix.update_requisite(requisite_company_id, company_requisite_payload)
    # Иначе создаем новые
    else:
        requisite_company_id = forward_sync_bitrix.add_requisite(company_requisite_payload)

    # Собираем payload для банковских реквизитов компании для отправки в битрикс
    company_bankdetail_requisite_payload = company_utils.build_payload_company_bankdetail_requisite(organization, requisite_company_id)
    
    # Если банковские реквизиты компании уже существуют, то обновляем
    if bankdetail_requisite_company_id:
        res = forward_sync_bitrix.update_bankdetail_requisite(bankdetail_requisite_company_id, company_bankdetail_requisite_payload)
    # Иначе создаем новые
    else:
        bankdetail_requisite_company_id = forward_sync_bitrix.add_bankdetail_requisite(company_bankdetail_requisite_payload)

    # Собираем payload-ы для юридического и фактического адресов компании для отправки в битрикс
    address_jur_payload, address_fact_payload = company_utils.build_payload_company_address(organization, requisite_company_id)
    
    # Если юридический адрес уже есть, то обновляем
    if has_address_jur_company:
        res = forward_sync_bitrix.update_address(address_jur_payload)
    # Иначе создаем
    else:
        has_address_jur_company = forward_sync_bitrix.add_address(address_jur_payload)

    # Если фактический адрес уже есть, то обновляем
    if has_address_fact_company:
        res = forward_sync_bitrix.update_address(address_fact_payload)
    # Иначе создаем
    else:
        has_address_fact_company = forward_sync_bitrix.add_address(address_fact_payload)

    # Обновляем все crm id-шники в БД
    query_organization.update_organization_with_crm_ids(id, bitrix_company_id, requisite_company_id, bankdetail_requisite_company_id, has_address_jur_company, has_address_fact_company)

    return {
        "organization_id": id,
        "company_id": bitrix_company_id,
        "requisite_id": requisite_company_id,
        "bankdetail_requisite_id": bankdetail_requisite_company_id,
        "has_address_jur_company": has_address_jur_company,
        "has_address_fact_company": has_address_fact_company
    }

@router.post("/equip/{equip_id}/house_equip/{house_equip_id}")
def forward_sync_equip_endpoint(equip_id: int, house_equip_id: int):
    # Достаём оборудование из БД по id
    equip: dict = query_equip.query_equip_by_id(equip_id)
    house_equip: dict = query_house_equip.query_house_equip_by_id(house_equip_id)

    if not(equip and house_equip):
        raise HTTPException(status_code=400, detail="Equip not found") 

    # Собираем payload оборудования для отправки в битрикс
    equip_payload = equip_utils.build_payload_equip(equip, house_equip)

    # return {
    #     "equip": equip,
    #     "house_equip": house_equip,
    #     "equip_payload": equip_payload
    # }

    #Вытаскиваем crm_id
    equip_crm_id = equip["equip_crm_id"]

    # Проверяем, если equip_crm_id не null в обеих таблицах, то обновляем, иначе создаем новую
    if equip["equip_crm_id"] and house_equip["equip_crm_id"]:
        res = forward_sync_bitrix.update_item(equip_crm_id, settings.settings.EQUIP_TYPE_ID, equip_payload)
    else:
        equip_crm_id = forward_sync_bitrix.add_item(settings.settings.EQUIP_TYPE_ID, equip_payload)["id"]

    # Обновляем обе таблицы
    query_equip.update_equip_with_crm_ids(equip_id, equip_crm_id)
    query_house_equip.update_house_equip_with_crm_ids(house_equip_id, equip_crm_id)
   
    return {
        "equip_id": equip_id,
        "house_equip_id": house_equip_id,
        "equip_crm_id": equip_crm_id
    }

@router.post("/contract/{contract_id}")
def forward_sync_contract_endpoint(contract_id: int):
    # Достаём оборудование из БД по id
    contract: dict = query_contract.query_contract_by_id(contract_id)

    if not contract:
        raise HTTPException(status_code=400, detail="Contract not found")

    # если пустой contact_crm_id но не пустой id_person, то синхроним его и перезапрашиваем
    if contract["id_person"] and not contract["contact_crm_id"]:
        forward_sync_person_endpoint(contract["id_person"], contract["object_ks_crm_id"])
        contract = query_contract.query_contract_by_id(contract_id)
        
    # если пустой company_crm_id но не пустой id_organization, то синхроним его
    if contract["id_organization"] and not contract["company_crm_id"]:
        forward_sync_organization_endpoint(contract["id_organization"], contract["object_ks_crm_id"])
        contract = query_contract.query_contract_by_id(contract_id)

    if contract["id_house"] and not contract["object_ks_crm_id"]:
        forward_sync_house_endpoint(contract["id_house"])
        contract = query_contract.query_contract_by_id(contract_id)

    # Собираем payload договора для отправки в битрикс
    contract_payload = contract_utils.build_payload_contract(contract)

    if contract["object_ks_crm_id"]:
        contract_payload["parentId1066"] = contract["object_ks_crm_id"]

    # return {
    #     "contract_db": contract,
    #     "contract_payload_bitrix": contract_payload
    # }

    #Вытаскиваем crm_id
    contract_crm_id = contract["contract_crm_id"]

    # Проверяем, если contract_crm_id не null в обеих таблицах, то обновляем, иначе создаем новую
    if contract["contract_crm_id"]:
        res = forward_sync_bitrix.update_item(contract_crm_id, settings.settings.CONTRACT_TYPE_ID, contract_payload)
    else:
        contract_crm_id = forward_sync_bitrix.add_item(settings.settings.CONTRACT_TYPE_ID, contract_payload)["id"]

    # Обновляем таблицу
    query_contract.update_contract_with_crm_id(contract_id, contract_crm_id)

    # Ещё раз вызываем синхронизацию, чтобы записать id договора в объект кс
    forward_sync_house_endpoint(contract["id_house"], contract_crm_id)
   
    return {
        "contract_id": contract_id,
        "contract_crm_id": contract_crm_id
    }

@router.post("/ground/{ground_id}")
def forward_sync_ground_endpoint(ground_id: int):

    # Достаём площадку из БД по id
    ground: dict = query_net.query_net_by_id(ground_id)
    ground_id = ground["id"]

    if not ground:
        raise HTTPException(status_code=400, detail="Contract not found")


    ground_payload = ground_utils.build_payload_ground(ground)

    #Вытаскиваем crm_id
    ground_crm_id = ground["ground_crm_id"]

    # Проверяем, если contract_crm_id не null в обеих таблицах, то обновляем, иначе создаем новую
    if ground_crm_id:
        res = forward_sync_bitrix.update_item(ground_crm_id, settings.settings.GROUND_TYPE_ID, ground_payload)
    else:
        ground_crm_id = forward_sync_bitrix.add_item(settings.settings.GROUND_TYPE_ID, ground_payload)["id"]

    # Обновляем таблицу
    query_net.update_net_with_crm_id(ground_id, ground_crm_id)
   
    return {
        "ground_id": ground_id,
        "ground_crm_id": ground_crm_id
    }
    
    # return {
    #     "ground": ground,
    #     "ground_payload": ground_payload
    # }