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
    def __init__(self, settings, model):
        self.settings = settings
        self.model = model

    def save(self):
        try:
            comInfoElement = etree.Element('КоммерческаяИнформация',**{'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}, **{'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema'}, **{"ВерсияСхемы":"2.09"}, **{"ДатаФормирования":"2015-06-26T18:28:09"}, **{"xmlns":"urn:1C.ru:commerceml_2"})
            catalog_element = etree.SubElement(comInfoElement, 'Каталог')
            catalog_element.set('СодержитТолькоИзменения', 'true')
            Id = etree.SubElement(comInfoElement, "Ид")
            Id.text = "3e376578-5aae-466f-8301-6842d2796cf9"
            id_of_classificator = etree.SubElement(comInfoElement, "ИдКлассификатора")
            id_of_classificator.text = "3e376578-5aae-466f-8301-6842d2796cf9"
            name = etree.SubElement(comInfoElement, "Наименование")
            name.text = "upp kaz"
            if len(self.model.goodGroups) > 0:
                groups = etree.SubElement(comInfoElement, "Группы")          
                self.draw_group_node(None, etree, groups)
                # for gr in self.model.goodGroups:
                    # group = etree.SubElement(groups, "Группа")
                    # group_id = etree.SubElement(group, "Ид")
                    # group_id.text = str(gr.id)
                    # version_number  = etree.SubElement(group, "НормерГруппы")
                    # gr_delete_note = etree.SubElement(group, "ПометкаУдаления")
                    # gr_name = etree.SubElement(group, "Наименование")
                    # gr_name.text = gr.name

            goods = etree.SubElement(comInfoElement, "Товары")
            for good in self.model.goods:
                good_elem_name = etree.SubElement(goods, "Товар")
                good_id = etree.SubElement(good_elem_name, "Ид")
                good_id.text = str(good.id)
                version_number = etree.SubElement(good_elem_name, "НомерВерсии")
                version_number.text = "AAAAAQAAAHI="
                delete_note = etree.SubElement(good_elem_name, "ПометкаУдаления")
                delete_note.text = "false"
                shtrihcode = etree.SubElement(good_elem_name, "Штрихкод")
                articul = etree.SubElement(good_elem_name, "Артикул")
                base_one  = etree.SubElement(good_elem_name, "БазоваяЕдиница")
                base_one.text = "166"
                good_name = etree.SubElement(good_elem_name, "Наименование")
                good_name.text = good.name
                groups = etree.SubElement(good_elem_name, "Группы")
                groups_id = etree.SubElement(groups, "Ид")
                groups_id.text = '13dab563-e271-11db-95d9-505054503030'
                describtion = etree.SubElement(good_elem_name, "Описание")
                country = etree.SubElement(good_elem_name, "Страна")
                values_of_properties = etree.SubElement(good_elem_name, "ЗначениеСвойств")
                values_of_property = etree.SubElement(values_of_properties, "ЗначениеСвайства")
                value_id = etree.SubElement(values_of_property, "Ид")
                value_id.text = "13dab530-e271-11db-95d9-505054503030"
                value = etree.SubElement(values_of_property, "Значение")
                tax_rates = etree.SubElement(good_elem_name, "СтавкаНалогов")            
                tax_rate = etree.SubElement(tax_rates, "СтавкаНалога")
                tax_rate_name = etree.SubElement(tax_rate, "Наименование")
                tax_rate_name.text = "НДС"
                rate = etree.SubElement(tax_rate, "Ставка")
                rate.text = "12"
                requisites_values = etree.SubElement(good_elem_name, "ЗначенияРеквизитов")
                requisites_value = etree.SubElement(requisites_values, "ЗначенияРеквизита")
                requisite_name = etree.SubElement(requisites_value, "Наименование")
                requisite_name.text = "ВидНоменклатуры"
                value_requisite = etree.SubElement(requisites_value, "Значение")
                requisite_name.text = "Материал"
                weight = etree.SubElement(good_elem_name, "Вес")
                weight.text = '0' 

            XML_FILE = os.path.join(
                self.settings[constants.UploadDirectory], '1.xml')

            etree.ElementTree(comInfoElement).write(
                XML_FILE, encoding='utf-8', xml_declaration=True)

        except IOError as e:
            print('nERROR: %sn' % e)
    
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

    def get_nodes_count(self, parent_id):
        counter = 0
        for i in self.model.goodGroups:
            if i.parent_id == parent_id:
                counter += 1
        return counter
