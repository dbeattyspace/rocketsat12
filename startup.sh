#!/usr/bin/env bash

# If connected to internet, gives time to check time. Can remove for non-internet tests/flight
sleep 10

cd /home/debian/rocketsat12

printf "\n\n$(date)\n" >> /home/debian/rocketsat12/mission.log

python3 /home/debian/rocketsat12/mission_flight_code.py &>> /home/debian/rocketsat12/python.log &


