#!/usr/bin/env bash

COUNTER=0
MAIN_SCRIPT="main.new.py"

NODES=15 # Number of nodes
TIMEEMU=600 # Time of the emulation in seconds
SIZE=800 # Size of the network, 300m x 300m
SPEED=10 # Speed in m/s
PAUSE=0 # Pause time of the nodes in seconds

UPDATE_PERIOD=10 #Update data every UPDATE seconds for visceral

export NS3_HOME=/home/ubuntu/workspace/bake/source/ns-3-dev

# We create everything
python3 ${MAIN_SCRIPT} -n ${NODES} -t ${TIMEEMU} -s ${SIZE} -ns ${SPEED} -np ${PAUSE} create
# We run the NS3 simulation
python3 ${MAIN_SCRIPT} -n ${NODES} -t ${TIMEEMU} -s ${SIZE} -ns ${SPEED} -np ${PAUSE} ns3

while [  $COUNTER -lt 1 ]; do

    DATENOW=$(date +"%y_%m_%d_%H_%M")

    # Making a backup from the last iteration's logs
    echo "---------------------------"
    echo ${DATENOW}
    echo "---------------------------"
    mkdir -p var/archive/${DATENOW}
    mv var/log/* var/archive/${DATENOW}/

    # Start translate data from var/log to .json for visceral
    python transfrom.py -p ${UPDATE_PERIOD} -t ${TIMEEMU} &

    # Run the emulation
    python3 ${MAIN_SCRIPT} -n ${NODES} -t ${TIMEEMU} -s ${SIZE} -ns ${SPEED} -np ${PAUSE} emulation

        let COUNTER=COUNTER+1
done

# We destroy everything cause we don't need it anymore
python3 ${MAIN_SCRIPT} -n ${NODES} -t ${TIMEEMU} -s ${SIZE} -ns ${SPEED} -np ${PAUSE} destroy
