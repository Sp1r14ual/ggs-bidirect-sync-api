from fast_bitrix24 import Bitrix
from app.settings import settings

b = Bitrix(settings.BITRIX_WEBHOOK)

def add_item_for_db_sync(address):
    payload = address
    res = b.call('crm.address.add', {"fields": payload})
    return res

def update_item_for_db_sync(address):
    payload = address
    res = b.call('crm.address.update', {"fields": payload})
    return res