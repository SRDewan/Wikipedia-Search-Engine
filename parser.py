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
stemmed = {}
batchSize = 10000
ctr = 0

def dump(outFolder, docs):
    global ctr, index

    filePath = os.path.join(outFolder, "{}.txt".format(ctr))
    indexWrite(filePath)
    titleWrite(docs[ctr * batchSize:], os.path.join(outFolder, "titles.txt"))
    ctr += 1

    print("Done with ", len(docs), " docs")
    index = {}

def titleWrite(docs, filePath):
    content = ""
    for i in range(len(docs)):
        content += docs[i] + "\n"

    titleFile = open(filePath, "a")
    titleFile.write(content)
    titleFile.close()

def indexWrite(filePath):
    labels = ["t", "b", "i", "c", "l", "r"]
    content = ""

    for word in sorted(index):
        line = word + "|"
        for idx, doc in enumerate(index[word]):
            totFreq = sum(index[word][doc])
            if(totFreq <= 1):
                continue

            line += doc
            ctr = 0

            for field in index[word][doc]:
                if(field):
                    line += labels[ctr] + str(field) 
                ctr += 1

            line += "|"

        if(line == word + "|"):
            continue

        line = line[:-1]
        line += "\n"
        content += line

    indexFile = open(filePath, "w")
    indexFile.write(content)
    indexFile.close()

def processing(text, id, field):
    text = text.lower()
    tokens = re.split(r'[^a-z0-9]+', text)

    for token in tokens:
        if len(token) > 1 and token not in stopWords:
            if token not in stemmed:
                stemmed[token] = snowStemmer.stem(token)
            word = stemmed[token]

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

    context = ET.iterparse(file_path, events=("start", "end"))
    # get the root element
    event, root = next(context)

    for event, elem in context:
        if event == "end":
            _, _, elem.tag = elem.tag.rpartition('}')

            if elem.tag == 'title':
                docs.append(elem.text)

            elif elem.tag == 'text' and elem.text != None:
                docId = len(docs) - 1
                bodyParse(elem.text, str(docId), docs[docId])

            elif elem.tag == 'page':
                if len(docs) % batchSize == 0:
                    dump(outFolder, docs)

            elif elem.tag == 'mediawiki':
                dump(outFolder, docs)

            root.clear()
