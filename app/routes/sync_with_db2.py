from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from app.db.query_equip import query_equip_by_id, update_equip_with_crm_ids
from app.db.query_house_equip import query_house_equip_by_id, update_house_equip_with_crm_ids
from app.enums.equip import EquipType, PackingType, MarkType, DiameterType, PipeMaterialType, BoilSetupType
from app.enums.db_to_bitrix_fields import EquipToEquip, HouseEquipToEquip
from app.bitrix.equip import add_item_for_db_sync as equip_add_util, update_item_for_db_sync as equip_update_util

router = APIRouter(prefix="/bidirect_sync2", tags=["bidirect_sync2"])

def build_payload_equip(equip, house_equip):
    equip_payload = dict()

    for key, value in equip.items():
        if key not in EquipToEquip.__members__:
            continue

        elif key == "packing_name":
            bitrix_field_name = EquipToEquip[key].value
            equip_payload[bitrix_field_name] = PackingType(value).value
            continue
        
        elif key == "diameter_type_name":
            bitrix_field_name = EquipToEquip[key].value
            equip_payload[bitrix_field_name] = DiameterType(value).value
            continue

        elif key == "pipe_material_name":
            bitrix_field_name = EquipToEquip[key].value
            equip_payload[bitrix_field_name] = PipeMaterialType(value).value
            continue
        
        else:
            bitrix_field_name = EquipToEquip[key].value
            equip_payload[bitrix_field_name] = value

    for key, value in house_equip.items():
        if key not in HouseEquipToEquip.__members__:
            continue

        elif key == "equip_name":
            bitrix_field_name = HouseEquipToEquip[key].value

            if value not in MarkType.__members__:
                continue

            equip_payload[bitrix_field_name] = MarkType(value).value
            continue

        #Разобраться, почему не работает
        # elif key == "type_cat_name":
        #     bitrix_field_name = HouseEquipToEquip[key].value
        #     equip_payload[bitrix_field_name] = EquipType(value).value
        #     continue

        elif key == "boil_setup_name":
            bitrix_field_name = HouseEquipToEquip[key].value
            equip_payload[bitrix_field_name] = BoilSetupType(value).value
            continue

        if key == "amount":
            print(f"amount: {value}")

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