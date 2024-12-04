'''
Author: Prakhar Rampalli, Olive Challa, Tre'Stanley
Written: 09/24/24
Compilation: TuneRobot.py
Description: A program that sends command to the roomba to play happy birthday song. 
    The song is not completely accurate, revisions will be added in the near future.
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

# Note durations in 1/64th of a second
QUARTER_NOTE = b'\x10'  # 64/64 = 1 second
HALF_NOTE = b'\x20'     # 128/64 = 2 seconds
# Note Pitch
C4 = b'\x3C'
D4 = b'\x3E'
E4 = b'\x40'
F4 = b'\x41'
G4 = b'\x43'
A4 = b'\x45'
B4 = b'\x47'
C5 = b'\x48'

# Define the Happy Birthday song parts using MIDI numbers from our frequency table
def noteHappyBirthday():
    if connection:
        # Verse 1: "Happy Birthday to You"
        VERSE_ONE = (
            b'\x8C\x00\x06'  +
            C4 + QUARTER_NOTE +  
            C4 + QUARTER_NOTE +  
            D4 + QUARTER_NOTE +  
            C4 + HALF_NOTE +     
            F4 + QUARTER_NOTE +  
            E4 + HALF_NOTE       
        )

        # Verse 2: "Happy Birthday to You"
        VERSE_TWO = (
            b'\x8C\x01\x06' +  # Song 1, with 6 notes
            C4 + QUARTER_NOTE +  
            C4 + QUARTER_NOTE +  
            D4 + QUARTER_NOTE +  
            C4 + HALF_NOTE +     
            G4 + QUARTER_NOTE +  
            F4 + HALF_NOTE       
        )

        # Verse 3: "Happy Birthday dear [name]"
        VERSE_THREE = (
            b'\x8C\x02\x07' +  # Song 2, with 7 notes
            C4 + QUARTER_NOTE +  
            C4 + QUARTER_NOTE +  
            C5 + QUARTER_NOTE +  
            A4 + HALF_NOTE +     
            F4 + QUARTER_NOTE +  
            E4 + QUARTER_NOTE +  
            D4 + HALF_NOTE       
        )

        # Verse 4: "Happy Birthday to You"
        VERSE_FOUR = (
            b'\x8C\x03\x06' +  
            B4 + QUARTER_NOTE +  
            B4 + QUARTER_NOTE +  
            A4 + QUARTER_NOTE +  
            F4 + HALF_NOTE +     
            G4 + QUARTER_NOTE +  
            F4 + HALF_NOTE       
        )

        # Send the songs to the Roomba
        connection.write(VERSE_ONE)
        time.sleep(0.1) 
        connection.write(VERSE_TWO)
        time.sleep(0.1) 
        connection.write(VERSE_THREE)
        time.sleep(0.1) 
        connection.write(VERSE_FOUR)
        time.sleep(0.1)
        print("Song sent.")

# Function to play the defined song
def playSong():
    if connection:
        # Play each verse sequentially
        connection.write(b'\x8D\x00')  # Play song 0 (verse 1)
        # Debug - check to see whether song plays
        print("Playing verse 1")
        time.sleep(3)  

        connection.write(b'\x8D\x01')  # Play song 1 (verse 2)
        # Debug - check to see whether song plays
        print("Playing verse 2")
        time.sleep(3)  

        connection.write(b'\x8D\x02')  # Play song 2 (verse 3)
        # Debug - check to see whether song plays
        print("Playing verse 3")
        time.sleep(3)  

        connection.write(b'\x8D\x03')  # Play song 3 (verse 4)
        # Debug - check to see whether song plays
        print("Playing verse 4")
        time.sleep(2) 
    else:
        # Check to see whether the robot is connected
        print("Connection Not Established.")

# Calling the functions
connectRobot()
startSafe()
noteHappyBirthday()
playSong()
