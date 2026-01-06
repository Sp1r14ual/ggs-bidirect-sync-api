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
@app.get("/{id_obj}")
def test_get(id_obj: int):
    b = Bitrix(settings.BITRIX_WEBHOOK)
    return b.call('crm.item.get', {"id": id_obj, "entityTypeId": 1222})["ufCrm47_1753076450"]