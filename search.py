import sys
import os

from queryProc import *

def main(): 
    indexPath = sys.argv[1]
    queryStrg = sys.argv[2]

    if os.path.exists(indexPath):
        result = queryProc(indexPath, queryStrg)
    else:
        print("Dir does not exist!")

if __name__ == '__main__':
    main()
