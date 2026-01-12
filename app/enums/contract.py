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

class ContractType(BaseEnum):
    not_chosen = 0, None
    tod = 892, "Договор ТОД"

class ContractTypePrefix(BaseEnum):
    not_chosen = 0, None
    # Пустой список на стороне битрикса

# class TypeProductShortname(BaseEnum):
#     not_chosen = 0, None
#     #To-do

class ContractCategory(BaseEnum):
    not_chosen = 0, None
    tr = 533, "ТР"
    rent = 534, "Аренда"
    to = 535, "ТО"
    tp = 536, "ТП"
    cmr = 537, "СМР"
    pir = 538, "ПИР"
    third_party_services = 539, "Услуги сторонние"
    operating_costs = 540, "Расходы на эксплуатацию" 


class ContractKind(BaseEnum):
    not_chosen = 0, None
    provision_services_contract = 524, "Договор на оказание услуг"
    contract_work = 525, "Договор подряда"
    purchase_and_sale_contract = 526, "Договор купли-продажи"
    rent_contract = 527, "Договор аренды"
    loan_contract = 528, "Договор займа"
    agency_contract = 529, "Агентский договор"
    license_contract = 530, "Лицензионный договор"
    investment_contract = 531, "Инвестиционный договор"
    labour_contract = 532, "Трудовой договор"

class ContractCurrentStatus(BaseEnum):
    not_chosen = 0, None
    active = 1080, "Действует"
    expired = 1081, "Окончен"