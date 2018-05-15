import os
import threading
import subprocess as sp
import time
import queue

from mission_functions import downlink

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

## Actual Data Saving

for i in range(10):
    downlink_queue.put('Gee Willikers here\'s some data: {}'.format(i ** 2))
    time.sleep(0.5)

time.sleep(3)
import sys
sys.exit(0)
