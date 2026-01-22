from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fast_bitrix24 import Bitrix
from app.settings import settings
from app.db.query_crm_fields import create_crm_fields_table
from app.models.crm_fields import CrmFields
from app.db.query_crm_fields import fill_info_crm_fields_table

router = APIRouter(prefix="/admin_tasks", tags=["admin_tasks"])

# Тестовый эндпоинт для получения констант enumoв из битрикса
@router.get("/get_entity/{id_entity}/{id_obj}")
def get_entity(id_entity: int, id_obj: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    return b.call('crm.item.get', {"id": id_obj, "entityTypeId": id_entity})
    #return b.call('crm.contact.get', {'id': id_obj})


@router.get("/get_entity_type/{id_entity}")
def get_entity_type(id_entity: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    all_types = b.get_all('crm.type.list')
    for entity in all_types:
        if entity.get('entityTypeId') == id_entity:
            return entity


@router.get("/get_list/{id_list}")
def get_list(id_list: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    return b.get_all('lists.element.get',
                  {'IBLOCK_TYPE_ID': 'lists',
                          'IBLOCK_ID': id_list,
                          'NAV_PARAMS': {
                            'nPageSize': 100,  # Элементов на странице
                            'iNumPage': 1     # Номер страницы
                         }
                   })

@router.get("/get_field/{entity_id}/{field_id}")
def get_field_info(entity_id: str, field_id: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    field_data = b.call(
                 'userfieldconfig.get',
                    { 'moduleId': 'crm',
                            'entityId': entity_id,
                            'id': field_id
                            })
    #return field_data
    return [{'field_id': field_data.get('id'),
             'entityId': field_data.get('entityId'),
             'fieldName': field_data.get('fieldName'),
             'elem_id': x.get('id'),
             'elem_value': x.get('value')} for x in field_data['enum']]


@router.get("/get_all_enum_fields")
def get_all_enum_fields():
    b = Bitrix(settings.BITRIX_WEBHOOK)
    field_data = b.get_all(
                 'userfieldconfig.list',
                   { "moduleId": "crm"}
    )

    return [{'field_id': x['id'], 'entityId': x['entityId'], 'fieldName':  x['fieldName']} for x in field_data if x['userTypeId'] == 'enumeration']

def unify_field_name(s: str) -> str:
    if not s:
        return s
    
    parts = s.split('_')
    
    if len(parts) < 3:
        return s.lower()
    
    # Обрабатываем первую часть (префикс)
    result = parts[0].lower()
    
    # Обрабатываем средние части (те, что до последней части)
    for part in parts[1:-1]:
        if part:  # Проверяем, что часть не пустая
            # Делаем первую букву заглавной, остальные - строчными
            result += part[0].upper() + part[1:].lower()
    
    # Добавляем последнюю часть с разделителем '_'
    result += '_' + parts[-1]
    
    return result

@router.get("/sync_crm_fields_with_db")
def sync_crm_fields_with_db():
    rows: list = []

    create_crm_fields_table()

    fields: list = get_all_enum_fields()

    for field in fields:
        field_id: int = field.get("field_id")
        entity_id: str = field.get("entityId")
        field_name: str = field.get("fieldName")
        field_info: list = get_field_info(entity_id=entity_id, field_id=field_id)
        for info in field_info:
            crm_field = CrmFields(
                field_id=info.get("field_id"),
                entity_id=info.get("entityId"),
                field_name=info.get("fieldName"),
                field_name_unified = unify_field_name(info.get("fieldName")),
                elem_id=info.get("elem_id"),
                elem_value=info.get("elem_value")
            )
            if settings.RUN_MODE == "DEV":
                crm_field.is_prod = 0
            else:
                crm_field.is_prod = 1

            rows.append(crm_field)

    fill_info_crm_fields_table(rows)

    return {"result": "OK"}

