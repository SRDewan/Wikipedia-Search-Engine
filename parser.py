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
    pass

def processing(text):
    text = text.lower()
    tokens = tokenizer(text)
    stemmedTokens = []

    for token in tokens:
        stemmed = snowStemmer(token)
        if stemmed not in stopWords:
            stemmedTokens.append(stemmed)

    return stemmedTokens

def bodyParse(body, id, title):
    patterns = {
            'title': None,
            'infobox': re.compile('{{ ?Infobox ([\S\s]+)\n}}', re.I),
            'category': re.compile('\[\[Category:(.+)\]\]', re.I),
            'links': re.compile('== ?External Links ?==([\S\s]+)', re.I),
            'references': re.compile('== ?References ?==([\S\s]+)[==|\[\[Category:|]', re.I),
            }
    ctr = 0

    for key in patterns:
        string = ""
        if key != 'title':
            for i in patterns[key].finditer(body):
                string += '\n' + i.group(1)
        else:
            string = title

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
