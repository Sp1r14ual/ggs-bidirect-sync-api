from datetime import date
from typing import Optional
from pydantic import BaseModel
import app.enums.object_ks as ObjectKSEnums

class ObjectKSModel(BaseModel):
    project_to_vgdo_oao_sibirgasservice: Optional[bool] = False
    double_address: Optional[bool] = False
    address: Optional[str] = "Москва, Улица Ленина, 1, кв. 1" #Адрес передается строкой?
    client_type: Optional[ObjectKSEnums.ClientType] = 480
    state: Optional[ObjectKSEnums.State] = 483
    gasification_type: Optional[ObjectKSEnums.GasificationType] = 494
    district: ObjectKSEnums.District = 400
    ods: Optional[bool] = False
    land_kadastr_number: Optional[str] = "123321"
    oks_kadastr_number: Optional[str] = "321123"
    ownership_rights_registration_number: Optional[str] = "789987"
    owners: Optional[list[str]] = ["CO_28", "C_58"]
    documents: Optional[list[str]]
    playground: Optional[ObjectKSEnums.Playground] = 1
    id_house_osa: Optional[str] = "12382934"
    contracts: Optional[int] = 16 #Надо делать Enum?


class AddObjectKSModel(ObjectKSModel):
    pass

class UpdateObjectKSModel(ObjectKSModel):
    pass

class GetObjectKSModel(BaseModel):
    pass

class ListObjectKSModel(BaseModel):
    pass

class DeleteObjectKSModel(BaseModel):
    pass

