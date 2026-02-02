from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from app.db.query_equip import query_equip_by_id, update_equip_with_crm_ids
from app.db.query_house_equip import query_house_equip_by_id, update_house_equip_with_crm_ids
from app.db.query_contract import query_contract_by_id, update_contract_with_crm_id
# from app.db.query_crm_fields import query_crm_field_by_elem_value
from app.db.query_net import query_net_by_id, update_net_with_crm_id
from app.enums.equip import EquipType, PackingType, MarkType, DuType, DiameterType, StoveType, PipeMaterialType, BoilSetupType
from app.enums.contract import ContractType, ContractTypePrefix, ContractCategory, ContractKind, ContractCurrentStatus
from app.enums.db_to_bitrix_fields import EquipToEquip, HouseEquipToEquip, ContractToContract, NetToGround
from app.bitrix.equip import add_item_for_db_sync as equip_add_util, update_item_for_db_sync as equip_update_util
from app.bitrix.contract import add_item_for_db_sync as contract_add_util, update_item_for_db_sync as contract_update_util
from app.bitrix.ground import add_item_for_db_sync as ground_add_util, update_item_for_db_sync as ground_update_util
# from app.routes.sync_with_db import sync_with_db_house_endpoint

router = APIRouter(prefix="/bidirect_sync2", tags=["bidirect_sync2"])


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

@router.post("/ground/{ground_id}")
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
