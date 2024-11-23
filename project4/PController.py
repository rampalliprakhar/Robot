'''
Author: Prakhar Rampalli, Olive Challa, Tre'Stanley
Date Created: 11/14/24
Last Edited: 11/21/24
Description: This code implements a P-Controller (Proportional Controller) to ensure the robot moves forward in a straight 
    line while actively avoiding collisions with obstacles. 
    The controller continuously adjusts the robot's movement to maintain a straight path, responding to any detected deviations or obstructions, 
    ensuring smooth and safe navigation.
'''
import time
import struct
from Robot import Robot

# Create an instance of the Robot class
robot = Robot("COM9")
robot.startSafe() 

# Parameters for Wall Following
TARGET_DISTANCE = 30  # Target distance from the wall in centimeters
Kp = 0.5              # Proportional constant
MAX_SPEED = 200       # Maximum speed
MIN_SPEED = 50        # Minimum speed

# Drive with a particular speed for both wheels
def drive(left_speed, right_speed):
    # Convert left and right speeds to bytes and send them to the robot
    left_byte = struct.pack('>h', left_speed)
    right_byte = struct.pack('>h', right_speed)
    robot.driveDirectFunction(left_byte + right_byte)

# Small rotation to avoid obstacles
def avoid_obstacle():
    print("Obstacle detected, avoiding...")
    # Move backward
    drive(-100, -100)
    time.sleep(0.5)
    drive(100, -100)
    time.sleep(1)    
    # After avoiding the obstacle, turn back and follow the wall
    drive(MAX_SPEED, MAX_SPEED)

# Get the range sensor data (distance to the wall)
def get_range_sensor_data():
    try:
        # Use the twoByteSensor function to get the two-byte response from the wallSignal sensor
        sensor_data = robot.twoByteSensor(robot.wallSignal)
        
        # Check the format of the returned data
        if sensor_data:
            # Convert the response from binary string format to an integer
            distance = struct.unpack('>H', sensor_data.encode())[0]
            return distance  # Return the distance as an integer
        else:
            return 0  # if no data was received
    except Exception as e:
        print(f"Error getting sensor data: {e}")
        return 0  # Return a default value in case of an error

# Get bump sensor data (detect bump status)
def get_bump_sensor_data():
    try:
        robot.sendCommand(robot.bumpsAndWheels)         # Request bump sensor data
        data = robot.connection.readline().strip()      # Read the response
        return int(data) if data else 0                 # Return 1 if bump detected, otherwise 0
    except Exception as e:
        print(f"Error reading bump sensor: {e}")
        return 0                                        # Return 0 in case of an error

# Main wall-following function
def follow_wall():
    while True:
        # Get sensor data
        distance = get_range_sensor_data()
        bump_status = get_bump_sensor_data()

        # Calculate error (difference between target distance and actual distance)
        error = TARGET_DISTANCE - distance

        # Apply Proportional Control (P-controller)
        control_signal = Kp * error
        if control_signal > MAX_SPEED:
            control_signal = MAX_SPEED
        elif control_signal < MIN_SPEED:
            control_signal = MIN_SPEED

        # Adjust wheel speeds based on the error
        left_speed = MAX_SPEED - control_signal
        right_speed = MAX_SPEED + control_signal
        
        left_speed = max(MIN_SPEED, min(MAX_SPEED, left_speed))
        right_speed = max(MIN_SPEED, min(MAX_SPEED, right_speed))

        # Drive the robot with the adjusted speeds
        drive(left_speed, right_speed)

        # Check for obstacles using bump sensors
        if bump_status > 0:
            robot.stop()
            print("Obstacle detected! Avoiding in progress...")
            avoid_obstacle()
            time.sleep(1)
            drive(MAX_SPEED, MAX_SPEED)

        time.sleep(0.1)

# Execute the function
follow_wall()