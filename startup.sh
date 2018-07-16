#!/usr/bin/env bash

# So permissions aren't all weird
su pi

cd /home/pi/rocketsat12

python3 /home/pi/rocketsat12/mission_flight_code.py &>> /home/pi/rocketsat12/python.log &


