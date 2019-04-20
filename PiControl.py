#! /usr/bin/env/python

import serial
import time

arduino_port = "/dev/ttyUSB0"
    
rate = 9600

try:
    # Establish connection to the Arduino
    arduino_serial = serial.Serial(arduino_port, rate, timeout=5)
    arduino_serial.reset_input_buffer()
except Exception as e:
    print("Unable to connect to the Arduino.")


def dispense(jar, amount):
    try:
        for x in range(5):
                # Send 5 quick messages for the Arduino to pick up
                arduino_serial.write(b'd%d%d' % (jar, amount))
                arduino_serial.flush()
        # Times out assuming that each rotation takes 1 second
        dispense_timeout = time.time() + amount + 5
        # Loop until the response is received or until 5 seconds
        while time.time() < dispense_timeout:
            if arduino_serial.inWaiting() > 0:
                return True
        return False
    except Exception:
        print("Unable to connect to the Arduino.")
        return False


def fullness(jar):
    try:
        # Declare return value
        jar_fullness = 0
        # Send 5 quick messages for the Arduino to pick up
        for x in range(5):
            arduino_serial.write(b's%d' % jar)
            arduino_serial.flush()
        # Times out after five seconds
        fullness_timeout = time.time() + 5
        # Loop until the response is received or until 5 seconds
        while time.time() < fullness_timeout:
            if arduino_serial.inWaiting() > 0:
                byte_fullness = arduino_serial.read(7)
                arduino_serial.flushInput()
                arduino_serial.reset_input_buffer()
                jar_fullness = float(byte_fullness)
                break
        return jar_fullness
    except Exception:
        print("Unable to connect to the Arduino.")
        return 0


def test():
    while True:
        query = int(input("Dispense (1) or Get Fullness (2)? Exit (0): "))
        if query == 1:
            jar = int(input("Enter Jar: "))
            amount = int(input("Enter Amount: "))
            dispense(jar, amount)
        elif query == 2:
            jar = int(input("Enter Jar: "))
            print(fullness(jar))
        else:
            arduino_serial.close()
            break
