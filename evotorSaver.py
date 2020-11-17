import requests
import json
import constants


class EvotorSaver:
    def __init__(self, settings, model, logger):
        self.settings = settings
        self.model = model
        self.logger = logger

    def get_store_uuid(self):
        url = 'https://api.evotor.ru/api/v1/inventories/stores/search'
        response = requests.get(url, headers=self.headers)
        StoreUuid = response.json()[0]['uuid']
        return StoreUuid
    
    def transformModel(self):
        result=[]
        for good in self.model.goods:
            result.append({"parent_id":"2137d28b-e83f-4a19-b72e-34b6972d2351", "type": "NORMAL", "name":good.name, "price":10, "cost_price":1, "quantity": 8,"measure_name":"шт", "tax":"VAT_18","allow_to_sell":True, "description":"", "article_number": good.articul, "barcodes":[good.barcode]})
        return result

    def save(self):
        self.logger.debug("Evotor api interaction...")
        self.headers = {'Accept': 'application/vnd.evotor.v2+json',
                        'Content-type': 'application/vnd.evotor.v2+json', 'x-authorization': self.settings[constants.apiKey]
                        #При запросе типа post id товара присваивается автоматически при добавлении +bulk в content type ничего не работает
                        }
        StoreUuid = self.get_store_uuid()
        self.logger.debug("Got store uuid:"+StoreUuid)
        url = "https://api.evotor.ru/stores/"+StoreUuid+"/products"

        body = self.transformModel()
        json_body=json.dumps(body)
        print(json_body)

        requestResult = requests.post(url,data=json_body, headers=self.headers)
        self.logger.debug(requestResult.json())

