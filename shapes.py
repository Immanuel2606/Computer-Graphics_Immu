import turtle

# Create screen
screen = turtle.Screen()
screen.title("Geometric Primitives")
screen.bgcolor("white")
screen.setup(width=900, height=700)

# Create turtle
t = turtle.Turtle()
t.speed(5)
t.pensize(3)

# ---------------- LINE ----------------
t.penup()
t.goto(-350, 250)
t.pendown()

t.pencolor("black")
t.pensize(5)
t.goto(-150, 250)


# ---------------- CIRCLE ----------------
t.penup()
t.goto(0, 200)
t.pendown()

t.pencolor("blue")
t.fillcolor("lightblue")

t.begin_fill()
t.circle(60)
t.end_fill()


# ---------------- RECTANGLE ----------------
t.penup()
t.goto(180, 250)
t.pendown()

t.pencolor("green")
t.fillcolor("lightgreen")

t.begin_fill()

for i in range(2):
    t.forward(140)
    t.right(90)
    t.forward(80)
    t.right(90)

t.end_fill()


# ---------------- ELLIPSE ----------------
t.penup()
t.goto(-300, 50)
t.pendown()

t.pencolor("orange")
t.fillcolor("yellow")

t.begin_fill()

for i in range(2):
    t.circle(70, 90)
    t.circle(35, 90)

t.end_fill()


# ---------------- POLYGON ----------------
t.penup()
t.goto(100, -50)
t.pendown()

t.pencolor("purple")
t.fillcolor("violet")

t.begin_fill()

for i in range(6):
    t.forward(80)
    t.left(60)

t.end_fill()


# Hide turtle
t.hideturtle()

# Keep window open
turtle.done()