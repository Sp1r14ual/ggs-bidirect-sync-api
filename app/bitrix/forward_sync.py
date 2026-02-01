from fast_bitrix24 import Bitrix
from app.settings import settings

b = Bitrix(settings.BITRIX_WEBHOOK)

def add_item(entity_type_id: int, payload: dict):
    res = b.call('crm.item.add', {"entityTypeId": entity_type_id, "fields": payload})
    return res

def update_item(id: int, entity_type_id: int, payload: dict):
    res = b.call('crm.item.update', {"id": id, "entityTypeId": entity_type_id, "fields": payload})
    return res

