"""
Author: Prakhar Rampalli, Olive Challa, Tre'Stanley
Date Created: 10/10/24
Last Edited: 10/10/24
Description: This is the main robot class that contains all commands, and we can use this class as an instance in other classes.
"""

import serial
import time


class Robot:
    # Command hex-byte
    start_cmd = b"\x80"
    reset_cmd = b"\x07"
    stop_cmd = b"\xAD"
    safe_cmd = b"\x83"
    full_cmd = b"\x84"
    drive_direct = b"\x91"
    song_load_cmd = b"\x8C"
    play_song_cmd = b"\x8D"
    leds = b"\x8B"
    digit_led = b'\xA4'

    # packet IDs definitions
    wall = b"\x08"
    bumpsAndWheels = b"\x07"
    cliffLeft = b"\x09"
    cliffFrontLeft = b"\x0A"
    cliffFrontRight = b"\x0B"
    cliffRight = b"\x0C"
    virtualWall = b"\x0D"
    buttons = b"\x12"
    distance = b"\x13"
    angle = b"\x14"
    chargingState = b"\x15"
    voltage = b"\x16"
    temperature = b"\x18"
    batteryCharge = b"\x19"
    wallSignal = b"\x1B"
    cliffLeftSignal = b"\x1C"
    cliffFrontLeftSignal = b"\x1D"
    cliffFrontRightSignal = b"\x1E"
    cliffRightSignal = b"\x1F"

    # Constructor that connects the Roomba via the COM Port
    def __init__(self, port):
        """This constructor creates an instance of Robot by establishing a serial connection between the robot and the user's machine.
                NOTE: The COM port frequently changes depending on the type of wire.

        Args:
                port (str): The COM port connects the robot to the machine via serial communication.
        """
        try:
            # Connection
            self.connection = serial.Serial(port, baudrate=115200, timeout=1)
            print("Connected")
        except serial.SerialException:
            print("Could not connect")

    # Function that sends command to the Roomba
    def sendCommand(self, value):
        """To send a command to the robot, use the following format
                .write to send a command via the serial connection.

        Args:
                value (bytes): The variable containing the byte representing the HEX OPCODE value.
        """
        self.connection.write(value)

    # Function that starts the Roomba
    def start(self):
        """The Start command prepares the robot for action."""
        self.sendCommand(self.start_cmd)

    # Function that stops the Roomba
    def stop(self):
        """The Stop instruction terminates current communication with the robot."""
        self.sendCommand(self.stop_cmd)

    # Function that resets the Roomba
    def reset(self):
        """Reset command to reset the robot."""
        self.sendCommand(self.reset_cmd)
        time.sleep(1)

    # Function for songs and drive to work
    def startSafe(self):
        """Combination of start and safe command to start the robot and move to the safe mode."""
        if self.connection:
            self.sendCommand(self.start_cmd)  # Start
            time.sleep(0.1)
            self.sendCommand(self.safe_cmd)  # Safe mode
            time.sleep(0.1)
        else:
            print("Not Connected.")

    # Function for driveDirect
    def driveDirectFunction(self, wheelByte):
        """Drive direct command allows the user to control each wheel of the robot individually.
                NOTE: The syntax includes negative values of the input, using 2's complement.

        Args:
                wheelByte (bytes): 			All wheel bytes in one, with slashes, inputted.
        """
        self.sendCommand(self.drive_direct + wheelByte)

    def led(self, ledBits, powerColor, powerIntensity):
        self.sendCommand(self.leds + ledBits + powerColor + powerIntensity)

    def digitLEDsASCII(self, digit3, digit2, digit1, digit0):
        self.sendCommand(self.digit_led + digit3 + digit2 + digit1 + digit0)

    def playSong(self):
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
        self.sendCommand(VERSE_ONE)
        time.sleep(0.1)
        self.sendCommand(b"\x8D\x00")  # Play song 0 (verse 1)
        time.sleep(3)

        self.sendCommand(VERSE_TWO)
        time.sleep(0.1)
        self.sendCommand(b"\x8D\x01")  # Play song 1 (verse 2)
        time.sleep(3)
        print("Song sent.")
