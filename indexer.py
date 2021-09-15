import sys
import os

from parser import *
from finalInd import *

def main(): 
    wikiPath = sys.argv[1]
    indexPath = sys.argv[2]
    indexStat = sys.argv[3]

    try:
        os.mkdir(indexPath)
    except FileExistsError:
        print("Dir already exists!")

    parse(wikiPath, indexPath, indexStat)
    finalInd(indexPath)

if __name__ == '__main__':
    main()
