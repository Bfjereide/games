import turtle
import random
import time

score_a = 0
score_b = 0
power_up_active = False
power_up_type = None
power_up_spawned = False
last_power_up_time = 0

screen = turtle.Screen()
screen.title("Pong")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 7
ball.dy = -7

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 20, "normal"))

power_up = turtle.Turtle()
power_up.speed(0)
power_up.shape("circle")
power_up.color("yellow")
power_up.penup()
power_up.hideturtle()  # Initially hidden

def paddle_a_up():
    y = paddle_a.ycor()
    y += 30
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 30
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 30
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 30
    paddle_b.sety(y)

def spawn_power_up():
    global power_up_spawned, last_power_up_time, power_up
    x = random.randint(-350, 350)
    y = random.randint(-250, 250)
    power_up.goto(x, y)
    power_up.showturtle()
    power_up_spawned = True
    last_power_up_time = time.time()

def check_power_up_collision():
    global power_up_active, power_up_type, power_up_spawned
    if power_up.distance(paddle_a) < 50:
        activate_power_up("A")
    elif power_up.distance(paddle_b) < 50:
        activate_power_up("B")

def activate_power_up(player):
    global power_up_active, power_up_type, power_up_spawned
    if not power_up_active:
        power_up_active = True
        power_up_type = random.choice(['slow_ball', 'fast_paddle', 'double_ball'])
        power_up.hideturtle()
        power_up_spawned = False
        if player == "A":
            print("Player A activated:", power_up_type)
        else:
            print("Player B activated:", power_up_type)

        # Activate the power-up effects
        if power_up_type == 'slow_ball':
            ball.dx *= 0.5  # Slow down ball for the other player
            screen.ontimer(reset_ball_speed, 5000)  # Reset after 5 seconds
        elif power_up_type == 'fast_paddle':
            if player == "A":
                paddle_a.shapesize(stretch_wid=5, stretch_len=1.5)
                screen.ontimer(reset_paddle_size, 5000, paddle_a)
            else:
                paddle_b.shapesize(stretch_wid=5, stretch_len=1.5)
                screen.ontimer(reset_paddle_size, 5000, paddle_b)
        elif power_up_type == 'double_ball':
            new_ball = turtle.Turtle()
            new_ball.speed(0)
            new_ball.shape("circle")
            new_ball.color("white")
            new_ball.penup()
            new_ball.goto(0, 0)
            new_ball.dx = 7 * (1 - 0.2 * random.random())  # Random speed
            new_ball.dy = -7 * (1 - 0.2 * random.random())  # Random speed
            screen.update()

def reset_ball_speed():
    ball.dx *= 2  # Reset the speed of the ball
    global power_up_active
    power_up_active = False

def reset_paddle_size(paddle):
    paddle.shapesize(stretch_wid=5, stretch_len=1)  # Reset the paddle's size

def update():
    global score_a, score_b, power_up_active, last_power_up_time, power_up_spawned
    screen.update()
    
    # Move ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Boundaries
    if ball.ycor() > 280:
        ball.sety(280)
        ball.dy *= -1
    if ball.ycor() < -280:
        ball.sety(-280)
        ball.dy *= -1

    # Paddle collision
    if (ball.xcor() < -340 and (paddle_a.ycor() + 50 > ball.ycor() > paddle_a.ycor() - 50)):
        ball.setx(-340)
        ball.dx *= -1

    if (ball.xcor() > 340 and (paddle_b.ycor() + 50 > ball.ycor() > paddle_b.ycor() - 50)):
        ball.setx(340)
        ball.dx *= -1

    # Scoring
    if ball.xcor() > 380:
        score_a += 1
        pen.clear()
        pen.write("Player A: {} Player B: {}".format(score_a, score_b), align="center", font=("Courier", 20, "normal"))
        ball.goto(0, 0)
        ball.dx *= -1
        
    if ball.xcor() < -380:
        score_b += 1
        pen.clear()
        pen.write("Player A: {} Player B: {}".format(score_a, score_b), align="center", font=("Courier", 20, "normal"))
        ball.goto(0, 0)
        ball.dx *= -1

    # Check power-up collision
    if power_up_spawned:
        check_power_up_collision()

    # Spawn power-up every 10 seconds if the last one has been used
    if not power_up_spawned and (time.time() - last_power_up_time > 10):
        spawn_power_up()

    # Update every 20ms
    screen.ontimer(update, 20)

def quit_game():
    screen.bye()

screen.listen()
screen.onkeypress(paddle_a_up, "w")
screen.onkeypress(paddle_a_down, "s")
screen.onkeypress(paddle_b_up, "Up")
screen.onkeypress(paddle_b_down, "Down")
screen.onkeypress(quit_game, "q")

update()  # Start the update loop
turtle.mainloop()
