from fast_bitrix24 import Bitrix

webhook = "https://dev.ggs-nsk.ru/rest/132/sgcqlj6lfixazqh6/"
b = Bitrix(webhook)

def add_item_for_db_sync(address):
    payload = address
    res = b.call('crm.address.add', {"fields": payload})
    return res