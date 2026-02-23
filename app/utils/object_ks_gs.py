import app.enums.db_bitrix_fields_mapping as field_mapper
import app.db.query_crm_fields as crm_fields_db
import app.settings as settings

def get_bool_value(value):
    return "Y" if bool(value) else "N"

def address_builder(components: dict) -> str:
    postal_index = components.get("postal_index")
    town = components.get("town")
    street = components.get("street")
    house_number = components.get("house_number")
    corpus_number = components.get("corpus_number")
    flat_number = components.get("flat_number")
    return ", ".join(map(str, [postal_index, town, street, house_number, corpus_number, flat_number]))

def build_payloads_object_ks_gs(house):

    object_ks_payload = dict()
    gasification_stage_payload = dict()

    # Ставим плейсхолдер для адреса
    object_ks_payload["address"] = None

    for key, value in house.items():
        if key in ("postal_index", "town", "street", "house_number", "corpus_number", "flat_number",
        "object_ks_crm_id", "gasification_stage_crm_id", "id_net", "contract_id", "contract_crm_id"):
            continue

        if key in ("is_to_from_sibgs", "is_double_adress", "is_ods"):
            field_ru_label = field_mapper.HouseToObjectKSFields[key].value
            field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.OBJECT_KS_ENTITY_ID)
            object_ks_payload[field["field_name_unified"]] = get_bool_value(value)
            continue

        if key == "district":
            field = crm_fields_db.query_crm_field_by_iblock_element_value(value, settings.settings.OBJECT_KS_ENTITY_ID)
            if not field:
                continue
            object_ks_payload[field["field_name_unified"]] = field["iblock_element_id"]
            continue

        if key in ('id', 'ground_crm_id', "cadastr_number", "cadastr_number_oks"):
            field_ru_label = field_mapper.HouseToObjectKSFields[key].value
            field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.OBJECT_KS_ENTITY_ID)
            object_ks_payload[field["field_name_unified"]] = value
            continue

        if key in ('type_client', 'type_house_gazification'):
            # field_ru_label = field_mapper.HouseToObjectKSFields[key].value
            field = crm_fields_db.query_crm_field_by_enum_element_value(value, settings.settings.OBJECT_KS_ENTITY_ID)
            if not field:
                continue
            object_ks_payload[field["field_name_unified"]] = field["enum_element_id"]
            continue

        if key in ('grs', 'type_packing', 'type_pipe_material', 'type_spdg_action'):
            # field_ru_label = field_mapper.HouseToGasificationStageFields[key].value
            field = crm_fields_db.query_crm_field_by_enum_element_value(value, settings.settings.GASIFICATION_STAGE_ENTITY_ID)
            if not field:
                continue
            gasification_stage_payload[field["field_name_unified"]] = field["enum_element_id"]
            continue

        if key == "address":
            field_ru_label = field_mapper.HouseToObjectKSFields[key].value
            field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.OBJECT_KS_ENTITY_ID)
            address = address_builder(house)
            object_ks_payload[field["field_name_unified"]] = address
            continue

        if key in ('contact_id', 'company_id'):
            if key == "contact_id":
                object_ks_payload["contactId"] = value
                gasification_stage_payload["contactId"] = value
            else:
                object_ks_payload["companyId"] = value
                gasification_stage_payload["companyId"] = value
            continue

        field_ru_label = field_mapper.HouseToGasificationStageFields[key].value
        field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.GASIFICATION_STAGE_ENTITY_ID)
        gasification_stage_payload[field["field_name_unified"]] = value

    # Добавляем отдельно заголовки
    object_ks_payload["title"] = f"Объект КС, house_id: {house["id"]}" # Не дает записать в заголовок ничего кроме адреса
    gasification_stage_payload["title"] = f"Этап газификации, house_id: {house["id"]}"
    
    return object_ks_payload, gasification_stage_payload