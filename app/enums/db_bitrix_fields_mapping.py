from enum import Enum

class HouseToObjectKSFields(Enum):
    is_to_from_sibgs = "Проект ТО ВДГО ОАО 'Сибирьгазсервис'"
    is_double_adress = "Двойной адрес"
    # Адрес
    address = "Адрес"
    #
    type_client = "Тип клиента"
    type_house_gazification = "Тип газификации"
    district = "Район"
    is_ods = "ОДС"
    cadastr_number = "Кадастровый номер земельного участка"
    cadastr_number_oks = "Кадастровый номер ОКС"
    contact_id = "Владельцы"
    company_id = "Владельцы"
    id = "ID Домовладения в ОСА"
    ground_crm_id = "Площадка"

class HouseToGasificationStageFields(Enum):
    # Этапы газификации
    date_project_agreement = "Согласовано"
    project_agreement_remark = " примечание:"
    start_gas_number = "Договор о пуске газа№"
    start_gas_date = "Дата договора о пуске газа"
    gaz_pusk_date = "Первичная дата пуска газа:"
    gaz_note_date = "Дата вручения уведомления:"
    mrg_send_note_date = "Дата отправки в МРГ:"
    gaz_off_date = "Дата отключения от системы газоснабжения:"
    grs_meters = "метраж:"
    start_gaz_remark = "Примечание"
    ptu_request_date = "Заявление от (ПТУ)"
    ptu_send_date = "Передано в ПТО (ПТУ)"
    grs = "ГРС"
    spdg_number_protocol = "Номер протокола"
    spdg_date_protocol = "дата"
    spdg_number = "номер"
    spdg_date = "дата"
    type_spdg_action = "Мероп.:"
    gc_plan = "плановое:"
    gc_sign = "заявленное:"
    gc_fact = "фактическое:"
    type_packing = "прокладка:"
    type_pipe_material = "материал:"
    grs_diam = "диаметр:"

class PersonToContactFields(Enum):
    family_name = "LAST_NAME"
    birthdate = "BIRTHDATE"
    phone_number = "PHONE"
    name = "NAME"
    patronimic_name = "SECOND_NAME"
    snils = "СНИЛС"

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
    is_pir = "ПИР"
    is_smr_gvd_gnd = "СМР"
    is_to_gvd_gnd = "ГПО" # Точно ли так?

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
    packing_name = "Тип прокладки"
    # diameter = "ufCrm47_1755666805151"
    diameter_type_name = "ДУ"
    length = "Протяженность, м"
    pipe_material_name = "Материал труб"
    amount = "Кол-во, шт"

class HouseEquipToEquip(Enum):
    equip_name = "Марка"
    type_cat_name = "Тип оборудования"
    boil_setup_name = "Тип установки"
    type_boil_classification_name = "Тип камеры сгорания"
    year_produce = "Месяц, год выпуска"
    power = "Мощность, кВт"
    amount = "Кол-во, шт"
    du1 = "Диаметр"
    du2 = "ДУ"
    meters = "Протяженность, м"
    pg = "Тип плиты / варочной панели"

class ContractToContract(Enum):
    type_contract_name = "Тип:"
    date1 = "Дата заключения договора"
    finish = "Действует до"
    start = "Действует с"
    summ = "Сумма"
    number = "№"
    date2 = "Дата"
    remark = "Примечание"
    type_contract_status_name = "Текущее состояние"
    type_product_name = "Зарегистрировать"
    type_contract_prefix = "Префикс"
    act_signed = "Дата подписания договора"
    id_person1 = "Исполнитель/Продавец"
    id_organization1 = "Исполнитель/Продавец"
    id_person2 = "Заказчик/Покупатель"
    id_organization2 = "Заказчик/Покупатель"
    subject = "Предмет договора"
    contract_category_name = "Вид договора"
    crm_category = "Категория"

class NetToGround(Enum):
    sys_old = "Код"
    name = "Псевдоним"
    gro_name = "ГРО"
    town_name = "Нас.пункт"
    status_name = "Статус"
    houses_cnt = "Объектов (число)"
    consumer_type_name = "Тип потребителя"
    district_name  = "Район"
    remark = "Примечание"