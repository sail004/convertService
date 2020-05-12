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

            comInfoElement = etree.Element('КоммерческаяИнформация', **{'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}, **{
                                           'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema'}, **{"ВерсияСхемы": "2.09"}, **{"ДатаФормирования": "2015-06-26T18:28:09"}, **{"xmlns": "urn:1C.ru:commerceml_2"})

            # comment = Comment('Generated for PyMOTW')
            # top.append(comment)

            # child = Attr(comInfoElement, 'xmlns')
            # child.text = 'urn:1C.ru:commerceml_2'

            catalog_element = etree.SubElement(comInfoElement, 'Каталог')
            catalog_element.set('СодержитТолькоИзменения', 'true')
            # child_with_tail.text = 'This child has regular text.'
            # child_with_tail.tail = 'And "tail" text.'

            # child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
            # child_with_entity_ref.text = 'This & that'

            # print(prettify(top))
            # генерировать имя файла
            XML_FILE = os.path.join(
                self.settings[constants.UploadDirectory], '1.xml')

            etree.ElementTree(comInfoElement).write(
                XML_FILE, encoding='utf-8', xml_declaration=True)

        except IOError as e:
            print('nERROR: %sn' % e)
