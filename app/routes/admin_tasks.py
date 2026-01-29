from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fast_bitrix24 import Bitrix
from app.settings import settings
from app.db.query_crm_fields import create_crm_fields_table
from app.models.crm_fields import CrmFields
from app.db.query_crm_fields import fill_info_crm_fields_table

router = APIRouter(prefix="/admin_tasks", tags=["admin_tasks"])

@router.get("/get_contact/{id_obj}")
def get_contact(id_obj: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    return b.call('crm.contact.get', {'id': id_obj})

@router.get("/get_company/{id_obj}")
def get_company(id_obj: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    return b.call('crm.company.get', {'id': id_obj})

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


@router.get("/get_iblock_info/{iblock_id}")
def get_iblock_info(iblock_id: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    return b.get_all('lists.element.get',
                  {'IBLOCK_TYPE_ID': 'lists',
                          'IBLOCK_ID': iblock_id,
                          'NAV_PARAMS': {
                            'nPageSize': 100,  # Элементов на странице
                            'iNumPage': 1     # Номер страницы
                         }
                   })

@router.get("/get_enum_field_info/{entity_id}/{field_id}")
def get_enum_field_info(entity_id: str, field_id: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    field_data = b.call(
                 'userfieldconfig.get',
                    { 'moduleId': 'crm',
                            'entityId': entity_id,
                            'id': field_id
                            })
    # return field_data
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

    # return field_data
    return [{'field_id': x['id'], 'entityId': x['entityId'], 'fieldName':  x['fieldName'], 'userTypeId': x['userTypeId']} for x in field_data if x['userTypeId'] == 'enumeration']

@router.get("/get_all_iblock_element_fields")
def get_all_iblock_element_fields():
    b = Bitrix(settings.BITRIX_WEBHOOK)
    field_data = b.get_all(
                 'userfieldconfig.list',
                   { "moduleId": "crm"}
    )

    # return field_data
    return [{'field_id': x['id'], 'entityId': x['entityId'], 'fieldName':  x['fieldName'], 'userTypeId': x['userTypeId'], 'iblock_id': x["settings"]["IBLOCK_ID"]} for x in field_data if x['userTypeId'] == 'iblock_element']

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

    enum_fields: list = get_all_enum_fields()
    iblock_element_fields: list = get_all_iblock_element_fields()

    #Обработка enum-ов
    for field in enum_fields:
        field_id: int = field.get("field_id")
        user_type_id: str = field.get("userTypeId")
        entity_id: str = field.get("entityId")
        field_name: str = field.get("fieldName")
        enum_field_info: list = get_enum_field_info(entity_id=entity_id, field_id=field_id)
        for info in enum_field_info:
            crm_field = CrmFields(
                field_id=info.get("field_id"),
                user_type_id=user_type_id,
                entity_id=info.get("entityId"),
                field_name=info.get("fieldName"),
                field_name_unified = unify_field_name(info.get("fieldName")),
                elem_id=info.get("elem_id"),
                elem_value=info.get("elem_value")
            )
            crm_field.is_prod = 0 if settings.RUN_MODE == "DEV" else 1
            rows.append(crm_field)

    for iblock_field in iblock_element_fields:
        field_id: int = iblock_field.get("field_id")
        user_type_id: str = iblock_field.get("userTypeId")
        entity_id: str = iblock_field.get("entityId")
        field_name: str = iblock_field.get("fieldName")
        iblock_id: int = iblock_field.get("iblock_id")
        iblock_element_field_info: list = get_iblock_info(iblock_id=iblock_id)

        for iblock_info in iblock_element_field_info:
            crm_field = CrmFields(
                field_id=field_id,
                user_type_id=user_type_id,
                entity_id=entity_id,
                iblock_id=iblock_info.get("IBLOCK_ID"),
                field_name=field_name,
                field_name_unified=unify_field_name(field_name),
                elem_id=iblock_info.get("ID"),
                elem_value=iblock_info.get("NAME")
            )
            crm_field.is_prod = 0 if settings.RUN_MODE == "DEV" else 1
            rows.append(crm_field)
    

    fill_info_crm_fields_table(rows)

    return {"result": "OK"}

