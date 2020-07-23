#!/bin/bash
# Bash script that loops and runs the python Tautulli IP enforcment script


## run while loop to display date and hostname on screen ##
while [ : ]
do
    clear
    cd /home/dean/TautulliBanEnforcer && python3 tautulliIpEnforcer.py
    sleep 2
    echo "Sleeping..."
    sleep 10
done