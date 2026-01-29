from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from app.db.query_equip import query_equip_by_id, update_equip_with_crm_ids
from app.db.query_house_equip import query_house_equip_by_id, update_house_equip_with_crm_ids
from app.db.query_contract import query_contract_by_id, update_contract_with_crm_id
from app.db.query_crm_fields import query_crm_field_by_elem_value
from app.db.query_net import query_net_by_id, update_net_with_crm_id
from app.enums.equip import EquipType, PackingType, MarkType, DuType, DiameterType, StoveType, PipeMaterialType, BoilSetupType
from app.enums.contract import ContractType, ContractTypePrefix, ContractCategory, ContractKind, ContractCurrentStatus
from app.enums.db_to_bitrix_fields import EquipToEquip, HouseEquipToEquip, ContractToContract, NetToGround
from app.bitrix.equip import add_item_for_db_sync as equip_add_util, update_item_for_db_sync as equip_update_util
from app.bitrix.contract import add_item_for_db_sync as contract_add_util, update_item_for_db_sync as contract_update_util
from app.bitrix.ground import add_item_for_db_sync as ground_add_util, update_item_for_db_sync as ground_update_util
from app.routes.sync_with_db import sync_with_db_house_endpoint

router = APIRouter(prefix="/bidirect_sync2", tags=["bidirect_sync2"])

def build_payload_equip(equip, house_equip):
    equip_payload = dict()

    for key, value in equip.items():
        print(f"STATE: {key}:{value}")
        if key not in EquipToEquip.__members__:
            continue

        elif key in ('packing_name', 'pipe_material_name'):
            crm_field = query_crm_field_by_elem_value(value)
            if not crm_field:
                continue
            field_name_unified = crm_field["field_name_unified"]
            elem_id = crm_field["elem_id"]
            equip_payload[field_name_unified] = elem_id

            continue

        # elif key == "packing_name":
        #     bitrix_field_name = EquipToEquip[key].value
        #     equip_payload[bitrix_field_name] = PackingType(value).value
        #     continue
        
        # elif key == "diameter_type_name":
        #     bitrix_field_name = EquipToEquip[key].value
        #     equip_payload[bitrix_field_name] = DiameterType(value).value
        #     continue

        # elif key == "pipe_material_name":
        #     bitrix_field_name = EquipToEquip[key].value
        #     equip_payload[bitrix_field_name] = PipeMaterialType(value).value
        #     continue
        
        else:
            bitrix_field_name = EquipToEquip[key].value
            equip_payload[bitrix_field_name] = value

    for key, value in house_equip.items():
        print(f"STATE: {key}:{value}")
        if key not in HouseEquipToEquip.__members__ and key not in ('du'):
            continue

        elif key in ('equip_name', 'boil_setup_name', 'pg'):
            if key == 'pg':
                crm_field = query_crm_field_by_elem_value("ПГ-" + str(value))
            # elif key == "du":
            #     # Дополнительно проанализировать значения диаметров
            #     crm_field = query_crm_field_by_elem_value(value)
            else:
                crm_field = query_crm_field_by_elem_value(value)
            if not crm_field:
                continue
            field_name_unified = crm_field["field_name_unified"]
            elem_id = crm_field["elem_id"]
            equip_payload[field_name_unified] = elem_id

            continue

        # elif key == "equip_name":
        #     bitrix_field_name = HouseEquipToEquip[key].value

        #     if value not in MarkType.__members__:
        #         continue

        #     equip_payload[bitrix_field_name] = MarkType(value).value
        #     continue

        #Разобраться, почему не работает
        # elif key == "type_cat_name":
        #     bitrix_field_name = HouseEquipToEquip[key].value
        #     equip_payload[bitrix_field_name] = EquipType(value).value
        #     continue

        # elif key == "boil_setup_name":
        #     bitrix_field_name = HouseEquipToEquip[key].value
        #     equip_payload[bitrix_field_name] = BoilSetupType(value).value
        #     continue

        elif key == "du":
            bitrix_field_name = HouseEquipToEquip[key + "1"].value
            equip_payload[bitrix_field_name] = DiameterType(value).value

            bitrix_field_name = HouseEquipToEquip[key + "2"].value
            equip_payload[bitrix_field_name] = DuType(value).value

            continue

        # elif key == "pg":
        #     bitrix_field_name = HouseEquipToEquip[key].value
        #     equip_payload[bitrix_field_name] = StoveType(value).value
        #     continue


        bitrix_field_name = HouseEquipToEquip[key].value
        equip_payload[bitrix_field_name] = value   

    
    return equip_payload

