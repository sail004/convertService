import fdb
import constants


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
    def __init__(self, goodGroups, goods):
        self.goodGroups = goodGroups
        self.goods = goods


class SamlpeGoodsModel:
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
        self.__goodsModel = SamlpeGoodsModel()
        self.logger.debug("Got %s good groups" %
                          len(self.__goodsModel.goodGroups))
        return self.__goodsModel


class FbLoader:
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

    def Load(self):
        connection = fdb.connect(
            dsn=self.settings[constants.dbPath], user='sysdba', password='masterke')
        cur = connection.cursor()
        cur.execute("select id,name,idparentgroup,treepath from v_goodgroups")
        goodGroups = []
        for record in cur.fetchall():
            group = GoodGroup(record[0], record[1], record[2])
            goodGroups.append(group)
        cur.execute("select id,name,articul,idgoodgroup from v_goods")
        goods = []
        for record in cur.fetchall():
            good = Good(record[0], record[1], record[2], '', record[3])
            goods.append(good)

        self.__goodsModel = GoodsModel(goodGroups, goods)
        self.logger.debug("Got %s good groups" %
                          len(self.__goodsModel.goodGroups))
        self.logger.debug("Got %s goods " %
                          len(self.__goodsModel.goods))
        return self.__goodsModel
