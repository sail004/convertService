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

    def get_products(self):
        StoreUuid = self.get_store_uuid()
        url = 'https://api.evotor.ru/stores/' + StoreUuid + '/products'
        response = requests.get(url, headers=self.headers)
        Products = response.json()['items']
        return (Products)

    def get_groups(self):
        StoreUuid = self.get_store_uuid()
        url = 'https://api.evotor.ru/stores/' + StoreUuid + '/product-groups'
        print(url)
        response = requests.get(url, headers=self.headers)
        Groups = response.json()['items']
        return Groups

    def transformModel(self):
        result=[]
        for good in self.model.goods:
            result.append({"parent_id":"2137d28b-e83f-4a19-b72e-34b6972d2351", "type": "NORMAL", "name":good.name, "price":10, "cost_price":1, "quantity": 8,"measure_name":"шт", "tax":"VAT_18","allow_to_sell":True, "description":"", "article_number": good.articul, "barcodes":[good.barcode]})
        return result

    def GoodGroups(self):
        result=[]
        for group in self.model.goodGroups:
            result.append({'name': group.name, 'parent_id': group.evotorparentid})
        return result

    def save(self):
        self.logger.debug("Evotor api interaction...")
        self.headers = {'Accept': 'application/vnd.evotor.v2+json',
                        'Content-type': 'application/vnd.evotor.v2+json', 'x-authorization': self.settings[constants.apiKey] #При запросе типа post id товара присваивается автоматически при добавлении +bulk в content type ничего не работает
                        }
        StoreUuid = self.get_store_uuid()
        self.logger.debug("Got store uuid:"+StoreUuid)
        url = "https://api.evotor.ru/stores/"+StoreUuid+"/products"

        body = self.transformModel()
        json_body=json.dumps(body)
        print(json_body)
        requestResult = requests.post(url,data=json_body, headers=self.headers)

        url = 'https://api.evotor.ru/stores/'+StoreUuid+'/product-groups'
        body = self.GoodGroups()
        json_body=json.dumps(body)
        print(json_body)
        requestResult = requests.post(url, data=json_body, headers=self.headers)

        products_json = self.get_products()
        with open('products.json', 'w') as outfile:
            json.dump(products_json, outfile, indent=2)

        groups_json = self.get_groups()
        with open('groups.json', 'w') as outfile:
            json.dump(groups_json, outfile, ensure_ascii=False, indent=2)

        with open('groups.json', 'r') as infile:     #если у товара нет parent_id то это поле просто не возвращается в JSONе, каеф
            groups_sql = json.loads(infile.read())
            parent_id = 'Null'
            for groups_sql in groups_sql:
                try:
                    name = groups_sql['name']
                    id = groups_sql['id']
                    parent_id = groups_sql['parent_id']
                except KeyError:
                    name = groups_sql['name']
                    id = groups_sql['id']

                print(name, id, parent_id)
                # url = 'https://api.evotor.ru/stores/' + StoreUuid + '/product-groups/' + id #УДАЛЕНИЕ ГРУПП ПО ОДНОЙ В СТО ТЫЩ ПРОХОДОВ
                # print(url)
                # response = requests.delete(url, headers=self.headers)
                # print(response)




        self.logger.debug(requestResult.json())



