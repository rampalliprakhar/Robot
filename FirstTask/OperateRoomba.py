'''
Author: Prakhar Rampalli, Olive Challa, Tre'Stanley
Date Created: 09/10/24
Description: Learning how to operate Roomba using python commands.
'''
import struct
import serial
import time
connection = None
port = 'COM5'

# Connection
def connectRobot():
    global connection
    try:
        connection = serial.Serial(port, baudrate=115200, timeout=1)
        print("Connected")
    except serial.SerialException:
        print('Could not connect')

# Start-Reset
def startReset():
    connection.write(b'\x80\x07')

# Start
def start():
    connection.write(b'\x80')

#safe
def safeCom():
    connection.write(b'\x83')
    time.sleep(0.2)

# Full
def fullCom():
    connection.write(b'\x84')
    time.sleep(5)

# Drive
def driveRobot():
    connection.write(b'\x91\x20\x01\x20\x01')

# LED Lights
def changeLED():
    # Make the LEDs display 7777
    connection.write(b'\xA3\x07\x07\x07\x07')
    # Make the LEDs display the year you were born
    connection.write(b'\xA3\x02\x00\x00\x03')

connectRobot()
time.sleep(5)

startReset()
time.sleep(3)

start()
time.sleep(2)

safeCom()
time.sleep(2)

driveRobot()
changeLED()
connection.close()