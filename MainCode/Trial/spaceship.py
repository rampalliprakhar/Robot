'''
Spaceship Class (spaceship.py)
○ Attributes: name, fuel, position.
○ Methods:
■ move(direction) - to change the position of the spaceship.
■ refuel(amount) - to increase the fuel.
'''
class Spaceship:
    
    def __init__(self, name, fuel):
        self.name = name
        self.fuel = fuel
        self.position = [0, 0]
    fuel = 0

    def move(self, direction):
        if self.fuel <= 0:
            print("Fuel low!")
            return
        elif direction == "up":
            self.position[1] += 1
        elif direction == "down":
            self.position[1] -= 1
        elif direction == "left":
            self.position[0] -= 1
        elif direction == "right":
            self.position[0] += 1

        self.fuel -= 1
        print(f"Moved {direction}. Current position: {self.position}. Fuel left: {self.fuel}")
    
    def refuel(amount):
        fuel += amount
        print("Fuel left: ", fuel)