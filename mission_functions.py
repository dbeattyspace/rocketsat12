import serial
import time
import threading
import os
import subprocess as sp
import shlex
import signal
import wave
import RPi.GPIO as GPIO

write_led_pin = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(write_led_pin, GPIO.OUT)

def downlink(downlink_queue, log_filename, log_lock):
    # serial setup
    ser = serial.Serial()
    ser.port = '/dev/ttyAMA0'
    ser.baudrate = 19200
    ser.timeout = None
    ser.open()

    # setup for file being downlinked
    downlink_file = ''
    downlinked = False

    # reading downlink queue
    while True:
        while not downlink_queue.empty():
            message = downlink_queue.get() + '\n'
            # enable to downlink messages
            #ser.write(message.encode())

            # writes to log file
            with log_lock:
                with open(log_filename, 'a') as f:
                    f.write(message)
        # gets current files in directory
        current_files = os.listdir()

        # if file to downlink hasn't been found
        if downlink_file == '':
            if len(current_files) > 3:
                for file in current_files:
                    # look for file of correct size
                    if file.endswith('.wav') and os.path.getsize(file) == 400044:
                        downlink_file = file
        # if found but not yet downlinked
        elif not downlinked:
            downlink_queue.put('\nFile Downlink: {}'.format(downlink_file))
            downlink_queue.put('File Downlink Started: {}'.format(time.strftime('%b %d %Y %H:%M:%S')))
            with wave.open(downlink_file) as wav_file:
                downlink_queue.put('File Downlink Parameters: {}'.format(wav_file.getparams()))
                ser.write(b'\x01')
                ser.write(b'\x02')
                ser.write(b'\x03')
                ser.write(b'\x04')
                ser.write(wav_file.readframes(100000000))
            downlink_queue.put('File Downlink Complete: {}\n'.format(time.strftime('%b %d %Y %H:%M:%S')))
            downlinked = True

        time.sleep(1)
    return

def transfer_function(parameters, downlink_queue, counter):
    cmd = 'hackrf_transfer {}'.format(parameters)

    start_timestamp = time.time()
    start_time = time.strftime('%b %d %Y %H:%M:%S')

    downlink_queue.put('\nHackRF Process {} Started: {}'.format(counter,start_time))

    # run hackrf transfer command
    hackrf_process = sp.Popen(shlex.split(cmd), stdout=sp.PIPE)
    write_led_state = True

    # Checks to make sure that the process is still running
    # None is good, it means it's still running
    while hackrf_process.poll() is None:
        write_led_state = not write_led_state
        GPIO.output(write_led_pin, write_led_state)
        time.sleep(0.2)

    # If the process poll returns 'not None' it will reach here
    # Will kill the process, and start over
    GPIO.output(write_led_pin, False)
    stop_timestamp = time.time()
    stop_time = time.strftime('%b %d %Y %H:%M:%S')
    elapsed_time = stop_timestamp - start_timestamp

    # checks if process was successful, returns 0 if successful
    if elapsed_time > 5 or counter > 1:
        downlink_queue.put('HackRF Process {} Completed: {}'.format(counter,stop_time))
        downlink_queue.put('HackRF Process {} Time Elapsed: {} seconds'.format(counter,elapsed_time))
        return 0
    else:
        downlink_queue.put('HackRF Process {} Failed: {}'.format(counter,stop_time))
        downlink_queue.put('HackRF Process {} Time Elapsed: {} seconds'.format(counter,elapsed_time))
        downlink_queue.put('Retrying Process...')
        return -1

