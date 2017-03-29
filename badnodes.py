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
badNodes = 10 
lowestfcpport = 9481+seedNodes+openNodes+monitorNodes
highestfcpport = lowestfcpport + (badNodes-1)

#Empty textfiles that save said lists
putCHKs = []
if (os.path.isfile('./badjobs.txt')):
    putCHKs = pickle.load( open('./badjobs.txt', 'rb'))
dirList = os.listdir('./Bad')

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
        with open('./Bad/'+sfile, 'ab') as fout:
            fout.write(str(random.getrandbits(1))) # replace 1024 with size_kb if not unreasonably large
    return

#Calls changefileset and randomly add 10 elements of changed fileset
def putfiles(fileList):
    jobs = []
    changefileset(fileList)
    print("Changing our bad files and adding 10 of 'em")
    for i in range(10):
        fcpPort = random.randint(lowestfcpport,  highestfcpport)
        node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.FATAL)
        sfile = random.choice(fileList)
        job = node.put('CHK@', file = './Bad/'+sfile, async = True)
        jobs.append(job)
        
    for job in jobs:
        print("waiting for our bad inserts to settle")
        putCHKs.append(job.wait())
    return


changefileset(dirList)
jobs = []
for item in dirList:
    print("Being bad with " + item)
    fcpPort = random.randint(lowestfcpport,  highestfcpport)
    node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.FATAL)
    job = node.put('CHK@', file = './Bad/'+item, async = True)
    jobs.append(job)
for job in jobs:
    print("Waiting for CHK")
    putCHKs.append(job.wait())
pickle.dump(putCHKs,  open('./badjobs.txt', 'w'))

while True:
    print("We arrived in the endless badlands (We are calling our inserts and inserting 10 new ones at the end)")
    for CHK in putCHKs:
        fcpPort = random.randint(lowestfcpport,  highestfcpport)
        node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.FATAL)
        node.get(CHK, async = True,  timeout = 360,  ignoreDS = True)
    print("Tried to get each of our corrupted files!")
    putfiles(dirList)
    time.sleep(random.randint(3,  10))
    
