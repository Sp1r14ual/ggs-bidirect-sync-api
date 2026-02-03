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

class ClientType(BaseEnum):
    not_chosen = 0, None
    connection_launch_only = 480, "Подключение (только пуск)"
    gasification = 481, "Газификация"
    resigning_to_vdgo = 482, "Перезаключение ТО ВДГО"


class State(BaseEnum):
    not_chosen = 0, None
    considered_delayed = 483, "предполагаемый отсроченный"
    asocial = 484, "асоциальный"
    gasificated = 485, "газифицирован"
    not_gasificated = 486, "не газифицирован"
    considered_credit = 487, "предполагаемый кредитный"
    considered_social = 488, "предполагаемый социальный"
    considered_standard = 489, "предполагаемый стандартный"
    declined_to_demolish = 490, "отключен, под снос"
    house_burnt_down = 491, "дом сгорел"
    stub = 492, "заглушка"
    undefined = 493, "не_определен"


class GasificationType(BaseEnum):
    not_chosen = 0, None
    asocial = 494, "Асоциальный"
    standard = 495, "Стандартный"
    social = 496, "Социальный"
    credit = 497, "Кредитный"
    additional_gasification = 498, "Догазификация"
    additional_gasification_snt = 929, "Догазификация СНТ"
    additional_gasification_soc = 930, "Догазификация СОЦ"


class District(BaseEnum):
    not_chosen = 0, None
    dzerjinskiy = 400, "Дзержинский"
    jeleznodorojniy = 401, "Железнодорожный"
    zaeltsovskiy = 402, "Заельцовский"
    kalininskiy = 403, "Калининский"
    kirovskiy = 404, "Кировский"
    leninskiy = 405, "Ленинский"
    novosibirskiy = 406, "Новосибирский"
    oktyabrskiy = 407, "Октябрьский"
    pervomayskiy = 408, "Первомайский"
    sovetskiy = 409, "Советский"
    centralniy = 410, "Центральный"


class Playground(BaseEnum):
    not_chosen = 0, None
    test = 1, "Тестовая"
    avleda_m = 2, "Авледа-М"
    biatlon = 3, "БИАТЛОН"
    luch_97 = 4, "ЛУЧ-97"
    zolotaya_gorka_2003 = 5, "ЗОЛОТАЯ ГОРКА 2003"
    sibirskiye_prostori = 6, "СИБИРСКИЕ ПРОСТОРЫ"


# Надо делать?
class Contract(BaseEnum):
    pass


class ObjectKSFields(Enum):
    project_to_vgdo_oao_sibirgasservice = "ufCrm10_1739508360"
    double_address = "ufCrm10_1739508394"
    address = "ufCrm10_1741160979089"
    client_type = "ufCrm10_1750848582639"
    state = "ufCrm10_1750848760947"
    gasification_type = "ufCrm10_1750848908269"
    district = "ufCrm10_1750849066"
    ods = "ufCrm10_1750849198248"
    land_kadastr_number = "ufCrm10_1750849321158"
    oks_kadastr_number = "ufCrm10_1750849334062"
    ownership_rights_registration_number = "ufCrm10_1750849352474"
    owners = "ufCrm10_1750849383"
    documents = "ufCrm10_1751252895876"
    playground = "ufCrm10_1756278171"
    id_house_osa = "ufCrm10_1756282250286"
    contracts = "ufCrm10_1758892098"
    contact_id = "contact_id"
    company_id = "company_id"
