from planet import Planet
from spaceship import Spaceship

def main():
    spaceship = Spaceship("Explorer", 5)
    earth = Planet("Earth", "Green")

    while True:
        command = input("Enter a command (move, refuel, collect, exit):")
        if command == "move":
            direction = input("Enter direction (up, down, left, right)")
            spaceship.move(direction)
        elif command == "refuel":
            spaceship.refuel(2)
        elif command == "collect":
            print(f"Collected {earth.give_resource()} from {earth.name}.")
        elif command == "exit":
            break
if __name__ == "__main__":
    main()