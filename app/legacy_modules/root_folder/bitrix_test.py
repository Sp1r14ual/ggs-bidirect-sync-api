from fast_bitrix24 import Bitrix
from pprint import pprint
import json

webhook = "https://dev.ggs-nsk.ru/rest/132/sgcqlj6lfixazqh6/"
b = Bitrix(webhook)

# res = b.call('crm.contact.list', {'filter': {}, 'select': ['*']})
# res = b.call('crm.contact.get', {'id': 79})
# res = b.call('crm.company.get', {'id': 68})
# res = b.call('crm.requisite.list', {"select": ['*'], "filter": {"RQ_INN": "5405107128"}})
res = b.call('crm.item.get', {"id": id, "entityTypeId": 1222})
pprint(res)
# with open('data.json', 'w') as f:
#     json.dump(res, f)



