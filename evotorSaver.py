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
            result.append({ "parent_id": "1ddea16b-971b-dee5-3798-1b29a7aa2e27", "name":good.name, "price":10,"measure_name":"шт", "tax":"VAT_20","allow_to_sell":True, "article_number": good.articul,"code":good.articul, "barcodes":[good.barcode],"type": "ALCOHOL_NOT_MARKED"})
        return result

    def save(self):
        self.logger.debug("Evotor api interaction...")
        self.headers = {'Accept': 'application/vnd.evotor.v2+json;charset=UTF-8',
                        'Content-type': 'application/vnd.evotor.v2+bulk+json', 'x-authorization': self.settings[constants.apiKey]
                        }
        StoreUuid = self.get_store_uuid()
        self.logger.debug("Got store uuid:"+StoreUuid)
        url = "https://api.evotor.ru/stores/"+StoreUuid+"/products"

        body = self.transformModel()

        json_body=json.dumps(body)
        
        print(json_body)

        requestResult = requests.post(url,data=json_body, headers=self.headers)
        self.logger.debug(requestResult)

