import sys

from parser import *

def main(): 
    wikiPath = sys.argv[1]
    indexPath = sys.argv[2]
    indexStat = sys.argv[3]

    docs = parse(wikiPath)

if __name__ == '__main__':
    main()
