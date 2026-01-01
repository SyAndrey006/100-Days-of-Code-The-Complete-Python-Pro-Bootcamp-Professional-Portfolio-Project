import turtle
import time

# -----Default setting-----
screen_width = 800
screen_height = 700
step_width = 20
bullet_speed = 5 #pixels per update cycle
alien_speed = 20
alien_speed_down = 20
alien_distance = 50
aliens_in_row = 8
aliens_in_column = 3
INF = 1000
alien_y_start = (int)(screen_height / 2) - 50
alien_x_start = -(int)(screen_width / 2) + 100

game_over = False


# -----Window screen-----
window = turtle.Screen()
window.title("Space Invaders")
window.bgcolor("black")
window.setup(width = screen_width, height = screen_height)
window.tracer(0)


# -----Player aka spaceship which can move to left and to right-----
player = turtle.Turtle()
player.shape("triangle")
player.color("yellow")
player.penup()
player.goto(0, - (screen_height / 2 - 150) )

def move_left():
    x = player.xcor()
    if x - step_width > - screen_width/2:
        player.setx(x - step_width)

def move_right():
    x = player.xcor()
    if x + step_width < screen_width/2:
        player.setx(x + step_width)

window.listen()
window.onkey(move_left,"Left")
window.onkey(move_right,"Right")

# -----Bullet which we shoot thew aliens-----
bullet = turtle.Turtle()
bullet.shape("square")
bullet.shapesize(stretch_wid = 0.5, stretch_len = 0.25)
bullet.color("white")
bullet.penup()
bullet.hideturtle()

is_ready_to_launch = True

def fire_bullet():
    global is_ready_to_launch
    if is_ready_to_launch:
        is_ready_to_launch = False
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

window.onkey(fire_bullet, "space")

# -----Aliens spaceships on top-----
aliens = []
aliens_direction_to_right = []

for y in range (alien_y_start, alien_y_start - aliens_in_column * alien_distance, - alien_distance):
    for x in range( alien_x_start, alien_x_start + aliens_in_row * alien_distance, alien_distance):
        alien = turtle.Turtle()
        alien.shape("square")
        alien.color("green")
        alien.penup()
        alien.goto(x, y)
        aliens.append(alien)
        aliens_direction_to_right.append(True)
window.update()



def aliens_move():
    global game_over
    for i in range(len(aliens)):
        alien = aliens[i]
        if alien.xcor() == INF:
            continue # if it is dead, we skip it
        if aliens_direction_to_right[i]:
            if alien.xcor() + alien_speed < screen_width/2:
                alien.setx(alien.xcor() + alien_speed)
            else :
                alien.sety(alien.ycor() - alien_speed_down)
                aliens_direction_to_right[i] = False
        else:
            if alien.xcor() + alien_speed > - screen_width/2:
                alien.setx(alien.xcor() - alien_speed)
            else :
                alien.sety(alien.ycor() - alien_speed_down)
                aliens_direction_to_right[i] = True

        if is_collision(alien, player):
            game_over = True


# -----Collision check-----
def is_collision(t1, t2):
    return t1.distance(t2) < 20


# -----Game loop that calculate everything-----
last_move_time = time.time()

while not game_over:
    window.update()

    if not is_ready_to_launch:
        bullet.sety(bullet.ycor() + bullet_speed)
        if bullet.ycor() > screen_height / 2:
            bullet.hideturtle()
            is_ready_to_launch = True

    if time.time() - last_move_time > 1:
        aliens_move()
        last_move_time = time.time()

    for alien in aliens:
        if is_ready_to_launch == False and is_collision(bullet, alien):
            bullet.hideturtle()
            is_ready_to_launch = True
            alien.goto(INF, INF)

    time.sleep(0.02)

# -----Game Over
text = turtle.Turtle()
text.color("red")
text.penup()
text.hideturtle()
text.goto(0, 0)
text.write("GAME OVER", align="center", font=("Arial", 36, "bold"))

window.mainloop()