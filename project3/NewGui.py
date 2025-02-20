'''
Author: Prakhar Rampalli, Olive Challa, Tre'Stanley
Date Created: 10/10/24
Last Edited: 11/23/24
Description: This code enables comprehensive control of the robot via a graphical user interface (GUI) built with Tkinter. 
    It supports both GUI and keyboard inputs for seamless control, ensuring smooth operation through threading. 
    The robot can perform a variety of actions, including driving and turning in any direction, while simultaneously adjusting LED colors, playing music, 
    boosting speed, and modifying ASCII LED displays. 
'''
import tkinter as tk
import keyboard
import threading
from tkinter import Frame, Label, Button, Canvas, PhotoImage, Entry, messagebox
from functools import partial
from PIL import Image, ImageTk
from Robot import Robot

# Initialize the robot
robot = Robot("COM7")
robot.startSafe()

# Load images for different orientations
def load_images():
    base_image_path = "project3/nRobot.png"
    pil_roombaPic_N = Image.open(base_image_path)
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    return [ImageTk.PhotoImage(pil_roombaPic_N.rotate(angle)) for angle in angles]

# Function to check the 4 digit input
def display_led(input_digits):
    if len(input_digits) == 4 and input_digits.isdigit():
        ascii_digits = [ord(digit) for digit in input_digits]
        robot.digitLEDsASCII(bytes([ascii_digits[0]]), 
                            bytes([ascii_digits[1]]), 
                            bytes([ascii_digits[2]]), 
                            bytes([ascii_digits[3]]))
    else:
        messagebox.showerror("Invalid Input", "Please enter exactly 4 digits.")

# Update the displayed LED Value
def update_digit_leds(event=None):
    input_value = four_digit_input.get()  # Get the full input
    if len(input_value) == 4 and input_value.isdigit():  # Ensure it's exactly 4 digits
        display_led(input_value)  # Sends the 4-digit input to the robot's LEDs
    elif len(input_value) > 4:
        messagebox.showerror("Invalid Input", "Please enter exactly 4 digits. No more, no less.")  # Error for more than 4 digits
    else:
        messagebox.showerror("Invalid Input", "Please enter exactly 4 digits.")  # Error for less than 4 digits

# Movement functions
def move_robot(action, image):
    def move():
        if action == "North":
            robot.driveDirectFunction(b"\x02\x58\x02\x58")
        elif action == "South":
            robot.driveDirectFunction(b"\xFD\xA8\xFD\xA8")
        elif action == "West":
            robot.driveDirectFunction(b"\x00\xC8\xFF\x38")
        elif action == "East":
            robot.driveDirectFunction(b'\xFF\x38\x00\xC8')
        elif action == "NorthWest":
            robot.driveDirectFunction(b"\x02\x58\x01\x5E")
        elif action == "NorthEast":
            robot.driveDirectFunction(b"\x01\x5E\x02\x58")
        elif action == "SouthWest":
            robot.driveDirectFunction(b"\xFE\xA2\xFF\x06")
        elif action == "SouthEast":
            robot.driveDirectFunction(b"\xFF\x06\xFE\xA2")
        elif action == "Boost":
            robot.driveDirectFunction(b"\xFF\xC0\xFF\x51")
        else:  # Stop
            robot.driveDirectFunction(b"\x00\x00\x00\x00")

        # Update robot image on the canvas
        canvas.delete(canvas.find_closest(350, 350))
        canvas.create_image(350, 350, image=image)

    threading.Thread(target=move).start()

# Button press functions
def w_button_press(): move_robot("North", roomba_images[0])
def s_button_press(): move_robot("South", roomba_images[4])
def a_button_press(): move_robot("West", roomba_images[2])
def d_button_press(): move_robot("East", roomba_images[6])
def wa_button_press(): move_robot("NorthWest", roomba_images[1])
def wd_button_press(): move_robot("NorthEast", roomba_images[7])
def sa_button_press(): move_robot("SouthWest", roomba_images[3])
def sd_button_press(): move_robot("SouthEast", roomba_images[5])
def button_release(): move_robot("Stop", roomba_images[0])
def boost_button_press(): move_robot("Boost", roomba_images[0])
def play_music(): 
    def play_song():
        robot.playSong() 
    threading.Thread(target=play_song).start() # Play tune using the robot's function

# LED button function
def LED(color):
    def set_led():
        if color == "green":
            robot.led(b"\x04", b"\x00", b"\x80")
        elif color == "yellow":
            robot.led(b"\x04", b"\x10", b"\xFF")
        elif color == "orange":
            robot.led(b"\x04", b"\x20", b"\xFF")
        elif color == "red":
            robot.led(b"\x04", b"\xFF", b"\x80")
        else:
            print("Error: Invalid color")

    threading.Thread(target=set_led).start()


# Setting up the main window
root = tk.Tk()
root.title("Robot Control GUI")
root.configure(background="white")
root.geometry("800x800+0+0")
root.resizable(False, False)
root.state("zoomed")

# Create a canvas for the robot image
canvas_frame = Frame(root)
canvas_frame.pack()
canvas = Canvas(canvas_frame, bg="white", width=800, height=800)
canvas.pack()

# Display the default image
roomba_images = load_images()
canvas.create_image(350, 350, image=roomba_images[0])  # North

