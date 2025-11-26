from datetime import date
from typing import Optional
from pydantic import BaseModel
import app.enums.gasification_stage as GasificationStageEnums

class GasificationStageModel(BaseModel):
    agreed: Optional[date] = date.today()
    remark1: Optional[str] = "remark1"
    grs: Optional[int] = 2995 #Lead id
    gas_launch_agreement_number: Optional[str] = "342432424"
    gas_launch_agreement_date: Optional[date] = date.today()
    gas_launch_primary_date: Optional[date] = date.today()
    delivery_of_notice_date: Optional[date] = date.today()
    send_to_mrg_date: Optional[date] = date.today()
    shutting_gas_supply_system_date: Optional[date] = date.today()
    request: Optional[date] = date.today()
    footage: Optional[int] = 1983213
    remark2: Optional[str] = "remark2"
    application_from_ptu: Optional[date] = date.today()
    passed_in_pto_ptu: Optional[date] = date.today()
    received_technical_condition_ptu: Optional[str] = "tralala"
    number_ptu: Optional[str] = "2138493214"
    date_ptu: Optional[date] = date.today()
    number_tu: Optional[str] = "098432574325"
    date_tu: Optional[str] = date.today()
    grs2: Optional[int] = 937
    object_code: Optional[str] = "435894"
    passed_in_pto: Optional[date] = date.today()
    received_technical_condition: Optional[str] = "bimbimbimbambambam"
    protocol_number: Optional[str] = "12321321"
    date1: Optional[date] = date.today()
    number: Optional[str] = "1823498213984"
    date2: Optional[date] = date.today()
    event: Optional[GasificationStageEnums.Event] = 560
    due_date: Optional[date] = date.today()
    reschedule_date: Optional[date] = date.today()
    application_from: Optional[date] = date.today()
    date3: Optional[date] = date.today()
    remark3: Optional[str] = "tralalelotralala"
    planned: Optional[int] = 111
    stated: Optional[int] = 222
    actual: Optional[int] = 333
    pad: Optional[GasificationStageEnums.Pad] = 567
    material: Optional[GasificationStageEnums.Material] = 570
    diameter: Optional[int]= 32142
    object_ks_id: Optional[int] = 11



class AddGasificationStageModel(GasificationStageModel):
    pass

class UpdateGasificationStageModel(GasificationStageModel):
    pass

class GetGasificationStageModel(BaseModel):
    pass

class ListGasificationStageModel(BaseModel):
    pass

class DeleteGasificationStageModel(BaseModel):
    pass