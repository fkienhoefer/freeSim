#!/usr/bin/env python2
import os, random,  pickle,  time


# ------------------------------------------
# first things first - import fcp module
#Maybe randomize used nodes? Possibly increased perf...

import fcp
fcpHost = "127.0.0.1"
seedNodes = 1
openNodes = 10
lowestfcpport = 9481+seedNodes
highestfcpport = lowestfcpport + (openNodes-1)

#Empty textfiles that save said lists
putCHKs = pickle.load( open('./putjobs.txt', 'rb'))
dirList = os.listdir('./Test')

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



while True:
    fcpPort = random.randint(lowestfcpport,  highestfcpport)
    node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.FATAL)
    i = random.randint(0,  10)
    if (i == 1):
        changefileset(dirList)
        job = node.put('CHK@', file = './Test/'+dirList[2], async = True)
        print("Inserting new file")
        putCHKs.append(job.wait())
        print("Insert successful! CHK = "+ job.getResult())
        pickle.dump(putCHKs,  open('./putjobs.txt', 'a'))
        
    else:
        if(putCHKs != []):
            CHK = random.choice(putCHKs)
            print("Getting CHK: " + CHK)
            node.get(CHK, async = True,  timeout = 360)
        else:
            print("putCHKS is empty, mate!")
    time.sleep(random.randint(3,  15))
    
