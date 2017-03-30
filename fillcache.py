#!/usr/bin/env python2
import sys, os, tempfile, random, uuid,  pickle,  time


# ------------------------------------------
# first things first - import fcp module
#Maybe randomize used nodes? Possibly increased perf...

import fcp
fcpHost = "127.0.0.1"
seedNodes = 2
openNodes = 50
lowestfcpport = 9481+seedNodes
highestfcpport = lowestfcpport + openNodes

networkcachesize = 70 # *10mb, round this to nearest int you want it to be

#Lists for done *jobs
putJobs =  []
putCHKs = []
#Empty textfiles that save said lists
#pickle.dump(putJobs,  open('./putjobs.txt', 'wb'))
with open('./putjobs.txt', 'wb') as f:
    pickle.dump(putJobs, f)
#pickle.dump(putJobs,  open('./getjobs.txt', 'wb'))

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







if ((len(dirList))%(openNodes) ==  0):
    splitdirList = split(dirList,  openNodes) #If inserting Data is slow, check if len(dirList
else: 
    splitdirList = []
    print ("Error while dividing up files for the single Nodes")
    print (divmod(len(dirList), openNodes) )

#Guts of filling in chache.
#for |networkcachesize| fills in a gig of Data, by iterating through the Nodes based on their fcpPort and letting each Node put in a Chunk of the Dataset
i = 0
CHKList = []
while i < networkcachesize:
    for j in range (openNodes):
        fcpPort = str(lowestfcpport + j)
        node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.FATAL)
        print("current FCP Port:" + fcpPort)
        for sfile in splitdirList[j]:
            job =  node.put('CHK@', file = './Test/'+sfile, async = True)
            putJobs.append(job)
    
    for job in putJobs:
            print ("You have entered THE DARK ZONE!")
            # we can poll the job
            if job.isComplete():
                print("Yay! job complete")
                putCHKs.append(job.getResult())
            else:
                # or we can await its completion
                print ("Waiting on a Job")
                result = job.wait()
    #pickle.dump(putCHKs,  open('./putjobs.txt', 'w'))
    with open('./putjobs.txt', 'wb') as f:
        pickle.dump(putJobs, f)
    
    changefileset(dirList)
    print("100mb of files successsfully put!")
    i += 1
    time.sleep(30)

#
#for (sfile, uri, state) in uriTable:
#    #if state == 0:
#        uriTable[uriTable.index((sfile, uri, state))] = (sfile,  uri,  1)
#        fcpPort = random.randint(9482, 9491)#9500)
#        print ("\n Port:" + str(fcpPort) + "\n")
#        node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.DETAIL)
#        job = node.put('CHK@', file = './Test/'+sfile, async = True) #Option fuer lokales lookup deaktivieren!
#        putJobs.append(job)
##    else:
##        uriTable[uriTable.index((sfile, uri, state))] = (sfile,  uri,  1)
#        
#pickle.dump(uriTable,  open('./URI_table.txt', 'wb'))
#    
#for job in putJobs:
#            print ("You have entered THE DARK ZONE!")
#            # we can poll the job
#            if job.isComplete():
#                print("Yay! job complete")
#                putCHKs.append(job.getResult())
#            else:
#                # or we can await its completion
#                print ("Waiting on a Job")
#                result = job.wait()
#                
#pickle.dump(putCHKs,  open('./putjobs.txt', 'a'))
#getJobs = []    
#
#print ("\n Step 1 COMPLETE! \n Initiating phase 2: retrieving files... \n" )
#for CHK in putCHKs:
#    fcpPort = random.randint(9482, 9491)#9500)
#    print ("\n Port:" + str(fcpPort) + "\n")
#    node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.FATAL) #was fcp.FATAL
#    job = node.get(CHK, async = True,  timeout = 360 ,  ignoreDS = True) #,  verbosity = 1)
#    getJobs.append(job)
#allGetDone = False
#doneJobs = []
#while (allGetDone == False): 
#    print ("\n You have entered THE SUPER ZONE! \n")  
#    for job in getJobs:
#        allGetDone = True    
#        # we can poll the job
#        if job.isComplete():
#            print("Yay! job complete")
#            pickle.dump(job.id ,  open('./getjobs.txt', 'a'))
#            if job not in doneJobs:
#                doneJobs.append(job)
#            #getJobs[getJobs.index((job,  isCompleted))] = (job,  True)
#            
#        else:
#            # or we can await its completion
#            print(job.getResult())
#            allGetDone = False
#        time.sleep(3)
#        print("Jobs done" + str(len(doneJobs)))
print("Isch gloobs net, die Scheisse geht!")

