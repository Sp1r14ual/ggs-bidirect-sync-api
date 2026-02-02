from fast_bitrix24 import Bitrix
from app.settings import settings

b = Bitrix(settings.BITRIX_WEBHOOK)

def add_item(entity_type_id: int, payload: dict):
    res = b.call('crm.item.add', {"entityTypeId": entity_type_id, "fields": payload})
    return res

def update_item(id: int, entity_type_id: int, payload: dict):
    res = b.call('crm.item.update', {"id": id, "entityTypeId": entity_type_id, "fields": payload})
    return res

def add_contact(payload):
    res = b.call('crm.contact.add', {"fields": payload})
    return res

def update_contact(id, payload):
    res = b.call('crm.contact.update', {"id": id, "fields": payload})
    return res

def add_requisite(payload):
    res = b.call('crm.requisite.add', {"fields": payload})
    return res

def update_requisite(id, payload):
    res = b.call('crm.requisite.update', {"id": id, "fields": payload})
    return res

def add_address(payload):
    res = b.call('crm.address.add', {"fields": payload})
    return res

def update_address(payload):
    res = b.call('crm.address.update', {"fields": payload})
    return res