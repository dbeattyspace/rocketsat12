import serial
import time
import threading
import os
import subprocess as sp
import shlex
import signal

def downlink(downlink_queue, log_filename, log_lock):
    ser = serial.Serial()
    ser.port = '/dev/ttyO2'
    ser.baudrate = 19200
    ser.timeout = 1
    ser.open()

    print('Started downlink')

    while True:
        while not downlink_queue.empty():
            message = downlink_queue.get() + '\n'
            # Add print to log file and terminal window
            ser.write(message.encode())

            with log_lock:
                with open(log_filename, 'a') as f:
                    f.write(message)

            print(message)

        time.sleep(1)


def transfer_function(parameters, downlink_queue, start_timestamp, collection_duration):
    cmd = 'hackrf_transfer {}'.format(parameters)

    downlink_queue.put('Starting hackrf_transfer')
    hackrf_process = sp.Popen(shlex.split(cmd), stdout=sp.PIPE)

    # Checks to make sure that the process is still running
    # None is good, it means it's still running
    while hackrf_process.poll() is None:
        current_time = time.strftime('%b_%m_%H:%M:%S')
        downlink_queue.put('Polling process: {}'.format(current_time))
        if (time.time() - start_timestamp) > collection_duration:
            break
        time.sleep(1)

    # If the process poll returns 'not None' it will reach here
    # Will kill the process, and start over
    kill_time = time.strftime('%b_%m_%H:%M:%S')
    downlink_queue.put('Killing HackRF Process: {}'.format(kill_time))
    hackrf_process.send_signal(signal.SIGINT)
    return

