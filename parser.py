import xml.etree.ElementTree as ET
import re
import nltk
from nltk.tokenize import word_tokenize as tokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

nltk.download('punkt')
nltk.download('stopwords')
stopWords = set(stopwords.words('english'))
snowStemmer = SnowballStemmer(language='english')

index = {}

def fileWrite():
    print(index)

def processing(text):
    text = text.lower()
    tokens = tokenizer(text)
    stemmedTokens = []

    for token in tokens:
        stemmed = snowStemmer.stem(token)
        if stemmed not in stopWords:
            stemmedTokens.append(stemmed)

    return stemmedTokens

def getInfobox(text):
    string = ""
    regex = re.compile('{{ ?Infobox ', re.I)
    segs = regex.split(text)[1:]

    if len(segs):
        split = re.split('}}', segs[-1])
        for j in split:
            if '{{' not in j:
                segs[-1] = j
                break

        string = '\n'.join(segs)

    return string

def getCategory(text):
    string = ""
    regex = re.compile('\[\[Category:(.+)\]\]', re.I)

    for i in regex.finditer(text):
        string += '\n' + i.group(1)

    return string

def getLinks(text):
    string = ""
    regex = re.compile('== ?External Links ?==\n([\S\s]+)', re.I)

    for i in regex.finditer(text):
        section = i.group(1)

    return string

def getRefs(text):
    string = ""
    regex = re.compile('== ?References ?==([\S\s]+)[==|\[\[Category:|]', re.I)

    for i in regex.finditer(text):
        string += '\n' + i.group(1)

    return string

def bodyParse(body, id, title):
    comps = {
            'title': None,
            'infobox': getInfobox,
            'category': getCategory,
            'links': getLinks,
            'references': getRefs,
            }
    ctr = 0

    for key in comps:
        string = ""
        if key != 'title':
            string = comps[key](body)
        else:
            string = title

        # print(key, " : ", string)
        words = processing(string)
        for word in words:
            if word not in index:
                index[word] = { id: [0, 0, 0, 0, 0, 0] }
            elif id not in index[word]:
                index[word][id] = [0, 0, 0, 0, 0, 0]

            index[word][id][ctr] += 1
        
        ctr += 1

def parse(file_path):
    docs = []

    for event, elem in ET.iterparse(file_path, events=("end",)):
        _, _, elem.tag = elem.tag.rpartition('}')

        if elem.tag == 'title':
            docs.append({ 'title': elem.text })

        elif elem.tag == 'id' and 'id' not in docs[-1]:
            docs[-1]['id'] = elem.text

        elif elem.tag == 'text' and elem.text != None:
            bodyParse(elem.text, docs[-1]['id'], docs[-1]['title'])

        elem.clear()

    fileWrite()
