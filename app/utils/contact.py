import app.enums.db_bitrix_fields_mapping as field_mapper
import app.db.query_crm_fields as crm_fields_db
import app.settings as settings

def build_payload_contact(person):
    contact_payload = {}

    for key, value in person.items():
        if key not in field_mapper.PersonToContactFields.__members__:
            continue

        if key == 'snils':
            field_ru_label = field_mapper.PersonToContactFields[key].value
            field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.CONTACT_ENTITY_ID)
            contact_payload[field["field_name_unified"]] = value
            continue

        field_name = field_mapper.PersonToContactFields[key].value
        contact_payload[field_name] = value
    
    return contact_payload

def build_payload_contact_requisite(person, contact_id):
    requisite_payload = {"ENTITY_TYPE_ID": 3, 
                        "ENTITY_ID": contact_id, 
                        "PRESET_ID": 3,
                        "NAME": " ".join([person["family_name"], person["name"], person["patronimic_name"]])}

    for key, value in person.items():
        if key not in field_mapper.PersonToContactRequisite.__members__:
            continue

        field_name = field_mapper.PersonToContactRequisite[key].value
        requisite_payload[field_name] = value
    
    return requisite_payload

def build_payload_contact_address(person, requisite_id):
    address_payload = {
        "TYPE_ID": 4, # Адрес регистраци
        "ENTITY_TYPE_ID": 8, # Реквизиты
        "ENTITY_ID": requisite_id
    }

    ADDRESS_2 = ""

    for key, value in person.items():
        if key not in field_mapper.PersonToAddress.__members__:
            continue
        
        # Надо ли отдельно выделять этот блок?
        # Убрать
        # if key == "reg_address":
        #     field_name = field_mapper.PersonToAddress[key].value
        #     address_payload[field_name] = value
        #     continue

        if key in ("reg_street", "reg_house", "reg_flat"):
            ADDRESS_2 += str(value) + ", "
            continue

        field_name = field_mapper.PersonToAddress[key].value
        address_payload[field_name] = value

    address_payload["ADDRESS_2"] = ADDRESS_2
    
    return address_payload