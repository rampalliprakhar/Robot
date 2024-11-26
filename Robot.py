"""
Author: Prakhar Rampalli, Olive Challa, Tre'Stanley
Date Created: 10/10/24
Last Edited: 10/10/24
Description: This is the main robot class that contains all commands, and we can use this class as an instance in other classes.
"""

import serial
import struct
import time


class Robot:
    # Command hex-byte definitions for various robot functions
    start_cmd = b"\x80"           # Command to start the robot
    safe_cmd = b"\x83"            # Command to put robot in safe mode
    full_cmd = b"\x84"            # Command to put robot in full mode
    reset_cmd = b"\x07"           # Command to reset the robot
    stop_cmd = b"\xAD"            # Command to stop the robot
    sensors_cmd = b'\x8E'         # Command to get sensor data
    buttons_cmd = b'\xA5'         # Command to get button states
    drive_cmd = b'\x89'           # Command to control robot movement
    drive_direct = b"\x91"        # Command for direct wheel control
    leds = b"\x8B"                # Command to control LED lights
    digit_led = b'\xA4'           # Command to control digit LEDs
    song_load_cmd = b"\x8C"       # Command to load a song
    play_song_cmd = b"\x8D"       # Command to play a song
    seek_dock_cmd = b'\x8F'       # Command to initiate docking behavior


    # Packet IDs for different sensor readings
    wall = b"\x08"                # Wall detection sensor
    bumpsAndWheels = b"\x07"      # Bump sensor and wheel status
    cliffLeft = b"\x09"           # Left cliff sensor
    cliffFrontLeft = b"\x0A"      # Front-left cliff sensor
    cliffFrontRight = b"\x0B"     # Front-right cliff sensor
    cliffRight = b"\x0C"          # Right cliff sensor
    virtualWall = b"\x0D"         # Virtual wall sensor
    buttons = b"\x12"             # Button states
    distance = b"\x13"            # Distance traveled sensor
    angle = b"\x14"               # Angle turned sensor
    chargingState = b"\x15"       # Charging state sensor
    voltage = b"\x16"             # Voltage sensor
    temperature = b"\x18"         # Temperature sensor
    batteryCharge = b"\x19"       # Battery charge sensor
    wallSignal = b"\x1B"          # Wall signal sensor
    cliffLeftSignal = b"\x1C"     # Left cliff signal strength
    cliffFrontLeftSignal = b"\x1D"  # Front-left cliff signal strength
    cliffFrontRightSignal = b"\x1E" # Front-right cliff signal strength
    cliffRightSignal = b"\x1F"    # Right cliff signal strength

    # Constructor that connects the Roomba via the COM Port
    def __init__(self, port):
        """
        Initializes the robot by establishing a serial connection to the robot via the specified COM port.
        
        Args:
            port (str): The COM port to which the robot is connected for serial communication.
            
        Raises:
            serial.SerialException: If the connection to the robot cannot be established.
        """
        try:
            # Connection
            self.connection = serial.Serial(port, baudrate=115200, timeout=1)
            print("Connected")
        except serial.SerialException:
            print("Could not connect")

    # Function that sends command to the Roomba
    def sendCommand(self, value):
        """
        Sends a hex-byte command to the robot via the serial connection.
        
        Args:
            value (bytes): The command (in hex) to send to the robot.
        """
        self.connection.write(value)

    # Function that starts the Roomba
    def start(self):
        """
        Sends the start command to the robot, preparing it for action.
        This command starts the robot's motor and prepares it for further instructions.
        """
        self.sendCommand(self.start_cmd)

    # Function that stops the Roomba
    def stop(self):
        """
        Sends the stop command to the robot to halt its movement immediately.
        Stops the robot and terminates current communication.
        """
        self.sendCommand(self.stop_cmd)

    # Function that resets the Roomba
    def reset(self):
        """
        Sends the reset command to the robot to reset its internal state and clear any previous errors.
        The robot will reboot after this command.
        """
        self.sendCommand(self.reset_cmd)
        time.sleep(1)

    # Function for songs and drive to work
    def startSafe(self):
        """
        Sends the start and safe commands to the robot to start it in safe mode.
        Safe mode ensures the robot will avoid dangerous behaviors like moving too fast.
        """
        if self.connection:
            self.sendCommand(self.start_cmd)  # Start
            time.sleep(0.1)
            self.sendCommand(self.safe_cmd)  # Safe mode
            time.sleep(0.1)
        else:
            print("Not Connected.")

    def read(self, howManyBytes: int = 1) -> str:
        """
        Reads a specified number of bytes from the robot's response and returns it as a binary string.
        
        Args:
            howManyBytes (int): The number of bytes to read from the robot (default is 1).
            
        Returns:
            str: The binary representation of the received bytes.
        """
        if howManyBytes == 1:
            buttonState = self.connection.read(1)
            time.sleep(0.5)
            byte = struct.unpack("B", buttonState)[0]
            binary = "{0:08b}".format(byte)
            return binary
    
        if howManyBytes == 2:
            buttonState = self.connection.read(1)
            time.sleep(0.5)
            buttonState1 = self.connection.read(1)
            time.sleep(0.5)
            byte = struct.unpack("B", buttonState)[0]
            highByte = "{0:08b}".format(byte)
            byte1 = struct.unpack("B", buttonState)[0]
            lowByte = "{0:08b}".format(byte1)
            return highByte + lowByte
        
    def seekDock(self):
        """
        Sends the seek dock command to the robot, instructing it to locate and return to its charging dock.
        """
        self.sendCommand(self.seek_dock_cmd)

    def drive(self, velocityHighByte, velocityLowByte, radiusHighByte, radiushLowByte):
        """
        Sends a drive command to the robot, controlling both wheels at the specified velocity and radius.
        
        Args:
            velocityHighByte (bytes): The high byte of the robot's velocity.
            velocityLowByte (bytes): The low byte of the robot's velocity.
            radiusHighByte (bytes): The high byte of the radius (defines turn radius).
            radiushLowByte (bytes): The low byte of the radius.
        """
        self.sendCommand(self.drive_cmd + velocityHighByte + velocityLowByte + radiusHighByte + radiushLowByte)

    # Function for driveDirect
    def driveDirectFunction(self, wheelByte):
        """
        Sends the drive direct command, allowing for independent control of each wheel's velocity.
        This is useful for turning or moving one wheel faster than the other.
        
        Args:
            wheelByte (bytes): A byte array containing the velocities for both wheels (signed values in 2's complement).
        """
        self.sendCommand(self.drive_direct + wheelByte)

    def oneByteSensor(self, packetID):
        """
        Requests data from a sensor that returns a single byte of information.
        
        Args:
            packetID (bytes): The packet ID corresponding to the sensor being queried.
            
        Returns:
            str: The binary string representation of the sensor data.
        """
        self.sendCommand(self.sensors_cmd + packetID)
        return self.read(1)

    def twoByteSensor(self, packetID):
        """
        Requests data from a sensor that returns two bytes of information.
        
        Args:
            packetID (bytes): The packet ID corresponding to the sensor being queried.
            
        Returns:
            str: The binary string representation of the sensor data (two bytes combined).
        """
        self.sendCommand(self.sensors_cmd + packetID)
        return self.connection.readline().decode('utf-8').strip()

    def led(self, ledBits, powerColor, powerIntensity):
        """
        Controls the LED light on the robot, adjusting its state, color, and intensity.
        
        Args:
            ledBits (bytes): A byte indicating the LED's state (on/off).
            powerColor (bytes): A byte representing the color of the LED.
            powerIntensity (bytes): A byte representing the intensity of the LED.
        """
        self.sendCommand(self.leds + ledBits + powerColor + powerIntensity)

    def digitLEDsASCII(self, digit3, digit2, digit1, digit0):
        """
        Controls the four 7-segment digit LEDs on the robot.
        
        Args:
            digit3 (bytes): The value for the fourth digit LED.
            digit2 (bytes): The value for the third digit LED.
            digit1 (bytes): The value for the second digit LED.
            digit0 (bytes): The value for the first digit LED.
        """
        self.sendCommand(self.digit_led + digit3 + digit2 + digit1 + digit0)

    def playSong(self):
        """
        Plays the "Happy Birthday" song on the robot using pre-defined note durations and pitches.
        The song is split into two verses, each sent and played sequentially.
        """
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
            + C4 + QUARTER_NOTE + C4 + QUARTER_NOTE 
            + D4 + QUARTER_NOTE + C4 + HALF_NOTE 
            + F4 + QUARTER_NOTE + E4 + HALF_NOTE 
            + C4 + QUARTER_NOTE + C4 + QUARTER_NOTE 
            + D4 + QUARTER_NOTE + C4 + HALF_NOTE 
            + G4 + QUARTER_NOTE + F4 + HALF_NOTE
        )
        VERSE_TWO = (
            b"\x8C\x02\x0D"  # Song 2, with 7 notes
            + C4 + QUARTER_NOTE + C4 + QUARTER_NOTE
            + C5 + QUARTER_NOTE + A4 + HALF_NOTE
            + F4 + QUARTER_NOTE + E4 + QUARTER_NOTE 
            + D4 + HALF_NOTE + B4 + QUARTER_NOTE
            + B4 + QUARTER_NOTE + A4 + QUARTER_NOTE 
            + F4 + HALF_NOTE + G4 + QUARTER_NOTE 
            + F4 + HALF_NOTE
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
