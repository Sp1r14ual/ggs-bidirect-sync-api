from fast_bitrix24 import Bitrix
from pprint import pprint

webhook = "https://dev.ggs-nsk.ru/rest/132/sgcqlj6lfixazqh6/"
b = Bitrix(webhook)

# def add_crm_company(params: dict = {"TITLE": "ИП Тестов", "COMPANY_TYPE": "CUSTOMER", "CURRENCY_ID": "RUB", "REVENUE": 3000000}):
#     b.call('crm.company.add', {"fields": params})


# add_crm_company()

# res = b.call('crm.lead.list', {"select": ["*"], "filter": {"PHONE": "79133747598"}})
res = b.call('crm.lead.get', {"id": 2995})
pprint(res)