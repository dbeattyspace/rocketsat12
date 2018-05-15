import serial
import time
import threading

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
