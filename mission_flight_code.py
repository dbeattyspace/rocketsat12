import os
import threading
import subprocess as sp
import time
import queue
import shlex

from mission_functions import downlink

## HackRF Config
hackrf_transfer_parameters = {
    '-f' : 2893000000, # Frequency, [ Hz ]
    '-s' : 8000000,    # Sample Rate, [ Hz ]
    '-w' : ' ', # Saving method. -w is autonamed .wav file, -r needs filename argument
}

## File Administration
try:
    os.mkdir('mission_files')
except FileExistsError:
    # This directory should exist, just making sure
    pass

start_time = time.strftime('%b_%m_%H:%M:%S')

# Create directory where log file and data files will be saved
data_directory = 'mission_files/{}'.format(start_time)
os.mkdir(data_directory)

# Set up the log file, initialize as empty
log_filename = '{}/mission.log'.format(data_directory)
log_lock = threading.Lock()
open(log_filename, 'w+').close()

## Downlink
downlink_queue = queue.Queue()
downlink_queue.put('Running Mission Code: {}'.format(start_time))

# Start downlink thread
downlink_thread = threading.Thread(target=downlink, args=(downlink_queue, log_filename, log_lock), daemon=True)
downlink_thread.start()

## HackRF Data Saving

parameters = ' '.join([str(key) + ' ' + str(value) for key, value in zip(hackrf_transfer_parameters.keys(), hackrf_transfer_parameters.values())])

cmd = 'hackrf_transfer {}'.format(parameters)

hackrf_process = sp.Popen(shlex.split(cmd), stdout=sp.PIPE, stderr=sp.PIPE)

for i in range(10):
    time.sleep(1)
    output = hackrf_process.communicate()
    print(output)
    print(hackrf_process.poll())

hackrf_process.kill()

time.sleep(3)
import sys
sys.exit(0)