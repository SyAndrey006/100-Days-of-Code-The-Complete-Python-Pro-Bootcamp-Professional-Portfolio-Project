import turtle
import time
import random
from turtledemo.sorting_animate import show_text

# -----Default setting-----
# Window
screen_width = 800
screen_height = 600

# Player and bullet
step_width = 20
bullet_speed = 5 #pixels per update cycle

# Aliens
alien_speed = 20
alien_speed_down = 20
alien_distance_horizontal = 50
alien_distance_vertical = 35
aliens_in_row = 8
aliens_in_column = 3
alien_y_start = (int)(screen_height / 2) - 50
alien_x_start = -(int)(screen_width / 2) + 100

# Alien's missile
max_alien_missiles = aliens_in_row
alien_missile_speed = 3


hud_y = -screen_height / 2 + 100

# Objects size
player_width = 20
player_height = 20
bullet_width = 20 * 0.15
bullet_height = 20 * 0.5
alien_width = 20
alien_height = 20 * 0.8
alien_missile_width = 20 * 0.25
alien_missile_height = 20 * 0.7

# Game Parameters
game_over = False
win = False
player_hp = 3
score = 0
alien_timer = 1 # How often we update aliens. Default every 1 second
alien_timer_decrease = (alien_timer - 0.1) / (aliens_in_row * aliens_in_column)
missile_timer = 60


# -----Window screen-----
window = turtle.Screen()
window.title("Space Invaders")
window.bgcolor("black")
window.setup(width = screen_width, height = screen_height)
window.tracer(0)


# -----HUD with score and number of lives-----
# Draw a line that divides board with
line = turtle.Turtle()
line.hideturtle()
line.color("white")
line.penup()
line.goto(-screen_width / 2, hud_y)
line.pendown()
line.goto(screen_width / 2, hud_y)

# ---Score place---
score_text = turtle.Turtle()
score_text.hideturtle()
score_text.color("white")
score_text.penup()
score_text.goto(screen_width / 2 - 150, hud_y - 40)

# ---Number of hp---
hp_text = turtle.Turtle()
hp_text.hideturtle()
hp_text.color("white")
hp_text.penup()
hp_text.goto(-screen_width / 2 + 20, hud_y - 40)

# Draw and update our score
def draw_score():
    score_text.clear()
    score_text.write(f"Score: {score}", font=("Arial", 16, "normal"))

draw_score()

# Draw and update our hp
def draw_hp():
    hp_text.clear()
    hp_text.write(f"HP: {player_hp}", font=("Arial", 16, "normal"))
draw_hp()


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
bullet.shapesize(stretch_wid = 0.5, stretch_len = 0.15)
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

for y in range (alien_y_start, alien_y_start - aliens_in_column * alien_distance_vertical, - alien_distance_vertical):
    for x in range( alien_x_start, alien_x_start + aliens_in_row * alien_distance_horizontal, alien_distance_horizontal):
        alien = turtle.Turtle()
        alien.shape("square")
        alien.color("green")
        alien.shapesize(stretch_wid = 0.8, stretch_len = 1)
        alien.penup()
        alien.goto(x, y)
        aliens.append(alien)
window.update()

aliens_direction_to_right  = True

# Finds number of aliens left
def aliens_left():
    count = 0
    for alien in aliens:
        if alien.isvisible():
            count += 1
    return count

# A move function for aliens
def aliens_move():
    global aliens_direction_to_right , game_over

    need_to_go_down = False

    # Find if we need to go down
    for alien in aliens:
        if not alien.isvisible(): #skip dead alien spaceships
            continue
        if (aliens_direction_to_right and alien.xcor() + alien_speed >= screen_width/2 - 20) or (not aliens_direction_to_right and alien.xcor() - alien_speed <= - screen_width/2 + 20):
            need_to_go_down = True
            break

    # If we need to go down, every visible alien spaceship goes down
    if need_to_go_down:
        for alien in aliens:
            if alien.isvisible():
                if alien.ycor() - alien_speed_down < hud_y +  alien_height/2: # Check if we are not below the HUD line, if below aliens disappear
                    alien.hideturtle()
                    continue
                alien.sety(alien.ycor() - alien_speed_down)

        aliens_direction_to_right = not aliens_direction_to_right
        return

    # Normal move to left or right
    for alien in aliens:
        if not alien.isvisible():
            continue

        if aliens_direction_to_right:
            alien.setx(alien.xcor() + alien_speed)
        else:
            alien.setx(alien.xcor() - alien_speed)

        if is_collision(player, player_width, player_height, alien, alien_width, alien_height):
            global player_hp
            player_hp -= 1
            draw_hp()

            if player_hp <= 0:
                game_over = True

