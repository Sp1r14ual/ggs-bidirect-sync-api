from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.bitrix.gasification_stage import add_item as gasification_stage_add_util
from app.bitrix.gasification_stage import update_item as gasification_stage_update_util
from app.bitrix.gasification_stage import get_item as gasification_stage_get_util
from app.bitrix.gasification_stage import list_items as gasification_stage_list_util
from app.bitrix.gasification_stage import delete_item as gasification_stage_delete_util
from app.schemas.gasification_stage import AddGasificationStageModel, UpdateGasificationStageModel

router = APIRouter(prefix="/gasification_stage", tags=["gasification_stage"])

@router.post("/add")
def add_gasification_stage_endpoint(gasification_stage: AddGasificationStageModel):
    return gasification_stage_add_util(gasification_stage)

@router.put("/update/{id}")
def update_gasification_stage_endpoint(id: int, gasification_stage: UpdateGasificationStageModel):
    try:
        res = gasification_stage_update_util(id, object_ks)
    except: 
        raise HTTPException(status_code=400, detail="Item does not exist")

@router.get("/get/{id}")
def get_gasification_stage_endpoint(id: int):
    try:
        res = gasification_stage_get_util(id)
    except:
        raise HTTPException(status_code=400, detail="Item does not exist")
    
    return res

@router.get("/list")
def list_gasification_stage_endpoint():
    #кастомизировать под выбор полей (select) и фильтрацию (filter)
    #Не хочет выгружать весь список, выгружает только первый элемент при дефолтных параметрах
    return gasification_stage_list_util()

@router.delete("/delete/{id}")
def delete_gasification_stage_endpoint(id: int):
    try:
        res = gasification_stage_delete_util(id)
    except:
        raise HTTPException(status_code=400, detail="Item does not exist")
    
    return res