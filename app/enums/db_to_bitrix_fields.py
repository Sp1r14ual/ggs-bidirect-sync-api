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

class OrganizationToCompanyFields(Enum):
    pass