import sys
import os

from parser import *

def main(): 
    wikiPath = sys.argv[1]
    indexPath = sys.argv[2]
    indexStat = sys.argv[3]

    try:
        os.mkdir(indexPath)
    except FileExistsError:
        print("Dir already exists!")

    parse(wikiPath, indexPath, indexStat)

if __name__ == '__main__':
    main()
