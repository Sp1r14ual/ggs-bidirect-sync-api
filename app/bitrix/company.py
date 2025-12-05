from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta

webhook = "https://dev.ggs-nsk.ru/rest/132/sgcqlj6lfixazqh6/"
b = Bitrix(webhook)

def add_item_for_db_sync(company):
    payload = company
    res = b.call('crm.company.add', {"fields": payload})
    return res

def update_item_for_db_sync(id, company):
    payload = company
    res = b.call('crm.company.update', {"id": id, "fields": payload})
    return res