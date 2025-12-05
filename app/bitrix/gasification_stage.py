from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta
import app.enums.gasification_stage as GasificationStageEnums

webhook = "https://dev.ggs-nsk.ru/rest/132/sgcqlj6lfixazqh6/"
b = Bitrix(webhook)

def build_payload(gasification_stage):
    gasification_stage_to_dict = dict(gasification_stage)
    payload = {}

    for key, value in gasification_stage_to_dict.items():
        append_value = value

        # Проверяем типы значений
        if isinstance(value, bool):
            append_value = "Y" if append_value else "N"
        elif isinstance(value, (GasificationStageEnums.Event, GasificationStageEnums.Pad, GasificationStageEnums.Material)):
            append_value = value.value
        else:
            append_value = value
        
        payload[GasificationStageEnums.GasificationStageFields[key].value] = append_value
    
    return payload


def add_item(gasification_stage):
    payload = build_payload(gasification_stage)
    # payload = gasification_stage
    res = b.call('crm.item.add', {"entityTypeId": 1146, "fields": payload})
    return res

def add_item_for_db_sync(gasification_stage):
    # payload = build_payload(gasification_stage)
    payload = gasification_stage
    res = b.call('crm.item.add', {"entityTypeId": 1146, "fields": payload})
    return res

def update_item(id, gasification_stage):
    payload = build_payload(gasification_stage)
    # payload = gasification_stage
    res = b.call('crm.item.update', {"id": id, "entityTypeId": 1146, "fields": payload})
    return res

def update_item_for_db_sync(id, gasification_stage):
    # payload = build_payload(gasification_stage)
    payload = gasification_stage
    res = b.call('crm.item.update', {"id": id, "entityTypeId": 1146, "fields": payload})
    return res

def get_item(id):
    res = b.call('crm.item.get', {"id": id, "entityTypeId": 1146})
    return res

def list_items():
    res = b.call('crm.item.list', {"entityTypeId": 1146})
    return res

def delete_item(id):
    res = b.call('crm.item.delete', {"id": id, "entityTypeId": 1146})
    return res