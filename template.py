import xml.etree.ElementTree as ET
import re

class Materials:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.indications = []
        
    def __repr__(self):
        return '{} with ID {}'.format(self.name, self.id)
        
    def add_indication(self, indication):
        self.indications.append(indication)
        #print("added for", self.name, 'indication', indication)
        
    def get_id(self):
        return self.id
        
    def get_name(self):
        return self.name
    
    def get_materials(self):
        return self.indications
         
    def print_indicatins(self):
        for indication in self.indications:
            print(indication)

class Indications:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.materials = []
        
    def __repr__(self):
        return 'Indication name {} with ID {}'.format(self.name, self.id)
        
    def get_name(self):
        return self.name
        
    def get_id(self):
        return int(self.id)
        
    def add_material(self, material):
        self.materials.append(material)


class Xml_indications:
    def __init__(self, name):
        self.name = name
        self.materials = []
    
    def add_material(self, material):
        self.materials.append(material)
        
    def get_name(self):
        return self.name
        
    def get_condition(self):
        condition = []
        for material in self.materials:
            condition.append('RestorationType={}'.format(material.get_name().replace(' ','')))
        return ' OR '.join(condition)
        
def line_parser(line, material_id):
    items = line.split(';;;')
    detected_items = []
    detected_class = ''
    #print('items', items)
    for item in items:
        #print('all items in items before ;__"{}"__'.format(item))
        item = item.strip(';')
        if item != '':
            #print('Item now is ___*{}____'.format(item))
            data = item.split(';')
            #print('printing data __*{}*__'.format(data))
            if data[0] == 'ID':
                #print('yes')
                detected_class = 'Materials'
                detected_items.append(data[1])
            elif len(data)>1 and re.match('\d{1,2}\w', data[0]):
                detected_class = 'Indications'
                #print(data)
                #print(data[0][:-1])
                detected_items.append(Indications(data[1], data[0][:-1]))
                
    return detected_class, detected_items

def link_data(meterials_list, indications_list):
    for material in materials_list:
        id = material.get_id()
        for indication in indications_list:
            #print('indication id check ', indication.get_id())
            #print(id)
            if indication.get_id() == id:
                #print('added indication with ID {} and name {} to material {}'.format(indication.get_id(), indication.get_name(), material.name))
                material.add_indication(indication.get_name())

def check_if_exists(list, name):
    for object in list:
        if object.get_name() == name:
            return True
    return False
                
def create_xml_indications(materils_list, indications_list):
    xml_indicatons_list = []
    for indication in indications_list:
        if not check_if_exists(xml_indicatons_list, indication.get_name()):
            temp_object = Xml_indications(indication.get_name())
            for material in materials_list:
                for indication_in_material in material.get_materials():
                    #print('material from materials list ', indication_in_material)
                    #print(indication.get_name())
                    if indication_in_material == indication.get_name():
                        temp_object.add_material(material)   
            xml_indicatons_list.append(temp_object)
    return xml_indicatons_list        
    
def read_file(file_name):
    with open(file_name, 'r') as file:
        material_id = 1
        for line in file:
            class_in_line, data_in_line = line_parser(line, material_id)
            if data_in_line:
                if class_in_line == 'Materials':
                    for material in data_in_line:
                        materials_list.append(Materials(material, material_id))
                        material_id += 1
                if class_in_line == 'Indications':
                    for indication in data_in_line:
                        indications_list.append(indication)

def remove_empty_materials(meterials_list):
    i = 0
    cleared_list = []
    for i in range(len(materials_list)-1):
        #print(meterials_list[i])
        #print(meterials_list[i].get_materials())
        if materials_list[i].get_materials() != []:
            #print('yes')
            cleared_list.append(materials_list[i])
    return cleared_list

materials_list = []
indications_list = []
read_file('raw.csv')                 
link_data(materials_list, indications_list)
materials_list = remove_empty_materials(materials_list)
xml_indicatons_list = create_xml_indications(materials_list, indications_list)
 #working with xml 
 

    
def xml_add_materilal(root, materials_list):
    for material in materials_list:
        item = ET.SubElement(root[6][0], 'Item')
        item.attrib['ID'] = material.get_name().replace(' ', '')
        item.attrib['SupportsColor'] = 'True'
        item.attrib['TypeClass'] = 'Crown'
        caption = ET.SubElement(item, 'Caption')
        caption.attrib['LanguageID'] = 'en'
        caption.attrib['Text'] = material.get_name()
        image = ET.SubElement(item, 'Image')
        image.attrib['FileName'] = 'CrownNew32x32.png'

def xml_add_indication(root, xml_indicatons_list):
    for indication in xml_indicatons_list:
        item = ET.SubElement(root[6][1], 'Item')
        item.attrib['Condition'] = indication.get_condition()
        item.attrib['ID'] = indication.get_name().replace(' ', '')
        caption = ET.SubElement(item, 'Caption')
        caption.attrib['LanguageID'] = 'en'
        caption.attrib['Text'] = indication.get_name()
        image = ET.SubElement(item, 'Image')
        image.attrib['FileName'] = 'ColorGold32x32.png'
    
def edit_xml(file_name):  
    tree = ET.parse(file_name)
    root = tree.getroot()
    xml_add_materilal(root, materials_list)
    xml_add_indication(root, xml_indicatons_list)
    tree.write('output.xml')



edit_xml('ThreeShapeDefault.xml')
    


'''
item = ET.SubElement(root[6][0], 'itemTEST')

item.attrib['ID'] = 'TEST Crown'
item.attrib['SupportsColor'] = 'Test True'
item.attrib['TyepClass'] = 'Test_type'

subitem = ET.SubElement(item, 'TEST_Caption')
subitem.attrib['LanguageID'] = 'EN'
subitem.attrib['Text'] = 'Test crown'



tree.write('output.xml')
'''
