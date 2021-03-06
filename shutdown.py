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
numberOfNodes = 3+100+5
for i in range((numberOfNodes)):
    fcpPort = 9481 + i
    node = fcp.FCPNode(host=fcpHost, port = fcpPort,  verbosity=fcp.DETAIL)
    nodes.append(node)
i = 0
for item in nodes:
    item.shutdown()
