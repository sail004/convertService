import requests
import json

token = '4844506a-d4c9-471d-8eb1-abebd865d91c'
headers = {'Accept': 'application/vnd.evotor.v2+json;charset=UTF-8',
           'Content-type':'application/vnd.evotor.v2+bulk+json',
            'x-authorization': '4844506a-d4c9-471d-8eb1-abebd865d91c'
           }
# def get_uuid():
#     url = 'https://api.evotor.ru/api/v1/inventories/stores/search'
#     response = requests.get(url, headers=headers)
#     #print (response)
#     StoreUuid=response.json()[0]['uuid']
#     #stores=json.loads(data)
#     return StoreUuid
# StoreUuid=get_uuid()
StoreUuid='20200421-86EB-4009-80AB-D54715C7D271'
print(StoreUuid)


# url ='https://api.evotor.ru/api/v1/inventories/stores/%s'%StoreUuid+'/products'
# print(url)
# response = requests.get(url, headers=headers)
# products=response.json()
# print(products)

# url = 'https://api.evotor.ru/api/v1/inventories/stores/%s'%StoreUuid+'/documents'
# response = requests.get(url, headers=headers)
# docs = response.json()
# print(docs)

# url = 'https://api.evotor.ru/api/v1/inventories/devices/search'
# response = requests.get(url, headers=headers)
# devices=response.json()
# print(devices)


url = 'https://api.evotor.ru/api/v1/inventories/stores/'+StoreUuid+'/products'
body =[
{
  "parent_id": "1ddea16b-971b-dee5-3798-1b29a7aa2e27",
  "name": "Сидр",
  "measure_name": "шт",
  "tax": "VAT_18",
  "allow_to_sell": True,
  "price": 123.12,
  "description": "Вкусный яблочный сидр",
  "article_number": "СДР-ЯБЛЧ",
  "code": "42",
  "barcodes": [
    "2000000000060"
  ],
  "type": "ALCOHOL_NOT_MARKED"
}]


json_body=json.dumps(body)
#json_body=json.dumps('{  "name":"Товар 1",  "type":"NORMAL",  "measure_name":"шт",  "tax":"VAT_18",  "allow_to_sell":true,  "price":111.0,  "cost_price":9352.5,  "parent_id":"5cd54680-5152-11e9-91c7-4b1dd1e1bcf8",  "attributes_choices":{    "be30db90-514f-11e9-91c7-4b1dd1e1bcf8":"be30db91-514f-11e9-91c7-4b1dd1e1bcf8",    "be30db94-514f-11e9-91c7-4b1dd1e1bcf8":"be3102a0-514f-11e9-91c7-4b1dd1e1bcf8"  }}')
print(json_body)
p = requests.post(url,data="{'name':'test 1','type':'NORMAL','measure_name':'шт','tax':'VAT_18','allow_to_sell':true,'price':111.0,'cost_price':9352.5,parent_id':'5cd54680-5152-11e9-91c7-4b1dd1e1bcf8','attributes_choices':{'be30db90-514f-11e9-91c7-4b1dd1e1bcf8':'be30db91-514f-11e9-91c7-4b1dd1e1bcf8','be30db94-514f-11e9-91c7-4b1dd1e1bcf8':'be3102a0-514f-11e9-91c7-4b1dd1e1bcf8'}}".encode('utf-8'),headers=headers)
# p = requests.post(url, json=json_body, headers=headers)
print(p)



