import fdb
import constants


class GoodGroup:
    def __init__(self, id, name, parent_id, evotorid, evotorparentid):
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.evotorid = evotorid
        self.evotorparentid = evotorparentid


class Good:
    def __init__(self, id, name, articul, barcode, goodGroupId,evotorid):
        self.name = name
        self.id = id
        self.articul = articul
        self.barcode = barcode
        self.goodGroupId = goodGroupId
        self.evotorid = evotorid

class Offer:
    def __init__(self, goodId, assortmentId, goodName, rest, salePrice, barcode, name1, name2):

        self.goodId = goodId
        self.assortmentId = assortmentId
        self.goodName = goodName
        self.rest = rest
        self.rest = rest
        self.salePrice = salePrice
        self.barcode = barcode
        self.name1 = name1
        self.name2 = name2


class ExportModel:
    def __init__(self, goodGroups, goods, offers):
        self.goodGroups = goodGroups
        self.goods = goods
        self.offers = offers


class SamlpeGoodsModel:
    def __init__(self):
        self.goodGroups = [GoodGroup(1, "Корень", None), GoodGroup(
            2, "Молоко ", 1), GoodGroup(3, "Хлеб", 1)]
        self.goods = [Good(1, "Молоко 1", "art1", "1234567890123", 2), Good(
            2, "Молоко 2", "art2", "123", 2), Good(3, "Хлеб 1", "art3", "12345", 3)]
        self.offers=[Offer(20041,156144,"СОРОЧКА ALLAN NEUMANN 000722",	1,	1400.00,	"2400000040798",	"ЦВЕТ",	"АЙВОРИ"),
            Offer(20041,156144,"СОРОЧКА ALLAN NEUMANN 000722",	1,	1400.00,	"2400000040798",	"МОДЕЛЬ",	"000722"),
            Offer(20105,156157,"КОСТЮМ БРАНОФФ",	1,	999.00,	"2400000065722",	"МОДЕЛЬ",	"5505-00")]


class LoaderResolver:
    def __init__(self,settings, logger):
        self.settings = settings
        self.logger = logger
    
    def GetLoader(self):
        if (self.settings[constants.ExchangeType]==0):
            return SampleLoader(self.settings, self.logger)
        if (self.settings[constants.ExchangeType]==1):
            return FbLoader(self.settings, self.logger)
        if (self.settings[constants.ExchangeType]==2):
            return EvotorLoader(self.settings, self.logger)
        return SampleLoader(self.settings, self.logger)

class SampleLoader:
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

    def Load(self):
        self.logger.debug("Starting sample loader")
        self.__goodsModel = SamlpeGoodsModel()
        self.logger.debug("Got %s good groups" %
                          len(self.__goodsModel.goodGroups))
        return self.__goodsModel


class FbLoader:
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

    def Load(self):
        self.logger.debug("Starting fb loader")
        connection = fdb.connect(
            dsn=self.settings[constants.dbPath], user='sysdba', password='masterke')
        cur = connection.cursor()
        cur.execute("select id,name,idparentgroup,treepath from v_goodgroups where id not in(868, 973, 1000, 1087, 1006, 948)")
        goodGroups = []
        for record in cur.fetchall():
            group = GoodGroup(record[0], record[1], record[2])
            goodGroups.append(group)
        cur.execute("select id,name,articul,idgoodgroup from v_goods where idgoodgroup not in (868, 973, 1000, 1087, 1006, 948)")
        goods = []
        for record in cur.fetchall():
            good = Good(record[0], record[1], record[2], '', record[3])
            goods.append(good)

        #cur.execute("select g.id as goodid,s.id as assortmentid,g.name as goodsname, rest ,saleprice,barcode, t.name as name1,ga.name  as name2 from currwhrests r join v_assortments s  on r.idassortment=s.id " +
        #            "left join  assortmentgoodattributes ga on s.id=ga.idassortment " +
        #            "left join attributetypes t on t.id=ga.idattributetype " +
        #            "left join goods g on s.idgood=g.id " +
        #            "order by g.id, s.id")
        cur.execute("select g.id as goodid,s.id as assortmentid,g.name as goodsname, r.rest ,r.saleprice,b.barcode, t.name as name1,ga.name  as name2 " +
                    "from goods g join v_assortments s  on g.id=s.idgood " +
                    "left join  assortmentgoodattributes ga on s.id=ga.idassortment "+
                    "left join barcodes b on s.id=b.idassortment "+
                    "left join attributetypes t on t.id=ga.idattributetype " +
                    "left join currwhrests r on r.idassortment=s.id " +
                    "where r.rest >=0 " +
                    "order by g.id, s.id")

        offers = []
        for record in cur.fetchall():
            offer = Offer(record[0], record[1], record[2], record[3],
                          record[4], record[5], record[6], record[7])
            offers.append(offer)
        self.__exportModel = ExportModel(goodGroups, goods, offers)
        self.logger.debug("Got %s good groups" %
                          len(self.__exportModel.goodGroups))
        self.logger.debug("Got %s goods " %
                          len(self.__exportModel.goods))
        self.logger.debug("Got %s offers " %
                          len(self.__exportModel.offers))
        return self.__exportModel

class EvotorLoader:
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

    def Load(self):
        self.logger.debug("Starting evotor loader")
        connection = fdb.connect(
            dsn=self.settings[constants.dbPath], user='sysdba', password='masterke')#,fb_library_name=self.settings[constants.FbClientPath])
        cur = connection.cursor()
        cur.execute("select id,name,idparentgroup,evotorid,evotorparentid from v_goodgroups where id not in(868, 973, 1000, 1087, 1006, 948)")
        goodGroups = []
        for record in cur.fetchall():
            group = GoodGroup(record[0], record[1], record[2], record[3], record[4])
            goodGroups.append(group)
        cur.execute("select first 10  g.id,name,articul,idgoodgroup, b.barcode, g.evotorid from v_goods g left join barcodes b on b.idgood=g.id where idgoodgroup not in (868, 973, 1000, 1087, 1006, 948)")
        goods = []
        for record in cur.fetchall():
            good = Good(record[0], record[1], record[2],  record[4], record[3], record[5])
            goods.append(good)

        cur.execute("select  first 10  g.id as goodid,s.id as assortmentid,g.name as goodsname, r.rest ,r.saleprice,b.barcode, t.name as name1,ga.name  as name2 " +
                    "from goods g join v_assortments s  on g.id=s.idgood " +
                    "left join  assortmentgoodattributes ga on s.id=ga.idassortment "+
                    "left join barcodes b on s.id=b.idassortment "+
                    "left join attributetypes t on t.id=ga.idattributetype " +
                    "left join currwhrests r on r.idassortment=s.id " +
                    "where r.rest >=0 " +
                    "order by g.id, s.id")

        offers = []
        for record in cur.fetchall():
            offer = Offer(record[0], record[1], record[2], record[3],
                          record[4], record[5], record[6], record[7])
            offers.append(offer)
        self.__exportModel = ExportModel(goodGroups, goods, offers)
        self.logger.debug("Got %s good groups" %
                          len(self.__exportModel.goodGroups))
        self.logger.debug("Got %s goods " %
                          len(self.__exportModel.goods))
        self.logger.debug("Got %s offers " %
                          len(self.__exportModel.offers))
        return self.__exportModel


