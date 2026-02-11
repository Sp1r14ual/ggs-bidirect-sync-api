
import app.enums.db_bitrix_fields_mapping as field_mapper
import app.db.query_crm_fields as crm_fields_db
import app.settings as settings

def build_payload_ground(ground: dict):
    ground_payload = dict()

    for key, value in ground.items():

        if key not in field_mapper.NetToGround.__members__:
            continue

        if key in ("gro_name", "town_name", "status_name", "consumer_type_name"):
            field = crm_fields_db.query_crm_field_by_enum_element_value(str(value), settings.settings.GROUND_ENTITY_ID)
            if not field:
                continue
            ground_payload[field["field_name_unified"]] = field["enum_element_id"]

            continue

        if key == "district_name":
            field = crm_fields_db.query_crm_field_by_iblock_element_value(value, settings.settings.GROUND_ENTITY_ID)
            if not field:
                continue
            ground_payload[field["field_name_unified"]] = field["iblock_element_id"]

            continue

        if key in ('contact_crm_id', 'company_crm_id'):
            if key == "contact_crm_id" and value:
                contract_payload["contactId"] = value
            elif key == "company_crm_id" and value:
                contract_payload["companyId"] = value
            continue

        # if key == "name":
        #     ground_payload["TITLE"] = value
        
        field_ru_label = field_mapper.NetToGround[key].value
        field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.GROUND_ENTITY_ID)
        ground_payload[field["field_name_unified"]] = value  

    # Добавляем отдельно заголовки
    ground_payload["title"] = ground.get("name")

    return ground_payload