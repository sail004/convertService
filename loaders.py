
class GoodGroup:
    def __init__(self, id, name, parent_id):
        self.name = name
        self.id = id
        self.parent_id = parent_id


class Good:
    def __init__(self, id, name, articul, barcode, goodGroupId):
        self.name = name
        self.id = id
        self.articul = articul
        self.barcode = barcode
        self.goodGroupId = goodGroupId


class GoodsModel:
    def __init__(self):
        self.goodGroups = [GoodGroup(1, "Корень", None), GoodGroup(
            2, "Молоко ", 1), GoodGroup(3, "Хлеб", 1)]
        self.goods = [Good(1, "Молоко 1", "art1", "1234567890123", 2), Good(
            2, "Молоко 2", "art2", "123", 2), Good(3, "Хлеб 1", "art3", "12345", 3)]


class Loader:
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

    def Load(self):
        self.__goodsModel = GoodsModel()
        self.logger.debug("Got %s good groups" % len(self.__goodsModel.goodGroups))
        return self.__goodsModel
