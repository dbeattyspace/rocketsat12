#!/usr/bin/env bash

# So permissions aren't all weird
su debian

cd /home/debian/rocketsat12

python3 /home/debian/rocketsat12/mission_flight_code.py &>> /home/debian/rocketsat12/python.log &


