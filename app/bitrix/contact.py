from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta

webhook = "https://dev.ggs-nsk.ru/rest/132/sgcqlj6lfixazqh6/"
b = Bitrix(webhook)

def add_item_for_db_sync(contact):
    payload = contact
    res = b.call('crm.contact.add', {"fields": payload})
    return res