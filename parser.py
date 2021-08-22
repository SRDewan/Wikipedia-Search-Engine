import xml.etree.ElementTree as ET

def parse(file_path):
    docs = []

    for event, elem in ET.iterparse(file_path, events=("end",)):
        _, _, elem.tag = elem.tag.rpartition('}')

        if elem.tag == 'title':
            docs.append({ 'title': elem.text });

        elif elem.tag == 'id' and 'id' not in docs[-1]:
            docs[-1]['id'] = elem.text;

        elif elem.tag == 'text':
            docs[-1]['text'] = elem.text;

        elem.clear()

    return docs 
