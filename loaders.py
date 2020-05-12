
class GoodGroup:
    def __init__(self, id, name, parentId):
        self.name = name
        self.id = id
        self.parentId = parentId


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
        self.goods = [Good(1, "Молоко 1", "art1", "1234567890123",2), Good(
            2, "Молоко 2", "art2", "123",2), Good(3, "Хлеб 1", "art3", "12345",3)]


class Loader:
    def __init__(self, settings):
        self.settings = settings

    def Load(self):
        self.__goodsModel = GoodsModel()
        return self.__goodsModel
