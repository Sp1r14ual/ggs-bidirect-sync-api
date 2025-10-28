from fast_bitrix24 import Bitrix

webhook = "https://10.0.80.130/rest/118/omaq6z2w849swei4"
# webhook = 'https://b24-m3at2v.bitrix24.ru/rest/1/dg5ac7u1087jr8fu/'
b = Bitrix(webhook)

# def add_crm_company(params: dict = {"TITLE": "ИП Тестов", "COMPANY_TYPE": "CUSTOMER", "CURRENCY_ID": "RUB", "REVENUE": 3000000}):
#     b.call('crm.company.add', {"fields": params})


# add_crm_company()

res = b.call('crm.company.list', {"select": ["*"], "filter": {}})
print(res)