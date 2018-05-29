import os
import threading
import subprocess as sp
import time
import queue
import shlex

from mission_functions import downlink, transfer_function

## Kill other hackrf stuff if it's happening
sp.run(shlex.split('killall -9 hackrf_transfer'))

## HackRF Config
hackrf_transfer_parameters = {
    '-f' : 2887500000, # Frequency, [ Hz ]
    '-s' : 8000000,    # Sample Rate, [ Hz ] set back to 8000000
    '-l' : 0, # Intermediate Frequency (IF) Gain, post-mixing gain [ dB ]
    '-g' : 10, # BaseBand (BB) Gain, *IVAN FILL IN WHAT DO*, [ dB ]
    '-w' : ' ', # Saving method. -w is autonamed .wav file, -r needs filename argument
}

## File Administration
try:
    os.mkdir('mission_files')
except FileExistsError:
    # This directory should exist, just making sure
    pass

# Total time beaglebone is powered on
total_mission_time = 255 #change back to 255

# Time before mission end that we want to save things and power off
end_buffer = 15

# Mission duration
collection_duration = total_mission_time - end_buffer

# Start time for measuring time elapsed and for file naming
start_timestamp = time.time()
start_time = time.strftime('%b_%m_%H:%M:%S')

# Create directory where log file and data files will be saved
file_index = 0
while os.path.exists('mission_files/datalog{}'.format(file_index)):
    file_index += 1
data_directory = 'mission_files/datalog{}'.format(file_index)
os.mkdir(data_directory)

# Set up the log file, initialize as empty
log_filename = '/home/debian/rocketsat12/{}/mission.log'.format(data_directory)
log_lock = threading.Lock()
open(log_filename, 'w+').close()

## Downlink
downlink_queue = queue.Queue()
downlink_queue.put('Running Mission Code. Data directory {}'.format(data_directory))
downlink_queue.put('BB Start Time: {}'.format(start_time))

# Start downlink thread
downlink_thread = threading.Thread(target=downlink, args=(downlink_queue, log_filename, log_lock), daemon=True)
downlink_thread.start()

## HackRF Data Saving
parameters = ' '.join([str(key) + ' ' + str(value) for key, value in zip(hackrf_transfer_parameters.keys(), hackrf_transfer_parameters.values())])

os.chdir(data_directory)
# Outer while loop to make sure that it doesn't re-run after time expires
while (time.time() - start_timestamp) < collection_duration:
    transfer_function(parameters, downlink_queue, start_timestamp, collection_duration)


os.chdir('/home/debian/rocketsat12')

# Won't work if ssh'd in
# os.system('systemctl poweroff')
