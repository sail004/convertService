import xml.etree.ElementTree as etree
import os
import constants
import xml.dom.minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = etree.tostring(elem, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='t')


class XmlSaver:
    def __init__(self, settings, model, logger):
        self.settings = settings
        self.model = model
        self.logger = logger
        self.global_id = "3e376578-5aae-466f-8301-6842d2796cf9"

    def save(self):
        try:
            if (len(self.model.goods) > 0):
                self.saveImport()
            if (len(self.model.offers) > 0):
                self.saveOffers()

        except IOError as e:
            self.logger.error('%s' % e)

    def saveImport(self):
        comInfoElement = etree.Element('КоммерческаяИнформация', **{'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}, **{
                                       'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema'}, **{"ВерсияСхемы": "2.09"}, **{"ДатаФормирования": "2015-06-26T18:28:09"}, **{"xmlns": "urn:1C.ru:commerceml_2"})
        classificator = etree.SubElement(comInfoElement, 'Классификатор')

        class_Id = etree.SubElement(classificator, "Ид")
        class_Id.text = self.global_id
        name = etree.SubElement(classificator, 'Наименование')
        name.text = "Экспорт"
        # catalog_element = etree.SubElement(comInfoElement, 'Каталог')
        # catalog_element.set('СодержитТолькоИзменения', 'true')
        # Id = etree.SubElement(comInfoElement, "Ид")
        # Id.text = self.global_id
        # id_of_classificator = etree.SubElement(
        #     comInfoElement, "ИдКлассификатора")
        # id_of_classificator.text = self.global_id
       # name1 = etree.SubElement(comInfoElement, "Наименование")
        # name1.text = "Товары"

        if len(self.model.goodGroups) > 0:
            groups = etree.SubElement(classificator, "Группы")
            self.draw_group_node(None, etree, groups)

        catalog_element = etree.SubElement(comInfoElement, 'Каталог')
        catalog_element.set('СодержитТолькоИзменения', 'true')
        id_classif = etree.SubElement(catalog_element, "ИдКлассификатора")
        id_classif.text = self.global_id
        id_catalog = etree.SubElement(catalog_element, "Ид")
        id_catalog.text = self.global_id
        name1 = etree.SubElement(catalog_element, "Наименование")
        name1.text = "Товары"
        goods = etree.SubElement(catalog_element, "Товары")
        for good in self.model.goods:
            good_elem_name = etree.SubElement(goods, "Товар")
            good_id = etree.SubElement(good_elem_name, "Ид")
            good_id.text = str(good.id)
            delete_note = etree.SubElement(
                good_elem_name, "ПометкаУдаления")
            delete_note.text = "false"
            good_name = etree.SubElement(good_elem_name, "Наименование")
            good_name.text = good.name
            groups = etree.SubElement(good_elem_name, "Группы")
            groupsId = etree.SubElement(groups, "Ид")
            groupsId.text = str(good.goodGroupId)
            tax_rates = etree.SubElement(good_elem_name, "СтавкаНалогов")
            tax_rate = etree.SubElement(tax_rates, "СтавкаНалога")
            tax_rate_name = etree.SubElement(tax_rate, "Наименование")
            tax_rate_name.text = "НДС"
            rate = etree.SubElement(tax_rate, "Ставка")
            rate.text = "20"

        XML_FILE = os.path.join(
            self.settings[constants.UploadDirectory], 'import.xml')

        etree.ElementTree(comInfoElement).write(
            XML_FILE, encoding='utf-8', xml_declaration=True)

    def draw_group_node(self, parent_id, etree, groups):
        for gr in self.model.goodGroups:
            if gr.parent_id == parent_id:
                group = etree.SubElement(groups, "Группа")
                group_id = etree.SubElement(group, "Ид")
                group_id.text = str(gr.id)
                gr_name = etree.SubElement(group, "Наименование")
                gr_name.text = gr.name
                if self.get_nodes_count(gr.id) > 0:
                    subgroups = etree.SubElement(group, "Группы")
                    self.draw_group_node(gr.id, etree, subgroups)

    def saveOffers(self):
        comInfoElement = etree.Element('КоммерческаяИнформация', **{'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}, **{
            'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema'}, **{"ВерсияСхемы": "2.09"}, **{"ДатаФормирования": "2015-06-26T18:28:09"}, **{"xmlns": "urn:1C.ru:commerceml_2"})
        # classificator = etree.SubElement(comInfoElement, 'Классификатор')
        # Id = etree.SubElement(classificator, "Ид")
        # Id.text = "1"
        # name = etree.SubElement(classificator, 'Наименование')
        # name.text = "export"
        offers_pack = etree.SubElement(comInfoElement, 'ПакетПредложений')
        offers_pack_id = etree.SubElement(offers_pack, 'Ид')
        offers_pack_id.text = self.global_id+"#"
        offers_pack_name = etree.SubElement(offers_pack, 'Наименование')
        offers_pack_name.text = "export"
        catalog_id = etree.SubElement(offers_pack, 'ИдКаталога')
        catalog_id.text = self.global_id
        classificator_id = etree.SubElement(offers_pack, 'ИдКлассификатора')
        classificator_id.text = self.global_id
        offers = etree.SubElement(offers_pack, 'Предложения')
        count = 0
        currentOffer = self.model.offers[0]
        while (count < len(self.model.offers)):
            offerElement = etree.SubElement(offers, 'Предложение')
            offer_id = etree.SubElement(offerElement, 'Ид')
            offer_id.text = str(currentOffer.goodId)+"#" + \
                str(currentOffer.assortmentId)
            delete_note = etree.SubElement(offerElement, 'ПометкаУдаления')
            delete_note.text = 'false'
            offer_name = etree.SubElement(offerElement, 'Наименование')
            offer_name.text = currentOffer.goodName
            barcode = etree.SubElement(offerElement, 'Штрихкод')
            barcode.text = currentOffer.barcode
            wasAssortmentFlag = False
            if (currentOffer.name1 != None):
                prod_charects = etree.SubElement(
                    offerElement, 'ХарактеристикиТовара')
                assortmentOffer = currentOffer
                while (currentOffer.assortmentId == assortmentOffer.assortmentId and (count < len(self.model.offers))):
                    wasAssortmentFlag = True
                    prod_charect = etree.SubElement(
                        prod_charects, 'ХарактеристикаТовара')
                    prod_charect_name = etree.SubElement(
                        prod_charect, 'Наименование')
                    prod_charect_name.text = assortmentOffer.name1
                    prod_charect_value = etree.SubElement(
                        prod_charect, 'Значение')
                    prod_charect_value.text = assortmentOffer.name2

                    count = count+1
                    if (count < len(self.model.offers)):
                        assortmentOffer = self.model.offers[count]

            pricesElement = etree.SubElement(offerElement, 'Цены')
            priceElement = etree.SubElement(pricesElement, 'Цена')
            price_id = etree.SubElement(priceElement, 'ИдТипаЦены')
            price_id.text = "BASE"
            pricepieceElement = etree.SubElement(priceElement, 'ЦенаЗаЕдиницу')
            pricepieceElement.text = str(currentOffer.salePrice)
            currencyElement = etree.SubElement(priceElement, 'Валюта')
            currencyElement.text = "RUB"
            quantityElement = etree.SubElement(offerElement, 'Количество')
            quantityElement.text = str(currentOffer.rest)

            if (wasAssortmentFlag == False):
                count = count+1
            if (count < len(self.model.offers)):
                currentOffer = self.model.offers[count]

        XML_FILE = os.path.join(
            self.settings[constants.UploadDirectory], 'offers.xml')

        etree.ElementTree(comInfoElement).write(
            XML_FILE, encoding='utf-8', xml_declaration=True)

    def get_nodes_count(self, parent_id):
        counter = 0
        for i in self.model.goodGroups:
            if i.parent_id == parent_id:
                counter += 1
        return counter