# Create LED buttons
color_frame = Frame(root, bg="white", width=400, height=100)
color_frame.place(x=30, y=30)
Label(color_frame, text="Clean/Power LED", pady=5, bg="white", font=("Comic Sans", 16)).pack()

for color in ["green", "yellow", "orange", "red"]:
    Button(color_frame, bg=color, text="    ", command=partial(LED, color)).pack(side=tk.LEFT, padx=10)

# Create WASD buttons
wasd_frame = Frame(root, bg="white", width=400, height=400)
wasd_frame.place(x=30, y=600)

buttons = {
    "W": w_button_press,
    "A": a_button_press,
    "S": s_button_press,
    "D": d_button_press,
    "WA": wa_button_press,
    "WD": wd_button_press,
    "SA": sa_button_press,
    "SD": sd_button_press
}

w_button = Button(wasd_frame, text="W", width=8, height=4)
a_button = Button(wasd_frame, text="A", width=8, height=4)
s_button = Button(wasd_frame, text="S", width=8, height=4)
d_button = Button(wasd_frame, text="D", width=8, height=4)
wa_button = Button(wasd_frame, text="WA", width=8, height=4)
wd_button = Button(wasd_frame, text="WD", width=8, height=4)
sa_button = Button(wasd_frame, text="SA", width=8, height=4)
sd_button = Button(wasd_frame, text="SD", width=8, height=4)

# Grid layout for buttons
w_button.grid(row=0, column=1, padx=5)
s_button.grid(row=2, column=1, pady=0)
a_button.grid(row=1, column=0, pady=5)
d_button.grid(row=1, column=2, pady=5)
wa_button.grid(row=0, column=0, pady=0)
wd_button.grid(row=0, column=2, pady=0)
sa_button.grid(row=2, column=0, pady=0)
sd_button.grid(row=2, column=2, pady=0)

# Bind the buttons to their functions
w_button.bind("<ButtonPress>", lambda event: w_button_press())
s_button.bind("<ButtonPress>", lambda event: s_button_press())
a_button.bind("<ButtonPress>", lambda event: a_button_press())
d_button.bind("<ButtonPress>", lambda event: d_button_press())
wa_button.bind("<ButtonPress>", lambda event: wa_button_press())
wd_button.bind("<ButtonPress>", lambda event: wd_button_press())
sa_button.bind("<ButtonPress>", lambda event: sa_button_press())
sd_button.bind("<ButtonPress>", lambda event: sd_button_press())

# Bind the button release to stop the robot
for button in [w_button, s_button, a_button, d_button, wa_button, wd_button, sa_button, sd_button]:
    button.bind("<ButtonRelease>", lambda event: button_release())

# Boost button
boost_button_frame = Frame(root, bg="white", width=400, height=100)
boost_button_frame.place(x=1430, y=730)
boost_icon = PhotoImage(file="project3/boosterIcon.png")
Button(boost_button_frame, image = boost_icon, bg="white", command=boost_button_press).pack()

# Play button
play_button_frame = Frame(root, bg="white", width=400, height=100)
play_button_frame.place(x=1430, y=630)
play_icon = PhotoImage(file="project3/playMusicButton.png")
Button(play_button_frame, image=play_icon, bg="white", command=play_music).pack()

# 4-digit ASCII LED input
four_digit_frame = tk.Frame(root, bg="white", width=400, height=100)
four_digit_frame.place(x=1330, y=20)
tk.Label(four_digit_frame, text="4 Digit ASCII LED", pady=5, bg="white", font=("Comic Sans", 16)).pack()

# Entry widget to allow the user to input 4 digits
four_digit_input = tk.Entry(four_digit_frame, width=4, font=("Comic Sans", 17), bg="black", fg="white", insertbackground="white")
four_digit_input.pack(side=tk.RIGHT, padx=10)

# Block any character input other than digits (0-9)
def block_non_digit_input(event):
    if event.keysym == "BackSpace":
        return None
    if event.char not in "0123456789":
        return "break"  # Prevent the character from being typed into the Entry

four_digit_input.bind("<Key>", block_non_digit_input)  # Bind to block non-digit input
four_digit_input.bind("<Return>", update_digit_leds)  # Bind the Return (Enter) key to update the LEDs

# Keyboard Binding
keyboard.on_press_key("w", lambda e: w_button_press())
keyboard.on_press_key("up_arrow", lambda e: w_button_press())
keyboard.on_press_key("a", lambda e: a_button_press())
keyboard.on_press_key("left_arrow", lambda e: a_button_press())
keyboard.on_press_key("d", lambda e: d_button_press())
keyboard.on_press_key("right_arrow", lambda e: d_button_press())
keyboard.on_press_key("s", lambda e: s_button_press())
keyboard.on_press_key("down_arrow", lambda e: s_button_press())
keyboard.on_press_key(" ", lambda e: boost_button_press())

keyboard.on_release_key("w", lambda e: button_release())
keyboard.on_release_key("up_arrow", lambda e: button_release())
keyboard.on_release_key("a", lambda e: button_release())
keyboard.on_release_key("left_arrow", lambda e: button_release())
keyboard.on_release_key("d", lambda e: button_release())
keyboard.on_release_key("right_arrow", lambda e: button_release())
keyboard.on_release_key("s", lambda e: button_release())
keyboard.on_release_key("down_arrow", lambda e: button_release())
keyboard.on_release_key(" ", lambda e: button_release())

# Start the GUI loop
root.mainloop()
