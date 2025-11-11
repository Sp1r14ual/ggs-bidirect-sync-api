from enum import Enum

class ClientType(Enum):
    connection_launch_only = 480
    gasification = 481
    resigning_to_vdgo = 482

class State(Enum):
    considered_delayed = 483
    asocial = 484
    gasificated = 485
    not_gasificated = 486
    considered_credit = 487
    considered_social = 488
    considered_standard = 489
    declined_to_demolish = 490
    house_burnt_down = 491
    stub = 492
    undefined = 493

class GasificationType(Enum):
    asocial = 494
    standard = 495
    social = 496
    credit = 497
    additional_gasification = 498

class District(Enum):
    dzerjinskiy = 400
    jeleznodorojniy = 401
    zaeltsovskiy = 402
    kalininskiy = 403
    kirovskiy = 404
    leninskiy = 405
    novosibirskiy = 406
    oktyabrskiy = 407
    pervomayskiy = 408
    sovetskiy = 409
    centralniy = 410

class Playground(Enum):
    test = 1
    avleda_m = 2
    biatlon = 3
    luch_97 = 4
    zolotaya_gorka_2003 = 5
    sibirskiye_prostori = 6

# Надо делать?
class Contract(Enum):
    pass

class ObjectKSFields(Enum):
    project_to_vgdo_oao_sibirgasservice = "ufCrm10_1739508360"
    double_address = "ufCrm10_1739508394"
    address = "ufCrm10_1741160979089"
    client_type = "ufCrm10_1750848582639"
    state = "ufCrm10_1750848760947"
    gasification_type = "ufCrm10_1750848908269"
    district = "ufCrm10_1750849066"
    ods = "ufCrm10_1750849198248"
    land_kadastr_number = "ufCrm10_1750849321158"
    oks_kadastr_number = "ufCrm10_1750849334062"
    ownership_rights_registration_number = "ufCrm10_1750849352474"
    owners = "ufCrm10_1750849383"
    documents = "ufCrm10_1751252895876"
    playground = "ufCrm10_1756278171"
    id_house_osa = "ufCrm10_1756282250286"
    contracts = "ufCrm10_1758892098"