import xml.etree.ElementTree as ET

def parse(file_path):
    docs = []
    for event, elem in ET.iterparse(file_path, events=("end",)):
        if elem.tag == 'title':

        elif elem.tag == 'page':

        elem.clear()
    return count
