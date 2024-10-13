class Spaceship:
    def __init__(self, name, fuel):
        self.name = name
        self.fuel = fuel
        self.position = [0, 0]

    def move(self, direction):
        if self.fuel <= 0:
            print("Out of fuel!")
            return
        
        if direction == 'up':
            self.position[1] += 1
        elif direction == 'down':
            self.position[1] -= 1
        elif direction == 'left':
            self.position[0] -= 1
        elif direction == 'right':
            self.position[0] += 1
        
        self.fuel -= 1
        print(f"Moved {direction}. Current position: {self.position}. Fuel left: {self.fuel}")

    def refuel(self, amount):
        self.fuel += amount
        print(f"Refueled {amount} units. Total fuel: {self.fuel}")
