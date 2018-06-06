import serial
import time
import threading
import os
import subprocess as sp
import shlex
import signal
import wave

def downlink(downlink_queue, log_filename, log_lock):
    ser = serial.Serial()
    ser.port = '/dev/ttyO2'
    ser.baudrate = 19200
    ser.timeout = None
    ser.open()

    downlink_file = ''
    downlinked = False

    print('Started downlink')

    while True:
        while not downlink_queue.empty():
            message = downlink_queue.get() + '\n'
            # Add print to log file and terminal window
            #ser.write(message.encode())

            with log_lock:
                with open(log_filename, 'a') as f:
                    f.write(message)

            print(message)

        current_files = os.listdir()

        if downlink_file == '':
            if len(current_files) > 3:
                for file in current_files:
                    if file.endswith('.wav') and os.path.getsize(file) == 4844:
                        downlink_file = file
                        downlink_queue.put('Downlinking File: {}'.format(downlink_file))
        elif not downlinked:
            downlink_queue.put('File Downlink Started: {}'.format(time.strftime('%b_%m_%H:%M:%S')))
            with wave.open(downlink_file) as wav_file:
                downlink_queue.put('Parameters: {}'.format(wav_file.getparams()))
                ser.write(wav_file.readframes(100000000))
            downlink_queue.put('File Downlink Complete: {}'.format(time.strftime('%b_%m_%H:%M:%S')))
            downlinked = True
        time.sleep(1)


def transfer_function(parameters, downlink_queue, start_timestamp, collection_duration):
    cmd = 'hackrf_transfer {}'.format(parameters)

    downlink_queue.put('Starting hackrf_transfer')
    hackrf_process = sp.Popen(shlex.split(cmd), stdout=sp.PIPE)

    # Checks to make sure that the process is still running
    # None is good, it means it's still running
    while hackrf_process.poll() is None:
        time.sleep(1)

    # If the process poll returns 'not None' it will reach here
    # Will kill the process, and start over
    kill_time = time.strftime('%b_%m_%H:%M:%S')
    downlink_queue.put('Killing Current HackRF Process: {}'.format(kill_time))

    return

