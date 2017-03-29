#!/usr/bin/env python2
import os, random,  pickle,  time


# ------------------------------------------
# first things first - import fcp module
#Maybe randomize used nodes? Possibly increased perf...

import fcp
fcpHost = "127.0.0.1"
seedNodes = 3
openNodes = 100
monitorNodes = 5
lowestfcpport = 9481+seedNodes+ openNodes
highestfcpport = lowestfcpport + (monitorNodes-1)
putCHKs = []
dirList = os.listdir('./Test')
monitoredCHKs = []
successfulCHKs = []

#Empty textfiles that save said lists
def getCHKList():
    bool = False
    while (bool == False):
        sequence =  pickle.load( open('./putjobs.txt', 'rb'))
        if (sequence == []):
            time.sleep(3)
            print("Waiting for CHK list")
        else:
            bool = True
            print("Successfully imported CHKs")
    return sequence


def split(sequence, number_of_chunks):
    
    if not sequence:
        return []
   
    chunk_size, remainder = divmod(len(sequence), number_of_chunks)
   
    if chunk_size:
        result = [sequence[x:x+chunk_size]
                  for x in xrange(0, number_of_chunks * chunk_size, chunk_size)]
    else:
        result = [[]]
   
    if remainder:
        result[-1].extend(sequence[-remainder:])
   
    return result
    
def changefileset(fileList):
    for sfile in fileList:
        with open('./Test/'+sfile, 'ab') as fout:
            fout.write(str(random.getrandbits(1))) # replace 1024 with size_kb if not unreasonably large
    return





i = 0
putCHKs = getCHKList
while True:
        if ((i%10)==0):
            putCHKs = getCHKList()
        fcpPort = random.randint(lowestfcpport,  highestfcpport)
        node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.FATAL)            
        if(putCHKs != []):
            CHK = random.choice(putCHKs)
            print("Getting CHK: " + CHK)
            node.get(CHK, async = True,  timeout = 360,  ignoreDS = True,  )
            monitoredCHKs.append(CHK)
            pickle.dump(monitoredCHKs,  open('./monitoredCHKs.txt', 'w'))
        else:
            print("putCHKS is empty, mate!")
        time.sleep(10)
        i += 1
    
