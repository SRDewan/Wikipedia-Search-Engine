import sys
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

stopWords = set(stopwords.words('english'))
snowStemmer = SnowballStemmer(language='english')
results = {}

def indexToJson(docs):
    ret = {"t": [], "b": [], "i": [], "c": [], "l": [], "r": []}

    for doc in docs:
        fields = re.split(r"([a-z])", doc)
        id = fields[0]

        for f in range(1, len(fields), 2):
            ret[fields[f]].append(id)

    return ret

def search(indexPath, searchSpace):
    indexFile = open(os.path.join(indexPath, "index.txt"), "r")
    index = indexFile.readlines()
    ctr = 0

    for line in index:
        segs = re.split(r"\|", line)
        if(segs[0] in searchSpace):
            results[searchSpace[segs[0]]] = indexToJson(segs[1:])

    indexFile.close()

def queryProc(queryStrg):
    query = queryStrg.lower()
    parts = re.split(r"[^a-z0-9:]", query)
    searchSpace = {}
    fieldQueries = {"n": [], "t": [], "b": [], "i": [], "c": [], "l": [], "r": []}
    cur = "n"

    for part in parts:
        subparts = re.split(":", part)

        if(len(subparts) == 1 and len(subparts[0])):
            fieldQueries[cur].append(part)
            results[part] = {}

            word = part
            if len(word) > 1 and word not in stopWords:
                word = snowStemmer.stem(word)
                searchSpace[word] = part

        else:
            for i, subpart in enumerate(subparts):
                if(subpart in fieldQueries and subpart != "n" and i < len(subparts) - 1):
                    cur = subpart

                elif(len(subpart)):
                    fieldQueries[cur].append(part)
                    results[subpart] = {}

                    word = subpart
                    if len(word) > 1 and word not in stopWords:
                        word = snowStemmer.stem(word)
                        searchSpace[word] = subpart

    return searchSpace

def disp(results):
    print("{")
    for key in results:
        print(key, ": ", results[key])

    print("}")
        
def main(): 
    indexPath = sys.argv[1]
    queryStrg = sys.argv[2]

    if os.path.exists(indexPath):
        searchSpace = queryProc(queryStrg)
        search(indexPath, searchSpace)
        disp(results)

    else:
        print("Dir does not exist!")

if __name__ == '__main__':
    main()
