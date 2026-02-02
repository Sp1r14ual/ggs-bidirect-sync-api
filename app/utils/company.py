import app.enums.db_bitrix_fields_mapping as field_mapper
import app.db.query_crm_fields as crm_fields_db
import app.settings as settings

def build_payload_company(organization: dict) -> (dict, int):
    company_payload = {}

    preset_id = 1

    for key, value in organization.items():
        if key not in field_mapper.OrganizationToCompanyFields.__members__:
            continue

        if key == "name" and "ИП" in value:
            preset_id = 2

        if key in ('is_pir', 'is_smr_gvd_gnd', 'is_to_gvd_gnd'):
            field_ru_label = field_mapper.OrganizationToCompanyFields[key].value
            field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.COMPANY_ENTITY_ID)
            company_payload[field["field_name_unified"]] = value
            continue

        field_name = field_mapper.OrganizationToCompanyFields[key].value
        company_payload[field_name] = value
    
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
        if key not in field_mapper.OrganizationToAddress.__members__:
            continue

        if key in ("adress_jur", "zip_code_jur"):
            bitrix_field_name = field_mapper.OrganizationToAddress[key].value
            jur_address_payload[bitrix_field_name] = value
            continue
        
        if key in ("adress_fact", "zip_code_fact"):
            bitrix_field_name = field_mapper.OrganizationToAddress[key].value
            fact_address_payload[bitrix_field_name] = value
            continue
    
    return jur_address_payload, fact_address_payload

def build_payload_company_requisite(organization, company_id, preset_id):
    requisite_payload = {"ENTITY_TYPE_ID": 4, 
                        "ENTITY_ID": company_id, 
                        "PRESET_ID": preset_id,
                        "NAME": organization["name"]}

    for key, value in organization.items():
        if key not in field_mapper.OrganizationToCompanyRequisite.__members__:
            continue

        bitrix_field_name = field_mapper.OrganizationToCompanyRequisite[key].value
        requisite_payload[bitrix_field_name] = value
    
    return requisite_payload

def build_payload_company_bankdetail_requisite(organization, requisite_id):
    bankdetail_requisite_payload = {"ENTITY_ID": requisite_id, "NAME": organization["name"]}

    for key, value in organization.items():
        if key not in field_mapper.OrganizationToCompanyBankdetailRequisite.__members__:
            continue

        bitrix_field_name = field_mapper.OrganizationToCompanyBankdetailRequisite[key].value
        bankdetail_requisite_payload[bitrix_field_name] = value
    
    return bankdetail_requisite_payload