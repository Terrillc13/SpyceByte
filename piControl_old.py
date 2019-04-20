#! /usr/bin/env/python

import serial
import time

#port = "/dev/ttyAMA0" 
arduinoPort = "/dev/ttyUSB0"
    
rate = 9600

# Establish connection to the arduino
arduinoSerial = serial.Serial(arduinoPort,rate,timeout=5)
arduinoSerial.reset_input_buffer()

def doDispense(jar, amount):
    for x in range(5):
        # Send 5 quick messages for the Arduino to pick up
        arduinoSerial.write(b'd%d%d' % (jar, amount))
        arduinoSerial.flush()
    # Times out assuming that each rotation takes 1 second
    dispenseTimeout = time.time() + amount + 5
    # Loop until the response is received or until 5 seconds
    while time.time() < dispenseTimeout:
        if arduinoSerial.inWaiting() > 0:
            return True
    return False
    
def getFullness(jar):
    # Declare return value
    jarFullness = 0
    # Send 5 quick messages for the Arduino to pick up
    for x in range(5):
        arduinoSerial.write(b's%d' % jar)
        arduinoSerial.flush()
    # Times out after five seconds
    fullnessTimeout = time.time() + 5
    # Loop until the response is received or until 5 seconds
    while time.time() < fullnessTimeout:
        if arduinoSerial.inWaiting() > 0:     
            byteFullness = arduinoSerial.read(7)
            arduinoSerial.flushInput()
            arduinoSerial.reset_input_buffer()
            jarFullness =float(byteFullness)
            break
    return jarFullness

# Test the functionality of the dispense and getFullness methods.
def test():
    while True:
        query = int(input("Dispense (1) or Get Fullness (2)? Exit (0): "))
        if query == 1:
            jar = int(input("Enter Jar: "))
            amount = int(input("Enter Amount: "))
            doDispense(jar, amount)
        elif query == 2:
            jar = int(input("Enter Jar: "))
            print(getFullness(jar))
        else:
            arduinoSerial.close()
            break
test() #Use to test class by itself.
