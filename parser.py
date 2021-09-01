import os
import xml.etree.ElementTree as ET
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

nltk.download('punkt')
nltk.download('stopwords')
stopWords = set(stopwords.words('english'))
snowStemmer = SnowballStemmer(language='english')

index = {}
batchSize = 1000

def statWrite(statFilePath):
    statFile = open(statFilePath, "w")
    statFile.write(str(0) + "\n" + str(len(index)))
    statFile.close()

def indexWrite(outFolder):
    labels = ["t", "b", "i", "c", "l", "r"]
    content = ""

    for word in index:
        for doc in index[word]:
            content += word + ":d" + doc
            ctr = 0

            for field in index[word][doc]:
                if(field):
                    content += labels[ctr] + str(field) 
                ctr += 1

            content += "\n"

    indexFile = open(os.path.join(outFolder, "index.txt"), "w")
    indexFile.write(content)
    indexFile.close()

def processing(text, id, field):
    text = text.lower()
    tokens = re.split(r'[^a-z0-9]+', text)

    for token in tokens:
        if len(token) > 1 and token not in stopWords:
            word = snowStemmer.stem(token)

            if word not in index:
                index[word] = { id: [0, 0, 0, 0, 0, 0] }
            elif id not in index[word]:
                index[word][id] = [0, 0, 0, 0, 0, 0]

            index[word][id][field] += 1

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
    regex = re.compile('== ?External Links ?==([\S\s]+)', re.I)
    segs = regex.split(text)[1:]

    if len(segs):
        split = re.split('\n\n', segs[-1])
        links = re.split('\*', split[0])
        string = '\n'.join(links)

    return string

def getRefs(text):
    string = ""
    regex = re.compile('== ?References ?==([\S\s]+)', re.I)
    segs = regex.split(text)[1:]

    if len(segs):
        endRex = re.compile('{{authority control|{{defaultsort|\[\[category|\n==\w+', re.I)
        refs = endRex.split(segs[-1])[0]

        cleanRex = re.compile('{{reflist', re.I)
        clean = cleanRex.split(refs)
        string = '\n'.join(clean)

    return string

def bodyParse(body, id, title):
    comps = {
            'title': title,
            'body': body,
            'infobox': getInfobox,
            'category': getCategory,
            'links': getLinks,
            'references': getRefs,
            }
    ctr = 0

    for key in comps:
        string = ""
        if isinstance(comps[key], str):
            string = comps[key]
        else:
            string = comps[key](body)

        words = processing(string, id, ctr)
        ctr += 1

def parse(file_path, outFolder, statFile):
    docs = []
    ctr = 0

    for event, elem in ET.iterparse(file_path, events=("end",)):
        _, _, elem.tag = elem.tag.rpartition('}')

        if elem.tag == 'title':
            docs.append({ 'title': elem.text })

        elif elem.tag == 'id' and 'id' not in docs[-1]:
            docs[-1]['id'] = elem.text

        elif elem.tag == 'text' and elem.text != None:
            bodyParse(elem.text, docs[-1]['id'], docs[-1]['title'])

        elem.clear()

        ctr += 1
        if ctr % batchSize == 0:
            print("Done with ", ctr, " docs")

    indexWrite(outFolder)
    statWrite(statFile)
