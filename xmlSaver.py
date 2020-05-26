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
        class_id = etree.SubElement(classificator, "Ид")
        class_id.text="3e376578-5aae-466f-8301-6842d2796cf9"
        name = etree.SubElement(classificator, 'Импорт')
               
        if len(self.model.goodGroups) > 0:
            groups = etree.SubElement(classificator, "Группы")
            self.draw_group_node(None, etree, groups)
        
        catalog_element = etree.SubElement(comInfoElement, 'Каталог')
        catalog_element.set('СодержитТолькоИзменения', 'true')
        id_classif = etree.SubElement(catalog_element, "ИдКлассификатора")
        id_classif.text = "3e376578-5aae-466f-8301-6842d2796cf9"
        id_catalog = etree.SubElement(catalog_element, "Ид")
        id_catalog.text = "3e376578-5aae-466f-8301-6842d2796cf9"
        goods = etree.SubElement(catalog_element, "Товары")
        for good in self.model.goods:
            good_elem_name = etree.SubElement(goods, "Товар")
            good_id = etree.SubElement(good_elem_name, "Ид")
            good_id.text = str(good.id)
            # version_number = etree.SubElement(
            #     good_elem_name, "НомерВерсии")
            # version_number.text = "AAAAAQAAAHI="
            delete_note = etree.SubElement(
                good_elem_name, "ПометкаУдаления")
            delete_note.text = "false"
            shtrihcode = etree.SubElement(good_elem_name, "Штрихкод")
            articul = etree.SubElement(good_elem_name, good.articul)
            # base_one = etree.SubElement(good_elem_name, "БазоваяЕдиница")
            # base_one.text = "166"
            good_name = etree.SubElement(good_elem_name, "Наименование")
            good_name.text = good.name
            groups = etree.SubElement(good_elem_name, "Группы")
            groups_id = etree.SubElement(groups, "Ид")
            groups_id.text = str(good.goodGroupId)
            # description = etree.SubElement(good_elem_name, "Описание")
            # country = etree.SubElement(good_elem_name, "Страна")
            # values_of_properties = etree.SubElement(
            #     good_elem_name, "ЗначениеСвойств")
            # values_of_property = etree.SubElement(
            #     values_of_properties, "ЗначениеСвайства")
            # value_id = etree.SubElement(values_of_property, "Ид")
            # value_id.text = "13dab530-e271-11db-95d9-505054503030"
            # value = etree.SubElement(values_of_property, "Значение")
            tax_rates = etree.SubElement(good_elem_name, "СтавкаНалогов")
            tax_rate = etree.SubElement(tax_rates, "СтавкаНалога")
            tax_rate_name = etree.SubElement(tax_rate, "Наименование")
            tax_rate_name.text = "НДС"
            rate = etree.SubElement(tax_rate, "Ставка")
            rate.text = "20"
            # requisites_values = etree.SubElement(
            #     good_elem_name, "ЗначенияРеквизитов")
            # requisites_value = etree.SubElement(
            #     requisites_values, "ЗначенияРеквизита")
            # requisite_name = etree.SubElement(
            #     requisites_value, "Наименование")
            # requisite_name.text = "ВидНоменклатуры"
            # value_requisite = etree.SubElement(
            #     requisites_value, "Значение")
            # requisite_name.text = "Материал"
            # weight = etree.SubElement(good_elem_name, "Вес")
            # weight.text = '0'

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
                # version_number  = etree.SubElement(group, "НормерГруппы")
                # gr_delete_note = etree.SubElement(group, "ПометкаУдаления")
                gr_name = etree.SubElement(group, "Наименование")
                gr_name.text = gr.name
                if self.get_nodes_count(gr.id) > 0:
                    subgroups = etree.SubElement(group, "Группы")
                    self.draw_group_node(gr.id, etree, subgroups)

    def saveOffers(self):
        comInfoElement = etree.Element('КоммерческаяИнформация', **{'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}, **{
            'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema'}, **{"ВерсияСхемы": "2.09"}, **{"ДатаФормирования": "2015-06-26T18:28:09"}, **{"xmlns": "urn:1C.ru:commerceml_2"})
        classificator = etree.SubElement(comInfoElement, 'Классификатор')
        Id = etree.SubElement(classificator, "Ид")
        Id.text = "1"
        name = etree.SubElement(classificator, 'Наименование')
        name.text = "export"
        offers_pack = etree.SubElement(comInfoElement, 'ПакетПредложений')
        offers_pack_id = etree.SubElement(offers_pack, 'Ид')
        offers_pack_id.text = "1"
        offers_pack_name = etree.SubElement(offers_pack, 'Наименование')
        offers_pack_name.text = "export"
        catalog_id = etree.SubElement(offers_pack, 'ИдКаталога')
        catalog_id.text = "1"
        classificator_id = etree.SubElement(offers_pack, 'ИдКлассификатора')
        classificator_id.text = "1"
        offers = etree.SubElement(offers_pack, 'Предложения')
        count = 0
        currentOffer = self.model.offers[0]
        while (count < len(self.model.offers)):
            offerElement = etree.SubElement(offers, 'Предложение')
            offer_id = etree.SubElement(offerElement, 'Ид')
            offer_id.text = str(currentOffer.goodId)+"#" + str(currentOffer.assortmentId)
            # version_number = etree.SubElement(offerElement, 'НомерВерсии')
            delete_note = etree.SubElement(offerElement, 'ПометкаУдаления')
            delete_note.text = 'false'
            offer_name = etree.SubElement(offerElement, 'Наименование')
            offer_name.text = currentOffer.goodName
            # offer_value = etree.SubElement(offerElement, 'Значение')
            barcode = etree.SubElement(offerElement, 'Штрихкод')
            barcode.text = currentOffer.barcode
            wasAssortmentFlag=False
            if (currentOffer.name1 != None):
                prod_charects = etree.SubElement(
                    offerElement, 'ХарактеристикиТовара')
                assortmentOffer = currentOffer
                while (currentOffer.assortmentId == assortmentOffer.assortmentId and (count < len(self.model.offers))):
                    wasAssortmentFlag=True
                    prod_charect = etree.SubElement(
                        prod_charects, 'ХарактеристикаТовара')
                    prod_charect_name = etree.SubElement(
                        prod_charect, 'Наименование')
                    prod_charect_name.text = assortmentOffer.name1
                    prod_charect_value = etree.SubElement(
                        prod_charect, 'Значение')
                    prod_charect_value.text = assortmentOffer.name2
                    
                    count = count+1
                    if (count<len(self.model.offers)):
                        assortmentOffer = self.model.offers[count]
         
            pricesElement = etree.SubElement(offerElement, 'Цены')
            priceElement = etree.SubElement(pricesElement, 'Цена')
            pricepieceElement = etree.SubElement(priceElement, 'ЦенаЗаЕдиницу')
            pricepieceElement.text = str(currentOffer.salePrice)
            currencyElement = etree.SubElement(priceElement, 'Валюта')
            currencyElement.text = "RUB"
            quantityElement = etree.SubElement(offerElement, 'Количество')
            quantityElement.text = str(currentOffer.rest)

            if (wasAssortmentFlag==False):
                count = count+1
            if (count<len(self.model.offers)):
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
