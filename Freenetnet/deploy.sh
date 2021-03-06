#!/bin/bash
#
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

JAVA_OPTS='-Xms256m -Xmx1024m'

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

# create temp file to hold the generated freenet.ini-files
TMPFILE=`mktemp`
SEEDFILE=`mktemp`

# initiate globally used configuration variables
OPORT=$LOWEST_OPENNET_PORT
DPORT=$LOWEST_DARKNET_PORT
FPORT=$LOWEST_FCP_PORT
HPORT=$LOWEST_HTTP_PORT

# launch seed nodes
for (( INST=0; INST<$NUM_SEED_NODES; INST++ )); do

let INPUT_BW=${INPUT_LIMITS[$(( $NUM_LIMITS - 1 ))]}
let OUTPUT_BW=${OUTPUT_LIMITS[$(( $NUM_LIMITS - 1 ))]}

echo "Setting up seed node $INST with opennet port $OPORT"

mkdir seed_$OPORT

# generate and copy ini file
sed -e s/?OPENNET_PORT?/$OPORT/ \
    -e s/?DARKNET_PORT?/$DPORT/ \
    -e s/?HTTP_PORT?/$HPORT/ \
    -e s/?FCP_PORT?/$FPORT/ \
    -e s/?OPENNET?/true/ \
    -e s/?SEEDNODE?/true/ \
    -e s/?PEERNODE?/false/ \
    -e s/?INPUT_BW?/$INPUT_BW/ \
    -e s/?OUTPUT_BW?/$OUTPUT_BW/ \
    -e s/?IP?/$TARGET_IP/ \
    -e s/?LOGLVL?/INFO/ \
$INITEMPLATE > $TMPFILE 

cp $TMPFILE seed_$OPORT/freenet.ini

# copy libraries
cp $MAINJAR $EXTJAR $BCJAR $WRAPPERJAR seed_$OPORT

# run freenet
cd seed_$OPORT
nohup java $JAVA_OPTS -Djava.net.preferIPv4Stack=true -cp ./freenet-ext.jar:./freenet.jar:./bcprov-jdk15on-154.jar:./wrapper.jar:/usr/share/java/jna-platform-4.1.0.jar:/usr/share/java/jna-4.1.0.jar freenet.node.NodeStarter > stdout.log 2>&1 &
cd ..

# copy node ref
echo -n "Waiting for seed node ref ..."
sleep 30
wget http://127.0.0.1:$HPORT/strangers/myref.fref -O - >> $SEEDFILE
echo "Done"

OPORT=$(( $OPORT + 1 ))
DPORT=$(( $DPORT + 1 ))
FPORT=$(( $FPORT + 1 ))
HPORT=$(( $HPORT + 1 ))
done

# launch opennet nodes
for (( INST=0; INST<$NUM_OPENNET_PEERS; INST++ )); do

let INPUT_BW=${INPUT_LIMITS[$(( $NUM_LIMITS - 1 ))]}
let OUTPUT_BW=${OUTPUT_LIMITS[$(( $NUM_LIMITS - 1 ))]}

echo "Setting up opennet node $INST with opennet port $OPORT"

mkdir opennet_$OPORT

# generate and copy ini file
sed -e s/?OPENNET_PORT?/$OPORT/ \
    -e s/?DARKNET_PORT?/$DPORT/ \
    -e s/?HTTP_PORT?/$HPORT/ \
    -e s/?FCP_PORT?/$FPORT/ \
    -e s/?OPENNET?/true/ \
    -e s/?SEEDNODE?/false/ \
    -e s/?PEERNODE?/true/ \
    -e s/?INPUT_BW?/$INPUT_BW/ \
    -e s/?OUTPUT_BW?/$OUTPUT_BW/ \
    -e s/?IP?/$TARGET_IP/ \
    -e s/?LOGLVL?/FATAL/ \
$INITEMPLATE > $TMPFILE 

cp $TMPFILE opennet_$OPORT/freenet.ini
cp $SEEDFILE opennet_$OPORT/seednodes.fref

# copy libraries
cp $MAINJAR $EXTJAR $BCJAR $WRAPPERJAR opennet_$OPORT

# run freenet
cd opennet_$OPORT
nohup java $JAVA_OPTS -Djava.net.preferIPv4Stack=true -cp ./freenet-ext.jar:./freenet.jar:./bcprov-jdk15on-154.jar:./wrapper.jar:/usr/share/java/jna-platform-4.1.0.jar:/usr/share/java/jna-4.1.0.jar freenet.node.NodeStarter > stdout.log 2>&1 &
cd ..

OPORT=$(( $OPORT + 1 ))
DPORT=$(( $DPORT + 1 ))
FPORT=$(( $FPORT + 1 ))
HPORT=$(( $HPORT + 1 ))
done


# delete temp file used for freenet configurations
rm $TMPFILE
sleep 60
rm $SEEDFILE
