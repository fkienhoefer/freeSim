# freeSim
A small project simulating a pollution attack on the opennet part of freenet
consisting of a slughtly modified freenet client and several python scripts-

0. PREPARATIONS:

To prepare a simulation you will have to create two folders in the directory where
you put the python scripts one named "Bad" and one named "Test" , after that run
"badfilescreator.py" and "create files.py" once.

This is necessary to get the dataset you are going to insert into your simulated network.

1. SETTING UP SEED- AND OPENNETNODES

If the above is done set the number of seed/opennet/monitor/attacker-nodes to the desired amount
in: badnodes.py, fillcache.py, monitor.py and trafficsimulator.py.

To start Freenet we first start our seed- and opennetnodes, to do that execute "./deploy.sh"
If you want to change the number of seed- or opennetnodes edit ./deploy.sh

When the script has finished running execute "fillcache.py" and wait for it to complete.

After that is done run "trafficsimulator.py" to start the behaviour-simulation of genuine freenet-users

2. SETTING UP MONITOR AND ATTACKERNODES:

To start the additonal need nodes execute ./attack.sh.
This will bring up a prompt asking how many nodes are already online (Keep track of the number you have already deployed!
Seednodes do count!)and ask you for the amount of nodes you want to deploy in addition to that.

If you just want the monitors:
Just add the number of monitornodes you configured in monitor.py and run monitor.py

If you want monitors and attackers:
Add the number of monitors and desired attackers and add that amount. After that run monitor.py and badnodes.py


