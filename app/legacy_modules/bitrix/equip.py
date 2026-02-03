from fast_bitrix24 import Bitrix
from app.settings import settings

b = Bitrix(settings.BITRIX_WEBHOOK)

def add_item_for_db_sync(equip):
    payload = equip
    res = b.call('crm.item.add', {"entityTypeId": 1222, "fields": payload})
    return res

def update_item_for_db_sync(id, equip):
    payload = equip
    res = b.call('crm.item.update', {"id": id, "entityTypeId": 1222, "fields": payload})
    return res

