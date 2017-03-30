#!/usr/bin/env python2

import os,  math,  pickle,  uuid, random
#amount_of_Nodes = raw_input("How many Nodes are in the network? ")
#cachesize_kb = raw_input("Please enter a short KSK key name: ")

amount_of_Nodes = 10
cachesize_byte = 100000000
filesize = 100000 #000

iterations = math.trunc(((amount_of_Nodes*cachesize_byte)/filesize)/10)
uriList = []
for i in range(1, 101):
    sfile= 'file' + str(i)
    with open('./Test/'+sfile, 'wb') as fout:
        fout.write(os.urandom(filesize)) # replace 1024 with size_kb if not unreasonably large
