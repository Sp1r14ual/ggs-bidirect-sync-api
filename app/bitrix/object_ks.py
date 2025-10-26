from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta

webhook = "https://dev.ggs-nsk.ru/rest/118/xb10aqz3kexdtxlm/"
b = Bitrix(webhook)

payload = {
    "title": "Тестовое название", # Надо ли?
    "ufCrm10_1739508194": "Текст примечания",
    "ufCrm10_1739508209": ["Новосибирск", "Криводановка"], #Уточнить
    "ufCrm10_1739508282": ["Посёлок 1", "Посёлок 2"], #Уточнить
    "ufCrm10_1739508300": "Улица Пушкина",
    "ufCrm10_1739508326": "Дом Колотушкина",
    "ufCrm10_1739508348": 482, #Уточнить
    "ufCrm10_1739508360": "Y",
    "ufCrm10_1739508371": ["Состояние 1", "Состояние 2"], #Уточнить
    "ufCrm10_1739508383": ["Тип газификации 1", "Тип газификации 2"], #Поле с префиксом aaaa?
    "ufCrm10_1739508394": "Y",
    "ufCrm10_1739508449": ['CO_28'],
    "ufCrm10_1741160979089": "Москва, Улица Ленина, 1, кв. 1", #Адрес передается строкой?
    "ufCrm10_1750848582639": 482, #480, 481, 482
    "ufCrm10_1750848760947": 489, #483 - 493
    "ufCrm10_1750848908269": 497, #494 - 498
    "ufCrm10_1750849066": 407, #400 - 410
    "ufCrm10_1750849198248": "Y",
    "ufCrm10_1750849305242": "Тестовый ОДС",
    "ufCrm10_1750849321158": "Тестовый кадастровый номер земельного участка",
    "ufCrm10_1750849334062": "Тестовый кадастровый номер ОКС",
    "ufCrm10_1750849352474": "Тестовый № регистрации права собственности",
    "ufCrm10_1750849383": ['C_58'],
    "ufCrm10_1750850648876": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1750850660915": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1750850682809": "https://example.com",
    "ufCrm10_1750850728813": "Тестовый номер протокола",
    "ufCrm10_1750850739998": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1750850754609": "Тестовый номер",
    "ufCrm10_1750850773884": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1750850948612": 504, #499-507
    "ufCrm10_1750850970563": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1750850985519": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1750850998324": "Тестовый код объекта",
    "ufCrm10_1750851031452": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1750851045612": "Тестовое примечание",
    "ufCrm10_1750851086044": 111,
    "ufCrm10_1750851102593": 222,
    "ufCrm10_1750851120444": 333,
    "ufCrm10_1751015873771": 509, #508-510
    "ufCrm10_1751252590838": 512, #511-512
    "ufCrm10_1751252606669": 444,
    "ufCrm10_1751252619837": 555,
    "ufCrm10_1751252636015": "Тестовое примечание 2",
    "ufCrm10_1751252728426": "Тестовый договор о пуске",
    "ufCrm10_1751252759100": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751252770639": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751252783563": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751252795379": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751252824115": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751252844280": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751252859940": "https://examle.com",
    "ufCrm10_1751252895876": [
        "test-image.png",
        "base64string"
    ],
    "ufCrm10_1751252933528": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751252945644": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751252968777": "Ещё одно примечание",
    "ufCrm10_1751253021217": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751253805944": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ufCrm10_1751253828": 118
}

def add():
    res = b.call('crm.item.add', {"entityTypeId": 1066, "fields": payload})
    return res