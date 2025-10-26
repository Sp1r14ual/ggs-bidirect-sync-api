from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bitrix.object_ks import add as object_ks_add_util

app = FastAPI()

@app.post("/add_object_ks")
def add_object_ks_endpoint():
    return object_ks_add_util()

@app.put("/update_object_ks")
def update_object_ks_endpoint():
    pass

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