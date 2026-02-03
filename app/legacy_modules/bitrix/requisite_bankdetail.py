from fast_bitrix24 import Bitrix
from app.settings import settings

b = Bitrix(settings.BITRIX_WEBHOOK)

def add_item_for_db_sync(bankdetail_requisite):
    payload = bankdetail_requisite
    res = b.call('crm.requisite.bankdetail.add', {"fields": payload})
    return res

def update_item_for_db_sync(id, bankdetail_requisite):
    payload = bankdetail_requisite
    res = b.call('crm.requisite.bankdetail.update', {"id": id, "fields": payload})
    return res