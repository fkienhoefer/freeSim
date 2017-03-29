#!/usr/bin/env python2

import sys, os, tempfile, random, uuid,  pickle,  time


# ------------------------------------------
# first things first - import fcp module
#Maybe randomize used nodes? Possibly increased perf...

import fcp
fcpHost = "127.0.0.1"
fcpPort = "9485"


# ------------------------------------------
# create a node connection object
# 
# we're setting a relatively high verbosity so you
# can see the traffic

#node = fcp.FCPNode(host=fcpHost, port = fcpPort, verbosity=fcp.DETAIL)
uriTable = pickle.load(open("./URI_table.txt","rb"))

nodes =  []
numberOfNodes = 9
for i in range((2+numberOfNodes)):
    fcpPort = 9481 + i
    node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.FATAL)
    nodes.append(node.listpeers())
i = 0
for item in nodes:
        print ("Port =" + str(9481 + i))
    #    print(node.listpeers())
    #    time.sleep(8)
        i += 1
        for elem in item:
            print (elem)
            print ("\n \n")
        print(len(item))
        print ("\n next \n")
