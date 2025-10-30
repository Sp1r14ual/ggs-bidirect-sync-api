from datetime import date
from typing import Optional
from pydantic import BaseModel
import app.enums.object_ks_enums as ObjectKSEnums

class ObjectKSModel(BaseModel):
    remark: Optional[str] = "tralala"
    nas_punkt: Optional[str] #Уточнить область допустимых значений
    dnt_pos: Optional[str] #Уточнить область допустимых значений
    street: Optional[str] = "Улица Ленина"
    house: Optional[str] = "1"
    client_type: Optional[int] = 482 #Уточнить область допустимых значений
    project_to_vgdo_oao_sibirgasservice: Optional[bool] = False
    state: Optional[int] #Уточнить область допустимых значений
    gasification_type: Optional[int] #Уточнить область допустимых значений
    double_address: Optional[bool] = False
    owner: Optional[list[str]] = ["CO_28", "C_58"]
    address: Optional[str] = "Москва, Улица Ленина, 1, кв. 1" #Адрес передается строкой?
    client_type2: Optional[ObjectKSEnums.ClientType2] = 480
    state2: Optional[ObjectKSEnums.State2] = 483
    gasification_type2: Optional[ObjectKSEnums.GasificationType2] = 494
    district: ObjectKSEnums.District = 400
    ods: Optional[bool] = False
    gas_distribution_network: Optional[str] = "Газораспределительная сеть"
    land_kadastr_number: Optional[str] = "123321"
    oks_kadastr_number: Optional[str] = "321123"
    ownership_rights_registration_number: Optional[str] = "789987"
    owners2: Optional[list[str]] = ["CO_28"]
    application_from: Optional[date] = date.today()
    passed_in_pto: Optional[date] = date.today()
    received_technical_condition: Optional[str] = "https://example.com" #Ссылки передавать текстом?
    protocol_number: Optional[str] = "12321321"
    date1: Optional[date] = date.today()
    number: Optional[str] = "45324532523"
    date2: Optional[date] = date.today()
    event: Optional[ObjectKSEnums.Event] = 500
    due_date: Optional[date] = date.today()
    reschedule_date: Optional[date] = date.today()
    object_code: Optional[str] = "435894"
    date3: Optional[date] = date.today()
    remark2: Optional[date] = date.today()
    planned: Optional[int] = 111
    stated: Optional[int] = 222
    actual: Optional[int] = 333
    pad: Optional[ObjectKSEnums.Pad] = 509
    material: Optional[ObjectKSEnums.Material] = 511
    diameter: Optional[int]= 32142
    footage: Optional[int] = 1983213
    remark3: Optional[str]= "blablabla"
    launch_agreement_number: Optional[str] = "342432424"
    gas_launch_date: Optional[date] = date.today()
    delivery_of_notice_date: Optional[date] = date.today()
    send_to_mrg_date: Optional[date] = date.today()
    shutting_gas_supply_system_date: Optional[date] = date.today()
    application_from2: Optional[date] = date.today()
    passed_in_pto2: Optional[date] = date.today()
    received_technical_condition2: Optional[str] = "https://example.com" #Ссылки передавать текстом?
    documents: Optional[str] #Как передавать байтовые массивы?
    application_date: Optional[date] = date.today()
    agreed: Optional[date] = date.today()
    remark4: Optional[str] = "yeyeyeyeye"
    gas_launch_date2: Optional[date] = date.today()
    pass_to_lawyer_date: Optional[date] = date.today()
    manager: Optional[ObjectKSEnums.Manager] = 118

class AddObjectKSModel(ObjectKSModel):
    pass

class UpdateObjectKSModel(ObjectKSModel):
    id: int = 15

class GetObjectKSModel(BaseModel):
    id: int = 8

class ListObjectKSModel(BaseModel):
    #to-do
    pass

class DeleteObjectKSModel(BaseModel):
    #to-do
    pass

