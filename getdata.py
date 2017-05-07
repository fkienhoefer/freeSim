#!/usr/bin/env python2
import os, random,  pickle,  time,  ast


seedNodes = 2
openNodes = 50
monitorNodes = 5
attackerNodes = 0

lowestOpenPort = 14833 + seedNodes
highestOpenPort = lowestOpenPort + openNodes-1
lowestStudyPort = highestOpenPort+1
highestStudyPort = lowestStudyPort + monitorNodes + attackerNodes -1

networkcachesize = 7 # *100mb, round this to nearest int you want it to be

SFF =[]
SIRS = []
combined = []
for i in range(14833,  14835):
    if (os.path.isfile('/home/felix/freenet/Freenetnet/seed_'+str(i) +'/madeSFF.txt')):
        with open('/home/felix/freenet/Freenetnet/seed_'+str(i) +'/madeSFF.txt', 'rb') as f:
            lines = [line.rstrip('\n') for line in f] 
            SFF.extend(lines)
        if (os.path.isfile('/home/felix/freenet/Freenetnet/seed_'+str(i) +'/successInRequestsender.txt')):
            with open('/home/felix/freenet/Freenetnet/seed_'+str(i) +'/successInRequestsender.txt', 'rb') as f:
                lines = [line.rstrip('\n') for line in f] 
                SIRS.extend(lines)

for i in range(lowestOpenPort,  highestOpenPort):
    if (os.path.isfile('/home/felix/freenet/Freenetnet/opennet_'+str(i) +'/madeSFF.txt')):
        with open('/home/felix/freenet/Freenetnet/opennet_'+str(i) +'/madeSFF.txt', 'rb') as f:
            lines = [line.rstrip('\n') for line in f] 
            SFF.extend(lines)
        if (os.path.isfile('/home/felix/freenet/Freenetnet/opennet_'+str(i) +'/successInRequestsender.txt')):
            with open('/home/felix/freenet/Freenetnet/opennet_'+str(i) +'/successInRequestsender.txt', 'rb') as f:
                lines = [line.rstrip('\n') for line in f] 
                SIRS.extend(lines)
                
for i in range(lowestStudyPort,  highestStudyPort):
    if (os.path.isfile('/home/felix/freenet/Freenetnet/study_'+str(i) +'/madeSFF.txt')):
        with open('/home/felix/freenet/Freenetnet/study_'+str(i) +'/madeSFF.txt', 'rb') as f:
            lines = [line.rstrip('\n') for line in f] 
            SFF.extend(lines)
        if (os.path.isfile('/home/felix/freenet/Freenetnet/study_'+str(i) +'/successInRequestsender.txt')):
            with open('/home/felix/freenet/Freenetnet/study_'+str(i) +'/successInRequestsender.txt', 'rb') as f:
                lines = [line.rstrip('\n') for line in f] 
                SIRS.extend(lines)

                
SFF = map(lambda x : eval(x), SFF )
SIRS = map(lambda x: ast.literal_eval(x),  SIRS)

for single in SFF:
    for sender in SIRS:
        if (single['NodeCHK for SFFKey'] == sender['key']):
            #dict ={'CHK': '@CHK', 'htl':'0'}
            #dict['CHK'] = single['origURI']
            #dict['htl'] = sender['htl']
            combined.append((single['origURI'],  int(sender['htl'])))
            #combined.append(dict)
print(combined)

i =1
bool = False
while bool == False:
    if not (os.path.isfile('./CHKs+htl'+str(i)+'.txt')):
        with open('./CHKs+htl'+str(i)+'.txt', "wb") as f:
            pickle.dump(combined, f)
            bool = True
    i+=1

for i in range(14833,  14835):
    if (os.path.isfile('/home/felix/freenet/Freenetnet/seed_'+str(i) +'/madeSFF.txt')):
        os.remove('/home/felix/freenet/Freenetnet/seed_'+str(i) +'/madeSFF.txt')

    if (os.path.isfile('/home/felix/freenet/Freenetnet/seed_'+str(i) +'/successInRequestsender.txt')):
        os.remove('/home/felix/freenet/Freenetnet/seed_'+str(i) +'/successInRequestsender.txt')    
    
for i in range(lowestOpenPort,  highestOpenPort):
    if (os.path.isfile('/home/felix/freenet/Freenetnet/opennet_'+str(i) +'/madeSFF.txt')):
        os.remove('/home/felix/freenet/Freenetnet/opennet_'+str(i) +'/madeSFF.txt')

    if (os.path.isfile('/home/felix/freenet/Freenetnet/opennet_'+str(i) +'/successInRequestsender.txt')):
        os.remove('/home/felix/freenet/Freenetnet/opennet_'+str(i) +'/successInRequestsender.txt')

for i in range(lowestStudyPort,  highestStudyPort):
    if (os.path.isfile('/home/felix/freenet/Freenetnet/study_'+str(i) +'/madeSFF.txt')):
        os.remove('/home/felix/freenet/Freenetnet/study_'+str(i) +'/madeSFF.txt')

    if (os.path.isfile('/home/felix/freenet/Freenetnet/study_'+str(i) +'/successInRequestsender.txt')):
        os.remove('/home/felix/freenet/Freenetnet/study_'+str(i) +'/successInRequestsender.txt')
