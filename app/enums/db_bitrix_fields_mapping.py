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