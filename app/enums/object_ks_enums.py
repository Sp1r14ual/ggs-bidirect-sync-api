from enum import Enum

class ClientType2(Enum):
    connection_launch_only = 480
    gasification = 481
    resigning_to_vdgo = 482

class State2(Enum):
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

class GasificationType2(Enum):
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

class Event(Enum):
    reconstruction_existent_grs = 499
    insertion_on_applicat_territory = 500
    reconstruction_gas_distribution_station = 501
    reconstruction_grs = 502
    reconstruction_grs_construction_gb = 503
    reconstruction_and_construction_grs = 504
    construction_grs = 505
    tech_add_on_applicant_territory_borders = 506
    installation_gas_reduction_node = 507

class Pad(Enum):
    underground = 508
    undefined = 509
    aboveground = 510

class Material(Enum):
    polyethylene = 511
    metal = 512

class Manager(Enum):
    sergey_panasenko = 118

class ObjectKSFields(Enum):
    remark = "ufCrm10_1739508194"
    nas_punkt = "ufCrm10_1739508209"
    dnt_pos = "ufCrm10_1739508282"
    street = "ufCrm10_1739508300"
    house = "ufCrm10_1739508326"
    client_type = "ufCrm10_1739508348"
    project_to_vgdo_oao_sibirgasservice = "ufCrm10_1739508360"
    state = "ufCrm10_1739508371"
    gasification_type = "ufCrm10_1739508383"
    double_address = "ufCrm10_1739508394"
    owner = "ufCrm10_1739508449"
    address = "ufCrm10_1741160979089"
    client_type2 = "ufCrm10_1750848582639"
    state2 = "ufCrm10_1750848760947"
    gasification_type2 = "ufCrm10_1750848908269"
    district = "ufCrm10_1750849066"
    ods = "ufCrm10_1750849198248"
    gas_distribution_network = "ufCrm10_1750849305242"
    land_kadastr_number = "ufCrm10_1750849321158"
    oks_kadastr_number = "ufCrm10_1750849334062"
    ownership_rights_registration_number = "ufCrm10_1750849352474"
    owners2 = "ufCrm10_1750849383"
    application_from = "ufCrm10_1750850648876"
    passed_in_pto = "ufCrm10_1750850660915"
    received_technical_condition = "ufCrm10_1750850682809"
    protocol_number = "ufCrm10_1750850728813"
    date1 = "ufCrm10_1750850739998"
    number = "ufCrm10_1750850754609"
    date2 = "ufCrm10_1750850773884"
    event = "ufCrm10_1750850948612"
    due_date = "ufCrm10_1750850970563"
    reschedule_date = "ufCrm10_1750850985519"
    object_code = "ufCrm10_1750850998324"
    date3 = "ufCrm10_1750851031452"
    remark2 = "ufCrm10_1750851045612"
    planned = "ufCrm10_1750851086044"
    stated = "ufCrm10_1750851102593"
    actual = "ufCrm10_1750851120444"
    pad = "ufCrm10_1751015873771"
    material = "ufCrm10_1751252590838"
    diameter = "ufCrm10_1751252606669"
    footage = "ufCrm10_1751252619837"
    remark3 = "ufCrm10_1751252636015"
    launch_agreement_number = "ufCrm10_1751252728426"
    gas_launch_date = "ufCrm10_1751252759100"
    delivery_of_notice_date = "ufCrm10_1751252770639"
    send_to_mrg_date = "ufCrm10_1751252783563"
    shutting_gas_supply_system_date = "ufCrm10_1751252795379"
    application_from2 = "ufCrm10_1751252824115"
    passed_in_pto2 = "ufCrm10_1751252844280"
    received_technical_condition2 = "ufCrm10_1751252859940"
    documents = "ufCrm10_1751252895876"
    application_date = "ufCrm10_1751252933528"
    agreed = "ufCrm10_1751252945644"
    remark4 = "ufCrm10_1751252968777"
    gas_launch_date2 = "ufCrm10_1751253021217"
    pass_to_lawyer_date = "ufCrm10_1751253805944"
    manager = "ufCrm10_1751253828"