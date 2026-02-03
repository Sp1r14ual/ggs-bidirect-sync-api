from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
from app.routes.gasification_stage import router as gasification_stage_router
from app.routes.object_ks import router as object_ks_router
from app.routes.forward_sync import router as forward_sync_router
from app.routes.admin_tasks import router as admin_tasks_router
from fast_bitrix24 import Bitrix
from app.settings import settings

app = FastAPI()

# app.include_router(gasification_stage_router)
# app.include_router(object_ks_router)
app.include_router(forward_sync_router)
app.include_router(admin_tasks_router)

@app.get("/")
def root():
    content = '''<h1>Здравствуй, мир</h1>
    <p>Документация <a href="/docs">туть</a></p>'''
    return HTMLResponse(content=content, status_code=200)