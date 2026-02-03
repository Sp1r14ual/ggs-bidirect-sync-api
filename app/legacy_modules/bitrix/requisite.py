from fast_bitrix24 import Bitrix
from app.settings import settings

b = Bitrix(settings.BITRIX_WEBHOOK)

def add_item_for_db_sync(requisite):
    payload = requisite
    res = b.call('crm.requisite.add', {"fields": payload})
    return res

def update_item_for_db_sync(id, requisite):
    payload = requisite
    res = b.call('crm.requisite.update', {"id": id, "fields": payload})
    return res