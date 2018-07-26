import serial
import time
import glob
from sys import platform
import wave
import shlex
import subprocess
import os

# finds computer serial port
if platform == 'linux' or platform == 'linux2':
	current_port = '/dev/ttyUSB0'
elif platform == 'darwin':
	current_port = glob.glob('/dev/tty.USA*')[0]

# sets up serial object for use
serial = serial.Serial(port=current_port,
					baudrate=19200,
					timeout=None)

print('Waiting for downlink...\n')

# downlinks data and writes to wav file
while True:
	if serial.inWaiting(): # waits to serial to receive data
		data = serial.read()
		print(data)
