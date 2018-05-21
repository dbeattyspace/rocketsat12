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
    '-f' : 2893000000, # Frequency, [ Hz ]
    '-s' : 20000000,    # Sample Rate, [ Hz ]
    '-w' : ' ', # Saving method. -w is autonamed .wav file, -r needs filename argument
}

## File Administration
try:
    os.mkdir('mission_files')
except FileExistsError:
    # This directory should exist, just making sure
    pass

# Total time beaglebone is powered on
total_mission_time = 20 #255

# Time before mission end that we want to save things and power off
end_buffer = 15

# Mission duration
collection_duration = total_mission_time - end_buffer

# Start time for measuring time elapsed and for file naming
start_timestamp = time.time()
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

while (time.time() - start_timestamp) < collection_duration:
    new_wav_file = transfer_function(parameters, downlink_queue)
    os.rename(new_wav_file, data_directory + '/' + new_wav_file)

# Won't work if ssh'd in
# os.system('systemctl poweroff')
