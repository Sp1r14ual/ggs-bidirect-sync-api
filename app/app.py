from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.bitrix.object_ks import add as object_ks_add_util
from app.bitrix.object_ks import update as object_ks_update_util 
from app.schemas.object_ks import AddObjectKSModel, UpdateObjectKSModel

app = FastAPI()

@app.post("/add_object_ks")
def add_object_ks_endpoint(object_ks: AddObjectKSModel):
    return object_ks_add_util(object_ks)
    # print(dict(object_ks))
    # return

@app.put("/update_object_ks")
def update_object_ks_endpoint(object_ks: UpdateObjectKSModel):
    #Добавить обработку случая "элемент не найден"
    return object_ks_update_util(object_ks)

@app.get("/get_object_ks")
def get_object_ks_endpoint():
    pass

@app.get("/list_object_ks")
def list_object_ks_endpoint():
    pass

@app.delete("/delete_object_ks")
def delete_object_ks_endpoint():
    pass

@app.get("/")
def root():
    content = '''<h1>Здравствуй, мир</h1>
    <p>Документация <a href="/docs">туть</a></p>'''
    return HTMLResponse(content=content, status_code=200)