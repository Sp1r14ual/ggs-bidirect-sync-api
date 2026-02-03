from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta
from app.settings import settings

b = Bitrix(settings.BITRIX_WEBHOOK)

def add_item_for_db_sync(company):
    payload = company
    res = b.call('crm.company.add', {"fields": payload})
    return res

def update_item_for_db_sync(id, company):
    payload = company
    res = b.call('crm.company.update', {"id": id, "fields": payload})
    return res