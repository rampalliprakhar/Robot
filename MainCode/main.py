from spaceship import Spaceship
from planet import Planet
#from visuals import draw_spaceship, setup_screen

def main():
    spaceship = Spaceship("Explorer", 5)
    earth = Planet("Earth", "Water")

    # Set up the screen for visualizing the spaceship
#    setup_screen()
#    draw_spaceship(spaceship.position)

    while True:
        command = input("Enter a command (move, refuel, collect, exit): ")
        if command == "move":
            direction = input("Enter direction (up, down, left, right): ")
            spaceship.move(direction)
            #draw_spaceship(spaceship.position)  # Update visuals after moving
        elif command == "refuel":
            spaceship.refuel(2)
        elif command == "collect":
            print(f"Collected {earth.give_resource()} from {earth.name}.")
        elif command == "exit":
            break

if __name__ == "__main__":
    main()
