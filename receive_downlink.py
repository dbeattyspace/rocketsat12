##################################################################
# Miura 2: Receive Downlinked Data (receive_downlink.py)
# Created: 6/4/2018
# Modified: 6/4/2018
# Purpose: Receive downlinked data and write to wav file
##################################################################

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

print("Serial object initialized...")
print("Waiting for downlink...")

# sets variable to track completion
completed = False

# creates new wav file to hold data
file_index = 0
while os.path.exists('downlink{}.wav'.format(file_index)):
	file_index += 1
filename = 'downlink{}.wav'.format(file_index)
subprocess.run(shlex.split('touch {}'.format(filename)))
print('New File Created: {}'.format(filename))

# downlinks data and writes to wav file
while not completed:
	if serial.inWaiting(): # waits to serial to receive data
		print('Downlink Started: {}'.format(time.strftime('%b %d %Y %H:%M:%S')))
		startofdownlink = serial.read(4) # should read 1 2 3 4
		data = serial.read(400000) # 400 Kb of data
		print('Downlink Completed: {}'.format(time.strftime('%b %d %Y %H:%M:%S')))
		wav_file = wave.open(filename, mode='wb') # opens wav file
		wav_file.setnchannels(2) # 2 bytes per sample
		wav_file.setsampwidth(1)
		wav_file.setframerate(5000000) # 5 MHz sample rate
		wav_file.setnframes(200000) # 2e6 frames of data
		print('File Write Started: {}'.format(time.strftime('%b %d %Y %H:%M:%S')))
		wav_file.writeframes(data) # writes data to file
		wav_file.writeframes(b'') # adds header to file
		wav_file.close() # closes wav file
		print('File Write Completed: {}'.format(time.strftime('%b %d %Y %H:%M:%S')))
		completed = True # sets complete to true
