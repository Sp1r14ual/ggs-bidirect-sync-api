from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta
import app.enums.object_ks_enums as ObjectKSEnums

webhook = "https://dev.ggs-nsk.ru/rest/118/xb10aqz3kexdtxlm/"
b = Bitrix(webhook)

def build_payload(object_ks):
    object_ks_to_dict = dict(object_ks)
    payload = {}

    for key, value in object_ks_to_dict.items():
        append_value = value

        # Проверяем типы значений
        if isinstance(value, bool):
            append_value = "Y" if append_value else "N"
        elif isinstance(value, (ObjectKSEnums.ClientType2, ObjectKSEnums.State2, ObjectKSEnums.GasificationType2, 
        ObjectKSEnums.District, ObjectKSEnums.Event, ObjectKSEnums.Pad, ObjectKSEnums.Material, ObjectKSEnums.Manager)):
            append_value = value.value
        else:
            append_value = value
        
        payload[ObjectKSEnums.ObjectKSFields[key].value] = append_value
    
    return payload



def add(object_ks):
    payload = build_payload(object_ks)
    res = b.call('crm.item.add', {"entityTypeId": 1066, "fields": payload})
    return res

def update(id, object_ks):
    payload = build_payload(object_ks)
    res = b.call('crm.item.update', {"id": id, "entityTypeId": 1066, "fields": payload})
    return res

def get(id):
    res = b.call('crm.item.get', {"id": id, "entityTypeId": 1066})
    return res

def list():
    res = b.call('crm.item.list', {"entityTypeId": 1066})
    return res

def delete(id):
    res = b.call('crm.item.delete', {"id": id, "entityTypeId": 1066})
    return res