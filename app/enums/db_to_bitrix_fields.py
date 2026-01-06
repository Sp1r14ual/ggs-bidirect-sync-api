from aenum import Enum

class BaseEnum(Enum):
    _init_ = 'value string'

    def __str__(self):
        return self.string

    @classmethod
    def _missing_value_(cls, value):
        for member in cls:
            if member.string == value:
                return member

class HouseToObjectKSFields(Enum):
    is_to_from_sibgs = "project_to_vgdo_oao_sibirgasservice"
    is_double_adress = "double_address"
    # Адрес
    address = "address"
    #
    type_client = "client_type"
    type_house_gazification = "gasification_type"
    district = "district"
    is_ods = "ods"
    cadastr_number = "land_kadastr_number"
    cadastr_number_oks = "oks_kadastr_number"
    organization = "owners" # Как интегрировать владельцев?
    id = "id_house_osa"

class HouseToGasificationStageFields(Enum):
    # Этапы газификации
    date_project_agreement = "agreed"
    project_agreement_remark = "remark1"
    start_gas_number = "gas_launch_agreement_number"
    start_gas_date = "gas_launch_agreement_date"
    gaz_pusk_date = "gas_launch_primary_date"
    gaz_note_date = "delivery_of_notice_date"
    mrg_send_note_date = "send_to_mrg_date"
    gaz_off_date = "shutting_gas_supply_system_date"
    grs_meters = "footage"
    start_gaz_remark = "remark2"
    ptu_request_date = "application_from_ptu"
    ptu_send_date = "passed_in_pto_ptu"
    grs = "grs2"
    spdg_number_protocol = "protocol_number"
    spdg_date_protocol = "date1"
    spdg_number = "number"
    spdg_date = "date2"
    type_spdg_action = "event"
    gc_plan = "planned"
    gc_sign = "stated"
    gc_fact = "actual"
    type_packing = "pad"
    type_pipe_material = "material"
    grs_diam = "diameter"

class PersonToContactFields(Enum):
    family_name = "LAST_NAME"
    birthdate = "BIRTHDATE"
    phone_number = "PHONE"
    name = "NAME"
    patronimic_name = "SECOND_NAME"
    snils = "UF_CRM_1739334773204"

class PersonToContactRequisite(Enum):
    family_name = "RQ_LAST_NAME"
    name = "RQ_FIRST_NAME"
    patronimic_name = "RQ_SECOND_NAME"
    phone_number = "RQ_PHONE"
    pasport_serial = "RQ_IDENT_DOC_SER"
    pasport_number = "RQ_IDENT_DOC_NUM"
    pasport_date = "RQ_IDENT_DOC_DATE"
    pasport_place = "RQ_IDENT_DOC_ISSUED_BY"
    dep_code = "RQ_IDENT_DOC_DEP_CODE"
    inn = "RQ_INN"
    ogrn = "RQ_OGRN"
    email = "RQ_EMAIL"

class PersonToAddress(Enum):
    reg_adress = "ADDRESS_1"
    reg_region = "PROVINCE"
    reg_raion = "REGION"
    reg_city = "CITY"
    reg_street = ""
    reg_house = ""
    reg_flat = ""
    postal_index = "POSTAL_CODE"

class OrganizationToCompanyFields(Enum):
    name = "TITLE"
    is_pir = "UfCrm1756803695"
    is_smr_gvd_gnd = "UfCrm1756803661"
    is_to_gvd_gnd = "UfCrm1756803741"

class OrganizationToAddress(Enum):
    adress_jur = "ADDRESS_1"
    zip_code_jur = "POSTAL_CODE"
    adress_fact = "ADDRESS_1"
    zip_code_fact = "POSTAL_CODE"

class OrganizationToCompanyRequisite(Enum):
    inn = "RQ_INN"
    kpp = "RQ_KPP"
    ogrn = "RQ_OGRN"

class OrganizationToCompanyBankdetailRequisite(Enum):
    bik = "RQ_BIK"
    korr_acc = "RQ_COR_ACC_NUM"
    calc_acc = "RQ_ACC_NUM"
    bank = "RQ_BANK_NAME"

class EquipToEquip(Enum):
    packing_name = "ufCrm47_1753076112"
    # diameter = "ufCrm47_1755666805151"
    diameter_type_name = "ufCrm47_1753076284"
    length = "ufCrm47_1753076263"
    pipe_material_name = "ufCrm47_1753076229"
    amount = "ufCrm47_1753076068"
    num = "ufCrm47_1753075654"

class HouseEquipToEquip(Enum):
    equip_name = "ufCrm47_1753081361"
    type_cat_name = "ufCrm47_1753075437"
    boil_setup_name = "ufCrm47_1753075764"
    year_produce = "ufCrm47_1753075747"
    power = "ufCrm47_1753075726"
    amount = "ufCrm47_1753075654"
    du1 = "ufCrm47_1755666805151"
    du2 = "ufCrm47_1753076284"


