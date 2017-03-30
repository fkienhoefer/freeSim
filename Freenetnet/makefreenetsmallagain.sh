#!/bin/bash
#
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

JAVA_OPTS='-Xms256m -Xmx1024m'

while true
do
	# Paths to required libraries
	MAINJAR=$SCRIPT_DIR/freenet.jar
	EXTJAR=$SCRIPT_DIR/freenet-ext.jar
	BCJAR=$SCRIPT_DIR/bcprov-jdk15on-154.jar
	WRAPPERJAR=$SCRIPT_DIR/wrapper.jar
	INITEMPLATE=$SCRIPT_DIR/freenet.ini.tpl

	# Configuration values
	TARGET_IP=127.0.0.1
	NUM_SEED_NODES=2
	NUM_OPENNET_PEERS=50

	# Maps to node.listenPort
	LOWEST_DARKNET_PORT=34463
	# Maps to node.opennet.listenPort
	LOWEST_OPENNET_PORT=14833
	# Maps to fcp.port
	LOWEST_FCP_PORT=9481
	# Maps to fproxy.port
	LOWEST_HTTP_PORT=8888

	# Bandwidth values taken from the Freenet first start wizard
	INPUT_LIMITS[0]=262144
	INPUT_LIMITS[1]=393216
	INPUT_LIMITS[2]=524288
	INPUT_LIMITS[3]=786432
	INPUT_LIMITS[4]=1310720
	INPUT_LIMITS[5]=1310720
	INPUT_LIMITS[6]=2097152
	OUTPUT_LIMITS[0]=16384
	OUTPUT_LIMITS[1]=16384
	OUTPUT_LIMITS[2]=32768
	OUTPUT_LIMITS[3]=65536
	OUTPUT_LIMITS[4]=65536
	OUTPUT_LIMITS[5]=327680
	OUTPUT_LIMITS[6]=2097152


	# initiate globally used configuration variables
	OPORT=$LOWEST_OPENNET_PORT
	DPORT=$LOWEST_DARKNET_PORT
	FPORT=$LOWEST_FCP_PORT
	HPORT=$LOWEST_HTTP_PORT

	# launch seed nodes
	for (( INST=0; INST<$NUM_SEED_NODES; INST++ )); do


	OPORT=$(( $OPORT + 1 ))
	DPORT=$(( $DPORT + 1 ))
	FPORT=$(( $FPORT + 1 ))
	HPORT=$(( $HPORT + 1 ))
	done

	# launch opennet nodes
	for (( INST=0; INST<$NUM_OPENNET_PEERS; INST++ )); do


	cd opennet_$OPORT
	cd logs

	rm freenet-latest.log

	cd ..
	cd ..

	OPORT=$(( $OPORT + 1 ))
	DPORT=$(( $DPORT + 1 ))
	FPORT=$(( $FPORT + 1 ))
	HPORT=$(( $HPORT + 1 ))
	done
	sleep(100)

done
