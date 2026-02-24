
import app.enums.db_bitrix_fields_mapping as field_mapper
import app.db.query_crm_fields as crm_fields_db
import app.settings as settings
import logging

logger = logging.getLogger(__name__)

def build_payload_equip(house_equip):
    equip_payload = dict()

    for key, value in house_equip.items():
        print(f"STATE: {key}:{value}")
        if key not in field_mapper.HouseEquipToEquip.__members__ and key not in ('du'):
            continue

        if key == "equip_name":
            field = crm_fields_db.query_crm_field_by_iblock_element_value(value, settings.settings.EQUIP_ENTITY_ID)
            if not field:
                continue
            equip_payload[field["field_name_unified"]] = field["iblock_element_id"]
            continue

        if key in ('pg', 'boil_setup_name', 'type_boil_classification_name'):
            field_ru_label = field_mapper.HouseEquipToEquip[key].value
            field = crm_fields_db.query_crm_field_by_enum_element_value(str(value), settings.settings.EQUIP_ENTITY_ID)
            if not field:
                continue
            equip_payload[field["field_name_unified"]] = field["enum_element_id"]
            continue

        # Проблема на стороне битрикс
        if key == "type_cat_name":
             bitrix_field_name = field_mapper.HouseEquipToEquip[key].value
             field = crm_fields_db.query_crm_field_by_enum_element_value(str(value), settings.settings.EQUIP_ENTITY_ID)
             if not field:
                 continue
             logger.error(f'!!!{field}!!!')
             #equip_payload[field["field_name_unified"]] = field["enum_element_id"]
             continue


        if key == "du":
            field_ru_label = field_mapper.HouseEquipToEquip[key + "1"].value
            field = crm_fields_db.query_crm_field_by_enum_element_value(str(value), settings.settings.EQUIP_ENTITY_ID)
            if not field:
                continue
            equip_payload[field["field_name_unified"]] = field["enum_element_id"]

            field_ru_label = field_mapper.HouseEquipToEquip[key + "2"].value
            field = crm_fields_db.query_crm_field_by_iblock_element_value(value, settings.settings.EQUIP_ENTITY_ID)
            if not field:
                continue
            equip_payload[field["field_name_unified"]] = field["iblock_element_id"]

            continue

        field_ru_label = field_mapper.HouseEquipToEquip[key].value
        field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.EQUIP_ENTITY_ID)
        equip_payload[field["field_name_unified"]] = value

    # Добавляем отдельно заголовки
    equip_payload["title"] = f'{house_equip["type_cat_name"]}, house_equip_id: {house_equip["id"]}'
    logger.error(equip_payload)

    return equip_payload