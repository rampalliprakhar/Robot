'''
Author: Prakhar Rampalli, Olive Challa, Tre'Stanley
Written: 10/26/24
Compilation: TuneRobot.py
Description: A program that sends command to the roomba to play happy birthday song. 
    The song is nearly accurate, revisions will be added in the near future.
'''
import serial
import time

connection = None
port = 'COM8' 

# Connect to the Roomba
def connectRobot():
    global connection
    try:
        # Connection
        connection = serial.Serial(port, baudrate=115200, timeout=1)
        print("Connected")
    except serial.SerialException:
        print('Could not connect')

# Start Roomba and set it to safe mode
def startSafe():
    if connection:
        connection.write(b'\x80')  # Start
        time.sleep(0.1)
        connection.write(b'\x83')  # Safe mode
        time.sleep(0.1)
    else:
        print("Not Connected.")

def playSong():
        # Note durations in 1/64th of a second
        QUARTER_NOTE = b"\x20"  # 64/64 = 1 second
        HALF_NOTE = b"\x30"  # 128/64 = 2 seconds
        # Note Pitch
        C4 = b"\x3C"
        D4 = b"\x3E"
        E4 = b"\x40"
        F4 = b"\x41"
        G4 = b"\x43"
        A4 = b"\x45"
        B4 = b"\x47"
        C5 = b"\x48"

        VERSE_ONE = (
            b"\x8C\x00\x0C"
            + C4
            + QUARTER_NOTE
            + C4
            + QUARTER_NOTE
            + D4
            + QUARTER_NOTE
            + C4
            + HALF_NOTE
            + F4
            + QUARTER_NOTE
            + E4
            + HALF_NOTE
            + C4
            + QUARTER_NOTE
            + C4
            + QUARTER_NOTE
            + D4
            + QUARTER_NOTE
            + C4
            + HALF_NOTE
            + G4
            + QUARTER_NOTE
            + F4
            + HALF_NOTE
        )
        VERSE_TWO = (
            b"\x8C\x02\x0D"  # Song 2, with 7 notes
            + C4
            + QUARTER_NOTE
            + C4
            + QUARTER_NOTE
            + C5
            + QUARTER_NOTE
            + A4
            + HALF_NOTE
            + F4
            + QUARTER_NOTE
            + E4
            + QUARTER_NOTE
            + D4
            + HALF_NOTE
            + B4
            + QUARTER_NOTE
            + B4
            + QUARTER_NOTE
            + A4
            + QUARTER_NOTE
            + F4
            + HALF_NOTE
            + G4
            + QUARTER_NOTE
            + F4
            + HALF_NOTE
        )
        connection.write(VERSE_ONE)
        time.sleep(0.1)
        connection.write(b"\x8D\x00")  # Play song 0 (verse 1)
        time.sleep(3)

        connection.write(VERSE_TWO)
        time.sleep(0.1)
        connection.write(b"\x8D\x01")  # Play song 1 (verse 2)
        time.sleep(3)
        print("Song sent.")


# Calling the functions
connectRobot()
startSafe()
playSong()
