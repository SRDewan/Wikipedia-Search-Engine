import sys

import parser

def main(): 
    wikiPath = sys.argv[1]
    indexPath = sys.argv[2]
    indexStat = sys.argv[3]

    parser(wikiPath)

if __name__ == '__main__':
    main()