# Finds if all aliens are dead
def all_aliens_dead():
    if aliens_left() == 0:
        return True
    return False

# -----Alien's Missile
alien_missiles = []

# A function to find the lowest alien in the column
def bottom_aliens():
    shooters = {}

    for alien in aliens:
        if not alien.isvisible():
            continue
        x = alien.xcor()
        if x not in shooters or alien.ycor() < shooters[x].ycor():
            shooters[x] = alien

    return list(shooters.values())

# Missile creation
def create_alien_missile(x, y):
    missile = turtle.Turtle()
    missile.shape("square")
    missile.shapesize(stretch_wid=0.7, stretch_len=0.25)
    missile.color("red")
    missile.penup()
    missile.goto(x, y)
    return missile

# A function that randomly choose an alien to shoot a missile
def missile_shoot():
    if len(alien_missiles) >= max_alien_missiles:
        return
    shooters = bottom_aliens()
    if len(shooters) == 0:
        return
    alien = random.choice(shooters)

    missile = create_alien_missile(alien.xcor(), alien.ycor() - alien_height / 2 - alien_missile_height / 2 - 1)
    alien_missiles.append(missile)


# -----Collision check-----
def is_collision(t1, w1, h1, t2, w2, h2):
    left1 = t1.xcor() - w1 / 2
    right1 = t1.xcor() + w1 / 2
    top1 = t1.ycor() + h1 / 2
    bottom1 = t1.ycor() - h1 / 2

    left2 = t2.xcor() - w2 / 2
    right2 = t2.xcor() + w2 / 2
    top2 = t2.ycor() + h2 / 2
    bottom2 = t2.ycor() - h2 / 2

    return (left1 < right2 and right1 > left2 and top1 > bottom2 and bottom1 < top2)


# -----Game loop that calculate everything-----
last_move_time = time.time()

while not game_over:
    window.update()

    if not is_ready_to_launch:
        bullet.sety(bullet.ycor() + bullet_speed)
        if bullet.ycor() > screen_height / 2:
            bullet.hideturtle()
            is_ready_to_launch = True

    for missile in alien_missiles[:]:
        missile.sety(missile.ycor() - alien_missile_speed)

        if missile.ycor() < hud_y +  alien_height / 2:
            missile.hideturtle()
            alien_missiles.remove(missile)
            continue

        if is_collision(missile, alien_missile_width, alien_missile_height,player, player_width, player_height): #Check collision with a player
            missile.hideturtle()
            alien_missiles.remove(missile)
            player_hp -= 1
            draw_hp()
            if player_hp <= 0:
                game_over = True

        if not is_ready_to_launch and is_collision(bullet, bullet_width, bullet_height, missile, alien_missile_width, alien_missile_height): #Check collision with a bullet
            bullet.hideturtle()
            is_ready_to_launch = True
            missile.hideturtle()
            alien_missiles.remove(missile)
            score += 10 # Extra points for destroying a missile
            draw_score()

    if random.randint(1, missile_timer) == 1:
        missile_shoot()

    if time.time() - last_move_time > alien_timer:
        aliens_move()
        last_move_time = time.time()

    for alien in aliens:
        if (alien.isvisible() and is_ready_to_launch == False and
                is_collision(bullet, bullet_width, bullet_height,alien, alien_width, alien_height)):
            bullet.hideturtle()
            is_ready_to_launch = True
            alien.hideturtle()
            score += 10 # Points for destroying an alien spaceship
            missile_timer -= 1
            alien_timer -= alien_timer_decrease
            draw_score()

    if all_aliens_dead():
        game_over = True
        win = True
        break

    time.sleep(0.02)

# -----Game Over-----
window.clear()
window.bgcolor("black")
text = turtle.Turtle()
text.hideturtle()
text.color("white")
text.penup()
text.goto(0, 40)

if win:
    text.write("YOU WIN!", align="center", font=("Arial", 36, "bold"))
else:
    text.write("GAME OVER", align="center", font=("Arial", 36, "bold"))

text.goto(0, -10)
text.write(f"Score: {score}", align="center", font=("Arial", 20, "normal"))

window.mainloop()