from enum import Enum

class Grs2(Enum):
    not_chosen = 0
    grs_2 = 931
    grs_3 = 935
    grs_4 = 936
    grs_5 = 937
    grs_6 = 938
    grs_tolmachevo = 939
    grs_verh_tula = 940
    grs_vniimb = 941
    grs_wastewater_cleaning = 942
    grs_11 = 943

class Event(Enum):
    reconstruction_existent_grs = 562
    insertion_on_applicat_territory = 557
    reconstruction_gas_distribution_station = 558
    reconstruction_grs = 559
    reconstruction_grs_construction_gb = 560
    reconstruction_and_construction_grs = 561
    construction_grs = 563
    tech_add_on_applicant_territory_borders = 564
    installation_gas_reduction_node = 565

class Pad(Enum):
    underground = 567
    undefined = 566
    aboveground = 568

class Material(Enum):
    polyethylene = 570
    metal = 569

class GasificationStageFields(Enum):
    agreed = "ufCrm30_1755258794624"
    remark1 = "ufCrm30_1752134986320"
    grs = "ufCrm30_1752135017"
    gas_launch_agreement_number = "ufCrm30_1752135098663"
    gas_launch_agreement_date = "ufCrm30_1752135109465"
    gas_launch_primary_date = "ufCrm30_1752135120742"
    delivery_of_notice_date = "ufCrm30_1752135131635"
    send_to_mrg_date = "ufCrm30_1752135142054"
    shutting_gas_supply_system_date = "ufCrm30_1752135153518"
    request = "ufCrm30_1755258771573"
    footage = "ufCrm30_1752134976747"
    remark2 = "ufCrm30_1755258809561"
    application_from_ptu = "ufCrm30_1755258863730"
    passed_in_pto_ptu = "ufCrm30_1755258885208"
    received_technical_condition_ptu = "ufCrm30_1755258906950"
    number_ptu = "ufCrm30_1756278460585"
    date_ptu = "ufCrm30_1756278472540"
    number_tu = "ufCrm30_1756278498486"
    date_tu = "ufCrm30_1756278512881"
    grs2 = "ufCrm30_1756278644966"
    object_code = "ufCrm30_1752134654175"
    passed_in_pto = "ufCrm30_1752134405438"
    received_technical_condition = "ufCrm30_1752134426528"
    protocol_number = "ufCrm30_1752134450630"
    date1 = "ufCrm30_1752134469076"
    number = "ufCrm30_1752134475250"
    date2 = "ufCrm30_1752134482425"
    event = "ufCrm30_1752134577921"
    due_date = "ufCrm30_1752134626017"
    reschedule_date = "ufCrm30_1752134639461"
    application_from = "ufCrm30_1752134391549"
    date3 = "ufCrm30_1752134687862"
    remark3 = "ufCrm30_1752134699557"
    planned = "ufCrm30_1752134739629"
    stated = "ufCrm30_1752134753050"
    actual = "ufCrm30_1752134764506"
    pad = "ufCrm30_1752134918796"
    material = "ufCrm30_1752134946873"
    diameter = "ufCrm30_1752134963457"
    object_ks_id = "parentId1066"
