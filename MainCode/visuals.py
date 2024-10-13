import turtle

def draw_spaceship(position):
    turtle.clear()
    turtle.penup()
    turtle.goto(position[0] * 20, position[1] * 20)
    turtle.pendown()
    turtle.circle(10)
    turtle.update()

def setup_screen():
    turtle.setup(400, 400)
    turtle.tracer(0)

if __name__ == "__main__":
    setup_screen()
    draw_spaceship([0, 0])
    turtle.done()
