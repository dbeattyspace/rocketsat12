import os
import threading
import subprocess as sp
import time
import queue
import shlex

from mission_functions import downlink, transfer_function

# MISSION PARAMETERS
frequency = 2888500000 # Hz
samplerate = 5000000 # samples/sec
if_gain = 8 # dB
bb_gain = 10 # dB

# FILE PARAMETERS
length = 20 # sec
numberoffiles = 15
downlink_file = 4

# Kill other hackrf stuff if it's happening
sp.run(shlex.split('killall -9 hackrf_transfer'))

# File Administration
try:
    os.mkdir('mission_files')
except FileExistsError:
    # This directory should exist, just making sure
    pass

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
log_filename = '/home/pi/rocketsat12/{}/mission.log'.format(data_directory)
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
    '-f' : frequency, # Frequency, [ Hz ]
    '-s' : samplerate,    # Sample Rate, [ Hz ]
    '-n' : samplerate*length,   # Number of Samples
    '-l' : if_gain, # Intermediate Frequency (IF) Gain, post-mixing gain [ dB ]
    '-g' : bb_gain, # BaseBand (BB) Gain, *IVAN FILL IN WHAT DO*, [ dB ]
    '-w' : ' ', # Saving method. -w is autonamed .wav file, -r needs filename argument
}
hackrf_transfer_parameters_down = {
    '-f' : frequency, # Frequency, [ Hz ]
    '-s' : samplerate,    # Sample Rate, [ Hz ]
    '-n' : 200000,   # Number of Samples
    '-l' : if_gain, # Intermediate Frequency (IF) Gain, post-mixing gain [ dB ]
    '-g' : bb_gain, # BaseBand (BB) Gain, *IVAN FILL IN WHAT DO*, [ dB ]
    '-w' : ' ', # Saving method. -w is autonamed .wav file, -r needs filename argument
}
hackrf_transfer_parameters_plus_one = {
    '-f' : frequency+1e6, # Frequency, [ Hz ]
    '-s' : samplerate,    # Sample Rate, [ Hz ]
    '-n' : samplerate*length,   # Number of Samples
    '-l' : if_gain, # Intermediate Frequency (IF) Gain, post-mixing gain [ dB ]
    '-g' : bb_gain, # BaseBand (BB) Gain, *IVAN FILL IN WHAT DO*, [ dB ]
    '-w' : ' ', # Saving method. -w is autonamed .wav file, -r needs filename argument
}
hackrf_transfer_parameters_minus_one = {
    '-f' : frequency-1e6, # Frequency, [ Hz ]
    '-s' : samplerate,    # Sample Rate, [ Hz ]
    '-n' : samplerate*length,   # Number of Samples
    '-l' : if_gain, # Intermediate Frequency (IF) Gain, post-mixing gain [ dB ]
    '-g' : bb_gain, # BaseBand (BB) Gain, *IVAN FILL IN WHAT DO*, [ dB ]
    '-w' : ' ', # Saving method. -w is autonamed .wav file, -r needs filename argument
}


# Combines Hack RF Parametersprocess = transfer_function(parameters, downlink_queue, counter)

parameters = ' '.join([str(key) + ' ' + str(value) for key, value in zip(hackrf_transfer_parameters.keys(), hackrf_transfer_parameters.values())])
parameters_plus_one = ' '.join([str(key) + ' ' + str(value) for key, value in zip(hackrf_transfer_parameters_plus_one.keys(), hackrf_transfer_parameters_plus_one.values())])
parameters_minus_one = ' '.join([str(key) + ' ' + str(value) for key, value in zip(hackrf_transfer_parameters_minus_one.keys(), hackrf_transfer_parameters_minus_one.values())])
parameters_down = ' '.join([str(key) + ' ' + str(value) for key, value in zip(hackrf_transfer_parameters_down.keys(), hackrf_transfer_parameters_down.values())])

# Delay if powering on with gse line
#time.sleep(179)

# Calls Hack RF Transfer Function
counter = 1
while counter<=numberoffiles: # total number of files
    if counter==downlink_file: # short file to downlink
        process = transfer_function(parameters_down, downlink_queue, counter)
        if process==0: # check if successful
            counter += 1
    else: # normal file size
        setfreq = counter%3
        if setfreq == 1:
            process = transfer_function(parameters, downlink_queue, counter)
        elif setfreq == 2:
            process = transfer_function(parameters_plus_one, downlink_queue, counter)
        else:
            process = transfer_function(parameters_minus_one, downlink_queue, counter)
        if process==0: # check if successful
            counter += 1

# Gets end of code stop times
stop_timestamp = time.time()
stop_time = time.strftime('%b %d %Y %H:%M:%S')

# Prints process complete to log files
downlink_queue.put('\nFlight Code Completd: {}'.format(stop_time))
downlink_queue.put('Flight Code Time Elapsed: {} seconds'.format(stop_timestamp-start_timestamp))
print('\nFlight Code Completed: {}'.format(stop_time))
print('Flight Code Time Elapsed: {} seconds'.format(stop_timestamp-start_timestamp))
print('\n\n---------------------------------------------------\n\n')

# Prevents exiting for final info for logs
time.sleep(5)