@router.get("/equip/{equip_id}/house_equip/{house_equip_id}")
def sync_with_db_equip_endpoint(equip_id: int, house_equip_id: int):
    # Достаём оборудование из БД по id
    equip: dict = query_equip_by_id(equip_id)
    house_equip: dict = query_house_equip_by_id(house_equip_id)

    if not(equip and house_equip):
        raise HTTPException(status_code=400, detail="Equip not found") 
    
    # return {
    #     "equip": equip,
    #     "house_equip": house_equip
    # }

    # Собираем payload оборудования для отправки в битрикс
    equip_payload = build_payload_equip(equip, house_equip)

    #Вытаскиваем crm_id
    equip_crm_id = equip["equip_crm_id"]

    # Проверяем, если equip_crm_id не null в обеих таблицах, то обновляем, иначе создаем новую
    if equip["equip_crm_id"] and house_equip["equip_crm_id"]:
        res = equip_update_util(equip_crm_id, equip_payload)
    else:
        equip_crm_id = equip_add_util(equip_payload)["id"]

    # Обновляем обе таблицы
    update_equip_with_crm_ids(equip_id, equip_crm_id)
    update_house_equip_with_crm_ids(house_equip_id, equip_crm_id)
   
    return {
        "equip_id": equip_id,
        "house_equip_id": house_equip_id,
        "equip_crm_id": equip_crm_id
    }

def build_payload_contract(contract):
    contract_payload = dict()

    for key, value in contract.items():
        if key not in ContractToContract.__members__ and key not in ('type_contract_prefix', 'date', 'contact_crm_id', 'company_crm_id', 'type_contract_person_category_name'):
            continue

        if key in ('type_contract_name', 'type_contract_prefix', 'type_contract_status_name', 'crm_category', 'type_contract_person_category_name'):
            if key == 'type_contract_status_name':
                crm_field = query_crm_field_by_elem_value(value.capitalize())
            else:
                crm_field = query_crm_field_by_elem_value(value)
            if not crm_field:
                continue
            field_name_unified = crm_field["field_name_unified"]
            elem_id = crm_field["elem_id"]
            contract_payload[field_name_unified] = elem_id

            continue

        # elif key == "type_contract_name":
        #     if key not in ContractType.__members__:
        #         continue

        #     bitrix_field_name = ContractToContract[key].value
        #     contract_payload[bitrix_field_name] = ContractType(value).value
        #     continue

        # elif key == "type_contract_prefix":
        #     if key not in ContractTypePrefix.__members__:
        #         continue

        #     bitrix_field_name = ContractToContract[key].value
        #     contract_payload[bitrix_field_name] = ContractTypePrefix(value).value
        #     continue

        # elif key == "type_contract_status_name":
        #     bitrix_field_name = ContractToContract[key].value

        #     if value in ("действует", "проект"):
        #         contract_payload[bitrix_field_name] = ContractCurrentStatus("Действует").value
        #     else:
        #         contract_payload[bitrix_field_name] = ContractCurrentStatus("Окончен").value
        #     continue
    
        # elif key == "crm_category":
        #     bitrix_field_name = ContractToContract[key].value
        #     contract_payload[bitrix_field_name] = ContractCategory(value).value
        #     continue

        # Несоответствие значений в БД и битриксе
        #   
        # elif key == "contract_category_name":
        #     bitrix_field_name = ContractToContract[key].value
        #     contract_payload[bitrix_field_name] = ContractKind(value).value
        #     continue
          
        if key in ("id_person1", "id_organization1"):
            if value is None:
                continue
            if key == "id_person1":
                bitrix_field_name = ContractToContract[key].value
                contract_payload[bitrix_field_name] = "C_" + str(value)   
                continue
            else:
                bitrix_field_name = ContractToContract[key].value
                contract_payload[bitrix_field_name] = "CO_" + str(value)
                continue

        if key in ("id_person2", "id_organization2"):
            if value is None:
                continue
            if key == "id_person2":
                bitrix_field_name = ContractToContract[key].value
                contract_payload[bitrix_field_name] = "C_" + str(value)   
                continue
            else:
                bitrix_field_name = ContractToContract[key].value
                contract_payload[bitrix_field_name] = "CO_" + str(value)
                continue

        if key in ('contact_crm_id', 'company_crm_id'):
            if key == "contact_crm_id" and value:
                contract_payload["contactId"] = value
            elif key == "company_crm_id" and value:
                contract_payload["companyId"] = value
            continue

        if key == "date":
            bitrix_field_name = ContractToContract[key + "1"].value
            contract_payload[bitrix_field_name] = value
            bitrix_field_name = ContractToContract[key + "2"].value
            contract_payload[bitrix_field_name] = value
            continue

        bitrix_field_name = ContractToContract[key].value
        contract_payload[bitrix_field_name] = value   
    
    return contract_payload

