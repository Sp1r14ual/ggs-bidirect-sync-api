from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.bitrix.object_ks import add_item as object_ks_add_util
from app.bitrix.object_ks import update_item as object_ks_update_util
from app.bitrix.object_ks import get_item as object_ks_get_util
from app.bitrix.object_ks import list_items as object_ks_list_util
from app.bitrix.object_ks import delete_item as object_ks_delete_util
from app.schemas.object_ks import AddObjectKSModel, UpdateObjectKSModel, GetObjectKSModel

app = FastAPI()

@app.post("/add_object_ks")
def add_object_ks_endpoint(object_ks: AddObjectKSModel):
    return object_ks_add_util(object_ks)

@app.put("/update_object_ks/{id}")
def update_object_ks_endpoint(id: int, object_ks: UpdateObjectKSModel):
    try:
        res = object_ks_update_util(id, object_ks)
    except: 
        raise HTTPException(status_code=400, detail="Item does not exist")
    
    return res

@app.get("/get_object_ks/{id}")
def get_object_ks_endpoint(id: int):
    try:
        res = object_ks_get_util(id)
    except:
        raise HTTPException(status_code=400, detail="Item does not exist")
    
    return res

@app.get("/list_object_ks")
def list_object_ks_endpoint():
    #кастомизировать под выбор полей (select) и фильтрацию (filter)
    #Не хочет выгружать весь список, выгружает только первый элемент при дефолтных параметрах
    return object_ks_list_util()

@app.delete("/delete_object_ks/{id}")
def delete_object_ks_endpoint(id: int):
    try:
        res = object_ks_delete_util(id)
    except:
        raise HTTPException(status_code=400, detail="Item does not exist")
    
    return res

@app.get("/")
def root():
    content = '''<h1>Здравствуй, мир</h1>
    <p>Документация <a href="/docs">туть</a></p>'''
    return HTMLResponse(content=content, status_code=200)