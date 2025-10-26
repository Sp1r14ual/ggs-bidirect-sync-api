from fast_bitrix24 import Bitrix
from pprint import pprint
import json

webhook = "https://dev.ggs-nsk.ru/rest/118/xb10aqz3kexdtxlm/"
b = Bitrix(webhook)

res = b.call('crm.item.get', {"entityTypeId": 1066 , "id": 34})
pprint(res)
# with open('data.json', 'w') as f:
#     json.dump(res, f)

