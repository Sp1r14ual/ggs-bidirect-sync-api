from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
from app.routes.gasification_stage import router as gasification_stage_router
from app.routes.object_ks import router as object_ks_router
from app.routes.sync_with_db import router as sync_with_db_router
from app.routes.sync_with_db2 import router as sync_with_db_router2
from fast_bitrix24 import Bitrix
from app.settings import settings

app = FastAPI()

# app.include_router(gasification_stage_router)
# app.include_router(object_ks_router)
app.include_router(sync_with_db_router)
app.include_router(sync_with_db_router2)

@app.get("/")
def root():
    content = '''<h1>Здравствуй, мир</h1>
    <p>Документация <a href="/docs">туть</a></p>'''
    return HTMLResponse(content=content, status_code=200)

# Тестовый эндпоинт для получения констант enumoв из битрикса
@app.get("/get_entity/{id_entity}/{id_obj}")
def test_get_entity(id_entity: int, id_obj: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    return b.call('crm.item.get', {"id": id_obj, "entityTypeId": id_entity})
    #return b.call('crm.contact.get', {'id': id_obj})


@app.get("/get_entity_type/{id_entity}")
def get_entity_type(id_entity: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    all_types = b.get_all('crm.type.list')
    for entity in all_types:
        if entity.get('entityTypeId') == id_entity:
            return entity


@app.get("/get_list/{id_list}")
def test_get_list(id_list: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    return b.get_all('lists.element.get',
                  {'IBLOCK_TYPE_ID': 'lists',
                          'IBLOCK_ID': id_list,
                          'NAV_PARAMS': {
                            'nPageSize': 100,  # Элементов на странице
                            'iNumPage': 1     # Номер страницы
                         }
                   })

@app.get("/get_field/{entity_code}/{id_field}")
def test_get_field_info(entity_code:str, id_field: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    field_data = b.call(
                 'userfieldconfig.get',
                    { 'moduleId': 'crm',
                            'entityId': entity_code,
                            'id': id_field
                            })
    #return field_data
    return [{'field_id': field_data.get('id'),
             'entityId': field_data.get('entityId'),
             'fieldName': field_data.get('fieldName'),
             'elem_id': x.get('id'),
             'elem_value': x.get('value')} for x in field_data['enum']]


@app.get("/get_all_fields")
def test_get_all_fields():
    b = Bitrix(settings.BITRIX_WEBHOOK)
    field_data = b.get_all(
                 'userfieldconfig.list',
                   { "moduleId": "crm"}
    )
    return [{'field_id': x['id'], 'entityId': x['entityId'], 'fieldName':  x['fieldName']} for x in field_data if x['userTypeId'] == 'enumeration']
