from fast_bitrix24 import Bitrix

webhook = "https://dev.ggs-nsk.ru/rest/132/sgcqlj6lfixazqh6/"
b = Bitrix(webhook)

def add_item_for_db_sync(bankdetail_requisite):
    payload = bankdetail_requisite
    res = b.call('crm.requisite.bankdetail.add', {"fields": payload})
    return res