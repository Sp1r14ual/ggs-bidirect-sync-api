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

@router.get("/get_entity/{id_entity}/{id_obj}")
def get_entity(id_entity: int, id_obj: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    return b.call('crm.item.get', {"id": id_obj, "entityTypeId": id_entity})


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

# @router.get("/get_enum_field_info/{entity_id}/{field_id}")
# def get_enum_field_info(entity_id: str, field_id: int):
#     b = Bitrix(settings.BITRIX_WEBHOOK)
#     field_data = b.call(
#                  'userfieldconfig.get',
#                     { 'moduleId': 'crm',
#                             'entityId': entity_id,
#                             'id': field_id
#                             })
#     return [{'field_id': field_data.get('id'),
#              'entityId': field_data.get('entityId'),
#              'fieldName': field_data.get('fieldName'),
#              'elem_id': x.get('id'),
#              'elem_value': x.get('value')} for x in field_data['enum']]

@router.get("/get_field_info_by_id/{id}")
def get_field_info_by_id(id: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    field_data = b.call(
                 'userfieldconfig.get',
                   { "moduleId": "crm", "id": id}
    )

    return field_data

@router.get("/get_all_fields")
def get_all_fields():
    b = Bitrix(settings.BITRIX_WEBHOOK)
    field_data = b.get_all(
                 'userfieldconfig.list',
                   { "moduleId": "crm", "select": ['*']}
    )

    return field_data

# @router.get("/get_all_enum_fields")
# def get_all_enum_fields():
#     b = Bitrix(settings.BITRIX_WEBHOOK)
#     field_data = b.get_all(
#                  'userfieldconfig.list',
#                    { "moduleId": "crm"}
#     )

#     return [{'field_id': x['id'], 'entityId': x['entityId'], 'fieldName':  x['fieldName'], 'userTypeId': x['userTypeId']} for x in field_data if x['userTypeId'] == 'enumeration']

# @router.get("/get_all_iblock_element_fields")
# def get_all_iblock_element_fields():
#     b = Bitrix(settings.BITRIX_WEBHOOK)
#     field_data = b.get_all(
#                  'userfieldconfig.list',
#                    { "moduleId": "crm"}
#     )

#     # return field_data
#     return [{'field_id': x['id'], 'entityId': x['entityId'], 'fieldName':  x['fieldName'], 'userTypeId': x['userTypeId'], 'iblock_id': x["settings"]["IBLOCK_ID"]} for x in field_data if x['userTypeId'] == 'iblock_element']

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

@router.post("/build_table_crm_fields")
def sync_crm_fields_with_db():
    rows: list = []

    create_crm_fields_table()

    all_fields = get_all_fields()

    

    #Обработка enum-ов
    try:
        for field in all_fields:
            field_id: int = field.get("id")
            user_type_id: str = field.get("userTypeId")
            entity_id: str = field.get("entityId")
            field_name: str = field.get("fieldName")

            # Если у поля тип enum
            if user_type_id == "enumeration":
                general_field_info: dict = get_field_info_by_id(id=field_id)
                for enum_info in general_field_info.get("enum", []):
                    crm_field = CrmFields(
                        field_id=field_id,
                        user_type_id=user_type_id,
                        entity_id=entity_id,
                        field_label_ru=general_field_info.get("editFormLabel").get("ru"),
                        field_label_en=general_field_info.get("editFormLabel").get("en"),
                        field_name=field_name,
                        field_name_unified = unify_field_name(field_name),
                        enum_element_id=enum_info.get("id"),
                        enum_element_value=enum_info.get("value")
                    )
                    crm_field.is_prod = 0 if settings.RUN_MODE == "DEV" else 1
                    rows.append(crm_field)
            
            # Если у поля тип инфоблок
            elif user_type_id == "iblock_element":
                iblock_id: int = field["settings"].get("IBLOCK_ID")
                iblock_element_field_info: list = get_iblock_info(iblock_id=iblock_id)
                general_field_info: dict = get_field_info_by_id(id=field_id)

                for iblock_info in iblock_element_field_info:
                    crm_field = CrmFields(
                        field_id=field_id,
                        user_type_id=user_type_id,
                        entity_id=entity_id,
                        iblock_id=iblock_info.get("IBLOCK_ID"),
                        field_label_ru=general_field_info.get("editFormLabel").get("ru"),
                        field_label_en=general_field_info.get("editFormLabel").get("en"),
                        field_name=field_name,
                        field_name_unified=unify_field_name(field_name),
                        iblock_element_id=iblock_info.get("ID"),
                        iblock_element_value=iblock_info.get("NAME")
                    )
                    crm_field.is_prod = 0 if settings.RUN_MODE == "DEV" else 1
                    rows.append(crm_field)

            else:
                general_field_info: dict = get_field_info_by_id(id=field_id)
                crm_field = CrmFields(
                        field_id=field_id,
                        user_type_id=user_type_id,
                        entity_id=entity_id,
                        field_label_ru=general_field_info.get("editFormLabel").get("ru"),
                        field_label_en=general_field_info.get("editFormLabel").get("en"),
                        field_name=field_name,
                        field_name_unified=unify_field_name(field_name)
                    )
                crm_field.is_prod = 0 if settings.RUN_MODE == "DEV" else 1
                rows.append(crm_field)
    
    except Exception as e:
        return {
            "field": general_field_info,
            "err": str(e)
        }
    

    fill_info_crm_fields_table(rows)

    return {"result": "OK"}

