import os

def split(indexPath, folder):

    secondary = os.path.join(folder, "secondary.txt")
    ctr = 0
    currName = ""
    curr = None

    with open(indexPath, 'r') as inp, open(secondary, 'w') as sec:
        while True:
            line = inp.readline()
            if not line:
                break

            if not curr:
                print("Making file {}.txt".format(ctr))
                currName = os.path.join(folder, "{}.txt".format(ctr))
                curr = open(currName, 'w')
                sec.write(line.split('|')[0] + "\n")

            curr.write(line)
            size = os.path.getsize(currName) / (1024 * 1024)
            if size > 512:
                curr.close()
                curr = None
                ctr += 1

    curr.close()

def merge(file1, file2, mergeFile):  
    with open(mergeFile, 'w') as op, open(file1, 'r') as f1, open(file2, 'r') as f2:
        line1 = f1.readline()
        line2 = f2.readline()

        while line1 or line2:
            if not line1:
                op.write(line2)
                line2 = f2.readline()

            elif not line2:
                op.write(line1)
                line1 = f1.readline()

            else:
                parts1 = line1.split('|')
                parts2 = line2.split('|')
                w1 = parts1[0]
                postings1 = '|'.join(parts1[1:])
                w2 = parts2[0]
                postings2 = '|'.join(parts2[1:])
                
                if w1 < w2:  
                    op.write(line1)  
                    line1 = f1.readline()

                elif w1 > w2:  
                    op.write(line2)  
                    line2 = f2.readline()

                else:
                    line = w1 + '|' + postings1.strip('\n') + '|' + postings2
                    op.write(line)

                    line1 = f1.readline()
                    line2 = f2.readline()

        os.remove(file1)
        os.remove(file2)

def mergeSort(folder):
    files = os.listdir(folder)

    while len(files) > 2:
        print("Number of index files: {}".format(len(files) - 1))

        for i in range(0, len(files) - 1, 2):
            old = os.path.join(folder, "{}.txt".format(i))
            new = os.path.join(folder, "{}.txt".format(i // 2))

            if(i + 1 < len(files) - 1):
                f1 = os.path.join(folder, "{}.txt".format(i))
                f2 = os.path.join(folder, "{}.txt".format(i + 1))
                old = os.path.join(folder, "merge.txt")
                merge(f1, f2, old)

            os.rename(old, new)

        files = os.listdir(folder)

    old = os.path.join(folder, "0.txt")
    new = os.path.join(folder, "index.txt")
    os.rename(old, new)
    return new

def finalInd(folder):
    indexPath = mergeSort(folder)
    split(indexPath, folder)
    os.remove(indexPath)