@router.get("/contract/{contract_id}")
def sync_with_db_contracts_endpoint(contract_id: int):
    # Достаём оборудование из БД по id
    contract: dict = query_contract_by_id(contract_id)

    if not contract:
        raise HTTPException(status_code=400, detail="Contract not found")

    # если пустой contact_crm_id но не  пустой id_person, то синхроним его и перезапрашиваем
    if contract["id_person"] and not contract["contact_crm_id"]:
        sync_with_db_person_endpoint(contract["id_person"], contract["object_ks_crm_id"])
        contract = query_contract_by_id(contract_id)
        
    # если пустой company_crm_id но не  пустой id_organization, то синхроним его
    if contract["id_organization"] and not contract["company_crm_id"]:
        sync_with_db_organization_endpoint(contract["id_organization"], contract["object_ks_crm_id"])
        contract = query_contract_by_id(contract_id)

    if contract["id_house"] and not contract["object_ks_crm_id"]:
        sync_with_db_house_endpoint(contract["id_house"])
        contract = query_contract_by_id(contract_id)

    # Собираем payload договора для отправки в битрикс
    contract_payload = build_payload_contract(contract)

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
        res = contract_update_util(contract_crm_id, contract_payload)
    else:
        contract_crm_id = contract_add_util(contract_payload)["id"]

    # Обновляем таблицу
    update_contract_with_crm_id(contract_id, contract_crm_id)

    # Ещё раз вызываем синхронизацию, чтобы записать id договора в объект кс
    sync_with_db_house_endpoint(contract["id_house"], contract_crm_id)
   
    return {
        "contract_id": contract_id,
        "contract_crm_id": contract_crm_id
    }


def build_payload_ground(ground: dict):
    ground_payload = dict()

    for key, value in ground.items():

        if key not in NetToGround.__members__:
            continue

        if key in ("gro_name", "town_name", "status_name", "consumer_type_name", "district_name"):
            crm_field = query_crm_field_by_elem_value(value)
            if not crm_field:
                continue
            field_name_unified = crm_field["field_name_unified"]
            elem_id = crm_field["elem_id"]
            ground_payload[field_name_unified] = elem_id

            continue

        if key == "name":
            ground_payload["TITLE"] = value
        
        bitrix_field_name = NetToGround[key].value
        ground_payload[bitrix_field_name] = value
    
    return ground_payload

@router.get("/ground/{ground_id}")
def sync_with_db_ground_endpoint(ground_id: int):

    # Достаём площадку из БД по id
    ground: dict = query_net_by_id(ground_id)
    ground_id = ground["id"]

    if not ground:
        raise HTTPException(status_code=400, detail="Contract not found")


    ground_payload = build_payload_ground(ground)

    #Вытаскиваем crm_id
    ground_crm_id = ground["ground_crm_id"]

    # Проверяем, если contract_crm_id не null в обеих таблицах, то обновляем, иначе создаем новую
    if ground_crm_id:
        res = ground_update_util(ground_crm_id, ground_payload)
    else:
        ground_crm_id = ground_add_util(ground_payload)["id"]

    # Обновляем таблицу
    update_net_with_crm_id(ground_id, ground_crm_id)
   
    return {
        "ground_id": ground_id,
        "ground_crm_id": ground_crm_id
    }
    
    # return {
    #     "ground": ground,
    #     "ground_payload": ground_payload
    # }
