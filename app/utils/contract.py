import app.enums.db_bitrix_fields_mapping as field_mapper
import app.db.query_crm_fields as crm_fields_db
import app.settings as settings

def build_payload_contract(contract):
    contract_payload = dict()

    for key, value in contract.items():
        if key not in field_mapper.ContractToContract.__members__ and key not in ('type_contract_prefix', 'date', 'contact_crm_id', 'company_crm_id', 'type_contract_person_category_name'):
            continue

        if key in ("type_contract_status_name", 'type_contract_name', 'type_contract_prefix', 'type_contract_status_name', 'crm_category', 'type_contract_person_category_name'):
            field = crm_fields_db.query_crm_field_by_enum_element_value(str(value), settings.settings.CONTRACT_ENTITY_ID)
            if not field:
                continue
            contract_payload[field["field_name_unified"]] = field["enum_element_id"]
            continue

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
                field_ru_label = field_mapper.ContractToContract[key].value
                field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.CONTRACT_ENTITY_ID)
                contract_payload[field["field_name_unified"]] = "C_" + str(value)
                continue
            else:
                field_ru_label = field_mapper.ContractToContract[key].value
                field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.CONTRACT_ENTITY_ID)
                contract_payload[field["field_name_unified"]] = "CO_" + str(value)
                continue

        if key in ("id_person2", "id_organization2"):
            if value is None:
                continue
            if key == "id_person2":
                field_ru_label = field_mapper.ContractToContract[key].value
                field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.CONTRACT_ENTITY_ID)
                contract_payload[field["field_name_unified"]] = "C_" + str(value)
                continue
            else:
                field_ru_label = field_mapper.ContractToContract[key].value
                field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.CONTRACT_ENTITY_ID)
                contract_payload[field["field_name_unified"]] = "CO_" + str(value)
                continue

        if key in ('contact_crm_id', 'company_crm_id'):
            if key == "contact_crm_id" and value:
                contract_payload["contactId"] = value
            elif key == "company_crm_id" and value:
                contract_payload["companyId"] = value
            continue

        if key == "date":
            field_ru_label = field_mapper.ContractToContract[key + "1"].value
            field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.CONTRACT_ENTITY_ID)
            contract_payload[field["field_name_unified"]] = value

            field_ru_label = field_mapper.ContractToContract[key + "2"].value
            field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.CONTRACT_ENTITY_ID)
            contract_payload[field["field_name_unified"]] = value
            continue

        field_ru_label = field_mapper.ContractToContract[key].value
        field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.CONTRACT_ENTITY_ID)
        contract_payload[field["field_name_unified"]] = value
    
    return contract_payload