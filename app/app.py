from fastapi import FastAPI
from app.routes.gasification_stage import router as gasification_stage_router
from app.routes.object_ks import router as object_ks_router


app = FastAPI()

app.include_router(gasification_stage_router)
app.include_router(object_ks_router)

@app.get("/")
def root():
    content = '''<h1>Здравствуй, мир</h1>
    <p>Документация <a href="/docs">туть</a></p>'''
    return HTMLResponse(content=content, status_code=200)