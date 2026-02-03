from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta
from app.settings import settings

b = Bitrix(settings.BITRIX_WEBHOOK)

def add_item_for_db_sync(contact):
    payload = contact
    res = b.call('crm.contact.add', {"fields": payload})
    return res

def update_item_for_db_sync(id, contact):
    payload = contact
    res = b.call('crm.contact.update', {"id": id, "fields": payload})
    return res