import os
import threading
import subprocess as sp
import time
import queue
import shlex

from mission_functions import downlink, transfer_function

# Kill other hackrf stuff if it's happening
sp.run(shlex.split('killall -9 hackrf_transfer'))

# File Administration
try:
    os.mkdir('mission_files')
except FileExistsError:
    # This directory should exist, just making sure
    pass

# Total time beaglebone is powered on
total_mission_time = 255 #change back to 255

# Time to wait before starting downlink of wav file
wav_downlink_buffer = 20

# Time before mission end that we want to save things and power off
end_buffer = 15

# Mission duration
collection_duration = (total_mission_time - end_buffer)

# Start time for measuring time elapsed and for file naming
start_timestamp = time.time()
start_time = time.strftime('%b %d %Y %H:%M:%S')

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

# Creates downlink queue
downlink_queue = queue.Queue()
downlink_queue.put('Flight Code Started: {}'.format(start_time))
downlink_queue.put('Data Directory: {}'.format(data_directory))

# Prints to python.log
print('\nFlight Code Started: {}'.format(start_time))
print('Data Directory: {}'.format(data_directory))

# Start downlink thread
downlink_thread = threading.Thread(target=downlink, args=(downlink_queue, log_filename, log_lock), daemon=True)
downlink_thread.start()

# Change to directory to save data
os.chdir(data_directory)

# Hack RF Parameters
hackrf_transfer_parameters = {
    '-f' : 2888000000, # Frequency, [ Hz ]
    '-s' : 10000000,    # Sample Rate, [ Hz ] set back to 8000000
    '-n' : 75000000*2,   # Number of Samples
    '-l' : 8, # Intermediate Frequency (IF) Gain, post-mixing gain [ dB ]
    '-g' : 10, # BaseBand (BB) Gain, *IVAN FILL IN WHAT DO*, [ dB ]
    '-w' : ' ', # Saving method. -w is autonamed .wav file, -r needs filename argument
}
hackrf_transfer_parameters_down = {
    '-f' : 2888000000, # Frequency, [ Hz ]
    '-s' : 10000000,    # Sample Rate, [ Hz ] set back to 8000000
    '-n' : 200000,   # Number of Samples
    '-l' : 8, # Intermediate Frequency (IF) Gain, post-mixing gain [ dB ]
    '-g' : 10, # BaseBand (BB) Gain, *IVAN FILL IN WHAT DO*, [ dB ]
    '-w' : ' ', # Saving method. -w is autonamed .wav file, -r needs filename argument
}

# Combines Hack RF Parameters
parameters = ' '.join([str(key) + ' ' + str(value) for key, value in zip(hackrf_transfer_parameters.keys(), hackrf_transfer_parameters.values())])
parameters_down = ' '.join([str(key) + ' ' + str(value) for key, value in zip(hackrf_transfer_parameters_down.keys(), hackrf_transfer_parameters_down.values())])

# Calls Hack RF Transfer Function
counter = 1
while counter<=15: # 15 total files
    if counter==2: # short file to downlink
        process = transfer_function(parameters_down, downlink_queue, counter)
        if process==0: # check if successful
            counter += 1
    else: # normal file size
        process = transfer_function(parameters, downlink_queue, counter)
        if process==0: # check if successful
            counter += 1

# gets end of code stop times
stop_timestamp = time.time()
stop_time = time.strftime('%b %d %Y %H:%M:%S')

# prints process complete to log files
downlink_queue.put('\nFlight Code Completd: {}'.format(stop_time))
downlink_queue.put('Flight Code Time Elapsed: {} seconds'.format(stop_timestamp-start_timestamp))
print('\nFlight Code Completed: {}'.format(stop_time))
print('Flight Code Time Elapsed: {} seconds'.format(stop_timestamp-start_timestamp))
print('\n\n---------------------------------------------------\n\n')

# prevents exiting for final info for logs
time.sleep(5)

# Won't work if ssh'd in
# os.system('systemctl poweroff')
