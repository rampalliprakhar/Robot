'''
Author: Prakhar Rampalli, Olive Challa, Tre'Stanley
Date Created: 09/26/24
Last Edited: 10/10/24
Description: This code directs the robot to travel around a 6ft x 6ft square on the classroom floor, which has been selected with markers. 
The code imports the Robot.py class, which has methods for delivering commands to the MoveRobot file.
'''
import serial
import time
from . import Robot

instance = Robot('COM6')
instance.startSafe()

#Function for robot to move straight
def move_straight():
    speed_one = 0x64            # speed in 100 seconds
    speed_two = 0x01/0x22       # speed in 290 seconds

    # Move robot straight 100 speed - 1st Attempt
    instance.driveDirectFunction(b'\x91\x00\x64\x00\x64') 
    time.sleep(16.1)            # 100 speed
    
    # Move robot straight 290 speed - 2nd Attempt
    instance.driveDirectFunction(b'\x91\x01\x22\x01\x22')
    time.sleep(6)               # 290 speed
    
    # Move robot straight 400 speed - 3rd Trial Attempt
    instance.driveDirectFunction(b'\x91\x01\x90\x01\x90')
    time.sleep(4.9)             # 400 speed
    
    # Stop the roomba
    instance.stop()
    time.sleep(0.1)
    
    # Start the roomba at safe mode
    instance.startSafe()

# function for robot to move right 90 degrees
def turn_right():
    # For speed 100, turn 90 degrees right
    duration_one = 2.95          # in seconds
    # For speed 290, turn 90 degrees right
    duration_two = 2.98         # in seconds
    # For speed 400, turn 90 degrees right - (To fix it)
    duration_three = 2.88
    
    # Drive direct with speed 40 and -40
    instance.driveDirectFunction(b'\x91\xFF\xD8\x00\x28')

    # Turn the robot 90 degrees for speed = 100 (1st Attempt)
    time.sleep(duration_one)
    # Turn the robot 90 degrees for speed = 290 (2nd Attempt)
    time.sleep(duration_two)
    # Turn the robot 90 degrees for speed = 400 (3rd Attempt - trial)
    time.sleep(duration_three)
    
    # Stop connection
    instance.stop()
    
    # Allow it start after turning
    time.sleep(0.2)

    # Start the robot
    instance.startSafe()

# Function for roomba to drive
def driveRobot():

    # Uses for loop to execute the inner code block four times
    for i in range(4):
        move_straight()
        turn_right()

driveRobot()